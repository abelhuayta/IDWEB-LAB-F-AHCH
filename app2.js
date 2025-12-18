document.addEventListener("DOMContentLoaded", () => {

    const fondo = document.querySelector(".fondo");
    const trigger = document.querySelector("#trigger-fundido");

    if (!fondo || !trigger) {
        console.warn("Fondo o trigger no encontrado.");
        return;
    }

    const opciones = {
        root: null,
        threshold: 0.25   
    };

    const observador = new IntersectionObserver((entradas) => {
        entradas.forEach(entry => {
            if (entry.isIntersecting) {
                fondo.classList.add("visible");
            } else {
                fondo.classList.remove("visible");
            }
        });
    }, opciones);

    observador.observe(trigger);
});
