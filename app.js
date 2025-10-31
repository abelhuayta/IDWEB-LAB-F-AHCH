document.addEventListener('DOMContentLoaded', () => {
    
    const triggers = document.querySelectorAll('.trigger-fondo');
    // Empezamos asumiendo que el proyector activo es ::before
    let activePseudo = 'before'; 

    // Opciones del observador
    const opciones = {
        threshold: 0.5 
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const nuevaImagen = entry.target.getAttribute('data-bg');
                
                // Si el proyector activo es 'before', preparamos y cambiamos a 'after'
                if (activePseudo === 'before') {
                    // 1. Cargamos la nueva imagen en el proyector oculto (::after)
                    document.body.style.setProperty('--bg-imagen-after', `url('${nuevaImagen}')`);
                    // 2. Cambiamos la clase para que el CSS haga la transición de opacidad
                    document.body.className = 'bg-active-after';
                    // 3. Actualizamos el estado
                    activePseudo = 'after';
                } 
                // Si no, hacemos lo contrario
                else {
                    // 1. Cargamos la nueva imagen en el proyector oculto (::before)
                    document.body.style.setProperty('--bg-imagen-before', `url('${nuevaImagen}')`);
                    // 2. Cambiamos la clase para que el CSS haga la transición de opacidad
                    document.body.className = 'bg-active-before';
                    // 3. Actualizamos el estado
                    activePseudo = 'before';
                }
            }
        });
    };

    // --- Configuración Inicial ---
    // Asegúrate de que el body tenga la clase inicial correcta al cargar
    document.body.className = 'bg-active-before';

    const observador = new IntersectionObserver(observerCallback, opciones);
    triggers.forEach(trigger => {
        observador.observe(trigger);
    });
});