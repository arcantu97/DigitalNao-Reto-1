document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const windowHeight = window.innerHeight;
    const content = document.getElementById('content');
    let pageHeight = body.scrollWidth;
    let numBoxes = Math.ceil(pageHeight / windowHeight);

    generarCajas();

    window.addEventListener('scroll', function () {
        const scrollPosition = window.pageYOffset;
        const maxScroll = body.scrollHeight - windowHeight;
        // Definimos que cuando llegue al scroll máximo, 
        // se generen nuevas "boxes" para el scroll.
        if (scrollPosition >= maxScroll - 1) {
            generarCajas();
        }
    });

    function generarCajas() {
        for (let i = 0; i < numBoxes; i++) {
            const box = document.createElement('div');
            box.className = 'sized-box';

            // Calcula el color basado en la posición de la caja
            const red = Math.floor((i / numBoxes) * 255);
            const green = 0;
            const blue = Math.floor(((numBoxes - i) / numBoxes) * 255);
            box.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;

            content.appendChild(box);
        }

        pageHeight = body.scrollHeight;
        numBoxes = Math.ceil(pageHeight / windowHeight);
    }
});
