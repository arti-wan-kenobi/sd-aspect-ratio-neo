# Aspect Ratio Neo

Size suggestions for [Stable Diffusion WebUI Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic). Replaces [sd-webui-ar](https://github.com/alemelis/sd-webui-ar).

## Usage

- **Size** sits above Width/Height and applies a saved size once. After that, the sliders can be edited freely; the select does not follow them.
- **Custom** is the idle choice. Selecting it does not change Width/Height.
- Use the built-in ⇅ next to the sliders to swap width and height.

Disable `sd-webui-ar` while this extension is enabled.

## Settings

**Settings → Aspect Ratio Neo → Additional size presets**

One extra size per line, then Reload UI:

```
1280, 720
1600 x 900
```

Built-in sizes stay in the list. Duplicates (including swapped width/height) and values outside the Width/Height slider range are ignored.
