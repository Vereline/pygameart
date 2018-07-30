function defineImageSize(pictWidth, pictHeight, maxWidth, maxHeight) {
    let params = {
        'width': 0,
        'height': 0
    };

    if (pictHeight > pictWidth) {
        let coefficient = pictHeight / maxHeight;
        params['height'] = maxHeight;
        params['width'] = pictWidth / coefficient;
    } else if (pictHeight < pictWidth) {
        let coefficient = pictWidth / maxWidth;
        params['height'] = pictHeight/coefficient;
        params['width'] = maxWidth;
    } else {
        let coefficient = 1;
        if (maxWidth > maxHeight){
            coefficient = pictHeight / maxHeight;
        } else {
            coefficient = pictWidth / maxWidth;
        }
        params['height'] = pictHeight / coefficient;
        params['width'] = pictWidth/ coefficient;
    }

    return params
}

let bar = document.querySelector("#progress");
window.addEventListener("scroll", () => {
let max = document.body.scrollHeight - innerHeight;
bar.style.width = `${(pageYOffset / max) * 100}%`;
});