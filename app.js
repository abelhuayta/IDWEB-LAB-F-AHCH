document.addEventListener('DOMContentLoaded', () => {
    
    const triggers = document.querySelectorAll('.trigger-fondo');
    let activePseudo = 'before'; 

    const opciones = {
        threshold: 0.5 
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const nuevaImagen = entry.target.getAttribute('data-bg');
                
                if (activePseudo === 'before') {
                    document.body.style.setProperty('--bg-imagen-after', `url('${nuevaImagen}')`);
                    document.body.className = 'bg-active-after';
                    activePseudo = 'after';
                } 
                else {
                    document.body.style.setProperty('--bg-imagen-before', `url('${nuevaImagen}')`);
                    document.body.className = 'bg-active-before';
                    activePseudo = 'before';
                }
            }
        });
    };

    document.body.className = 'bg-active-before';

    const observador = new IntersectionObserver(observerCallback, opciones);
    triggers.forEach(trigger => {
        observador.observe(trigger);
    });

});
