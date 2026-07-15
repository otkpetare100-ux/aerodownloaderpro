(function() {
    'use strict';

    function sendToAero() {
        const videoUrl = window.location.href;
        const btn = document.getElementById('aero-btn-floating');
        if (btn) btn.style.opacity = '0.5';
        
        fetch('http://127.0.0.1:65432/?url=' + encodeURIComponent(videoUrl))
            .then(response => {
                if (response.ok) {
                    if (btn) {
                        btn.style.opacity = '1';
                        btn.style.filter = 'brightness(1.5)';
                        setTimeout(() => {
                            btn.style.filter = 'none';
                        }, 3000);
                    }
                } else {
                    if (btn) btn.style.opacity = '1';
                    window.location.href = 'aerodl://' + encodeURIComponent(videoUrl);
                }
            })
            .catch(error => {
                if (btn) btn.style.opacity = '1';
                window.location.href = 'aerodl://' + encodeURIComponent(videoUrl);
            });
    }

    function injectButton() {
        if (!window.location.href.includes('/watch') && !window.location.href.includes('/shorts')) {
            const existingBtn = document.getElementById('aero-btn-floating');
            if (existingBtn) existingBtn.remove();
            return;
        }

        if (document.getElementById('aero-btn-floating')) return;

        const btn = document.createElement('button');
        btn.id = 'aero-btn-floating';
        // Diseño de botón CSS Ultra-Premium (sin usar imágenes, 100% nítido)
        btn.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
                <span>Descargar con Aero</span>
            </div>
        `;
        
        btn.style.position = 'fixed';
        btn.style.bottom = '40px';
        btn.style.right = '40px';
        btn.style.zIndex = '9999999';
        btn.style.backgroundColor = '#16161e'; // Fondo súper oscuro
        btn.style.color = '#ffffff';
        btn.style.border = '1px solid #00B4DB'; // Borde cian fino
        btn.style.borderRadius = '14px'; // Bordes redondeados modernos
        btn.style.padding = '12px 20px';
        btn.style.fontSize = '15px';
        btn.style.fontWeight = '600';
        btn.style.cursor = 'pointer';
        btn.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
        // Sombra doble para dar efecto de "brillo" premium cian
        btn.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 180, 219, 0.3)';
        btn.style.transition = 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)';
        btn.style.backdropFilter = 'blur(10px)'; // Efecto cristal si hay algo debajo
        
        btn.onmouseover = () => {
            btn.style.transform = 'translateY(-3px) scale(1.02)';
            btn.style.boxShadow = '0 15px 30px -5px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 180, 219, 0.6)';
            btn.style.backgroundColor = '#1a1a24';
        };
        btn.onmouseout = () => {
            btn.style.transform = 'translateY(0) scale(1)';
            btn.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 180, 219, 0.3)';
            btn.style.backgroundColor = '#16161e';
        };

        btn.onclick = sendToAero;

        document.body.appendChild(btn);
    }

    setInterval(injectButton, 1000);
})();
