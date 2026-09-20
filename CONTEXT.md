# Aspect Ratio Neo

A catalog of pixel-size suggestions that write generation width and height once. Generation Size stays freely editable after that; the catalog does not stay bound to the sliders.

## Language

**Size Preset**:
A saved pair of absolute pixel dimensions (width and height). Applying one writes Generation Size once.
_Avoid_: Resolution preset, aspect ratio preset, AR button, ratio

**Generation Size**:
The current width and height on one tab’s sliders. The user may type any values after a Size Preset is applied.
_Avoid_: Resolution

**Catalog**:
The Size Presets offered in the select: built-in presets plus user extras from Settings. A suggestion list, not a live view of Generation Size.
_Avoid_: resolutions.txt, aspect_ratios.txt

**Custom**:
The idle Catalog choice at UI start. Selecting it does not write Generation Size. Slider edits never switch the select to Custom.
_Avoid_: mismatch, unsynced
