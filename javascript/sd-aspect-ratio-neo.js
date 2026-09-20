function relocateAspectRatioNeo(tab) {
    const src = gradioApp().getElementById(`${tab}_aspect_ratio_neo`);
    const width = gradioApp().getElementById(`${tab}_width`);
    if (!src || !width) {
        return;
    }

    const dest = width.closest(`#${tab}_column_size`);
    if (!dest) {
        return;
    }

    let before = width;
    while (before.parentElement && before.parentElement !== dest) {
        before = before.parentElement;
    }

    if (src.parentElement === dest && src.nextElementSibling === before) {
        return;
    }

    dest.insertBefore(src, before);
}

onUiLoaded(function () {
    relocateAspectRatioNeo("txt2img");
    relocateAspectRatioNeo("img2img");
});
