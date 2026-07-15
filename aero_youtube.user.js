// ==UserScript==
// @name         Aero Downloader Bridge (YouTube)
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Envía videos de YouTube directamente a Aero Downloader PRO
// @author       Aero Downloader
// @match        *://*.youtube.com/watch*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function sendToAero() {
        const videoUrl = window.location.href;
        const btn = document.getElementById('aero-btn');
        btn.innerText = 'Enviando...';
        
        fetch('http://127.0.0.1:65432/?url=' + encodeURIComponent(videoUrl))
            .then(response => {
                if (response.ok) {
                    btn.innerText = '¡Enviado a Aero!';
                    btn.style.backgroundColor = '#10B981'; // Verde éxito
                    setTimeout(() => {
                        btn.innerText = '⚡ Descargar con Aero';
                        btn.style.backgroundColor = '#00B4DB';
                    }, 3000);
                } else {
                    alert('Error: Aero Downloader no parece estar abierto.');
                    btn.innerText = '⚡ Descargar con Aero';
                }
            })
            .catch(error => {
                alert('Asegúrate de que Aero Downloader PRO esté abierto antes de hacer clic.');
                btn.innerText = '⚡ Descargar con Aero';
            });
    }

    function injectButton() {
        if (document.getElementById('aero-btn')) return;

        // Inyectamos un botón flotante en la esquina inferior derecha. 
        // Es 100% garantizado que se verá, sin importar si YouTube cambia su diseño.
        const btn = document.createElement('button');
        btn.id = 'aero-btn';
        btn.innerText = '⚡ Descargar con Aero';
        btn.style.position = 'fixed';
        btn.style.bottom = '40px';
        btn.style.right = '40px';
        btn.style.zIndex = '999999';
        btn.style.backgroundColor = '#00B4DB';
        btn.style.color = '#ffffff';
        btn.style.border = 'none';
        btn.style.borderRadius = '30px';
        btn.style.padding = '15px 25px';
        btn.style.fontSize = '16px';
        btn.style.fontWeight = 'bold';
        btn.style.cursor = 'pointer';
        btn.style.fontFamily = 'Roboto, Arial, sans-serif';
        btn.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.3)';
        btn.style.transition = 'all 0.2s ease-in-out';
        
        btn.onmouseover = () => {
            btn.style.backgroundColor = '#0083B0';
            btn.style.transform = 'scale(1.05)';
        };
        btn.onmouseout = () => {
            btn.style.backgroundColor = '#00B4DB';
            btn.style.transform = 'scale(1)';
        };

        btn.onclick = sendToAero;

        document.body.appendChild(btn);
    }

    // YouTube usa navegación interna (Polymer), el script necesita chequear si la página cambió
    setInterval(injectButton, 1000);
})();
