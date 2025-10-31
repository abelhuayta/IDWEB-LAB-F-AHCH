document.addEventListener('DOMContentLoaded', function() {

    const contenedorFondo = document.querySelector('.fondo');

    const trigger = document.querySelector('#trigger-fundido');

    if (!contenedorFondo || !trigger) {
        console.error("No se encontraron los elementos necesarios para el fundido.");
        return;
    }

    const opciones = {
        root: null, 
        threshold: 0.5 
    };

    const observador = new IntersectionObserver(function(entries, observer) {
        
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                
                contenedorFondo.classList.add('visible');
                
            } else {
                
                contenedorFondo.classList.remove('visible');
            }
        });

    }, opciones);

    observador.observe(trigger);

});