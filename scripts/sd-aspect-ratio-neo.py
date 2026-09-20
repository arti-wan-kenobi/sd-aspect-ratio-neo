from __future__ import annotations

import re

import gradio as gr

from modules import script_callbacks, scripts, shared

CUSTOM_CHOICE = "Custom"

BUILTIN_PRESETS = (
    (832, 1216),
    (864, 1080),
    (768, 1344),
    (1024, 1536),
)

SLIDER_MIN = 64
SLIDER_MAX = 2048
EXTRA_LINE_RE = re.compile(r"^\s*(\d+)\s*(?:[,xX×]\s*|\s+)(\d+)\s*$")


def format_size(width: int, height: int) -> str:
    return f"{width} x {height}"


def canonical_key(width: int, height: int) -> tuple[int, int]:
    return (min(width, height), max(width, height))


def parse_extra_line(line: str) -> tuple[int, int] | None:
    text = line.split("#", 1)[0].strip()
    if not text:
        return None

    match = EXTRA_LINE_RE.match(text)
    if match is None:
        print(f"[sd-aspect-ratio-neo] skipping malformed extra preset: {line.strip()}")
        return None

    return int(match.group(1)), int(match.group(2))


def in_slider_range(width: int, height: int, min_size: int, max_size: int) -> bool:
    return min_size <= width <= max_size and min_size <= height <= max_size


def slider_limit(component, attr: str, default: int) -> int:
    if component is None:
        return default
    value = getattr(component, attr, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def build_catalog(width_comp=None, height_comp=None) -> list[tuple[int, int]]:
    min_size = max(
        slider_limit(width_comp, "minimum", SLIDER_MIN),
        slider_limit(height_comp, "minimum", SLIDER_MIN),
        SLIDER_MIN,
    )
    max_size = min(
        slider_limit(width_comp, "maximum", SLIDER_MAX),
        slider_limit(height_comp, "maximum", SLIDER_MAX),
        SLIDER_MAX,
    )

    presets: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()

    def add(width: int, height: int, *, warn_range: bool = False) -> None:
        if not in_slider_range(width, height, min_size, max_size):
            if warn_range:
                print(
                    f"[sd-aspect-ratio-neo] skipping extra preset outside slider range: {width} x {height}"
                )
            return
        key = canonical_key(width, height)
        if key in seen:
            return
        seen.add(key)
        presets.append((width, height))

    for width, height in BUILTIN_PRESETS:
        add(width, height)

    extras = getattr(shared.opts, "sd_aspect_ratio_neo_extras", "") or ""
    for line in extras.splitlines():
        parsed = parse_extra_line(line)
        if parsed is None:
            continue
        add(*parsed, warn_range=True)

    return presets


def apply_size_preset(choice: str, width, height, choice_to_size: dict[str, tuple[int, int]]):
    size = choice_to_size.get(choice)
    if size is None:
        return gr.skip(), gr.skip()
    return size


class AspectRatioNeoScript(scripts.Script):
    create_group = False

    def __init__(self):
        self.width = None
        self.height = None
        self.dropdown = None
        self._bound = False

    def title(self):
        return "Aspect Ratio Neo"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        tab = "img2img" if is_img2img else "txt2img"
        catalog = build_catalog(self.width, self.height)
        choice_to_size = {format_size(width, height): (width, height) for width, height in catalog}
        choices = [CUSTOM_CHOICE, *choice_to_size.keys()]

        with gr.Row(elem_id=f"{tab}_aspect_ratio_neo", elem_classes=["aspect-ratio-neo"]):
            self.dropdown = gr.Dropdown(
                label="Size",
                choices=choices,
                value=CUSTOM_CHOICE,
                elem_id=f"{tab}_aspect_ratio_neo_select",
                scale=1,
            )
            self.dropdown.do_not_save_to_config = True

        self._choice_to_size = choice_to_size
        self._try_bind()
        return None

    def after_component(self, component, **kwargs):
        elem_id = kwargs.get("elem_id")
        tab = "img2img" if self.is_img2img else "txt2img"

        if elem_id == f"{tab}_width":
            self.width = component
        elif elem_id == f"{tab}_height":
            self.height = component

        self._try_bind()

    def _try_bind(self):
        if self._bound or self.width is None or self.height is None or self.dropdown is None:
            return

        self.dropdown.change(
            fn=lambda choice, width, height: apply_size_preset(
                choice, width, height, self._choice_to_size
            ),
            inputs=[self.dropdown, self.width, self.height],
            outputs=[self.width, self.height],
            show_progress=False,
        )
        self._bound = True


def on_ui_settings():
    section = ("sd_aspect_ratio_neo", "Aspect Ratio Neo")
    shared.opts.add_option(
        "sd_aspect_ratio_neo_extras",
        shared.OptionInfo(
            "",
            "Additional size presets",
            gr.Textbox,
            {
                "lines": 6,
                "placeholder": "1280, 720\n1600 x 900",
            },
            section=section,
            category_id="ui",
        )
        .info("one per line: width, height or width x height. Duplicates and sizes outside the Width/Height sliders are ignored.")
        .needs_reload_ui(),
    )


script_callbacks.on_ui_settings(on_ui_settings)
