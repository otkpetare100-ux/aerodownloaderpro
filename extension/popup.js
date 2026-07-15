document.getElementById('download-btn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('status');
    const btn = document.getElementById('download-btn');
    
    // Obtener la URL de la pestaña actual
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        let activeTab = tabs[0];
        let url = activeTab.url;
        
        btn.innerText = 'Enviando...';
        
        fetch('http://127.0.0.1:65432/?url=' + encodeURIComponent(url))
            .then(response => {
                if (response.ok) {
                    btn.innerText = '⚡ Descargar Video Actual';
                    statusDiv.innerText = '¡Enviado a Aero con éxito!';
                    statusDiv.className = 'success';
                } else {
                    btn.innerText = '⚡ Descargar Video Actual';
                    statusDiv.innerText = 'Abriendo Aero Downloader...';
                    statusDiv.className = 'success';
                    window.location.href = 'aerodl://' + encodeURIComponent(url);
                }
            })
            .catch(error => {
                btn.innerText = '⚡ Descargar Video Actual';
                statusDiv.innerText = 'Abriendo Aero Downloader...';
                statusDiv.className = 'success';
                window.location.href = 'aerodl://' + encodeURIComponent(url);
            });
    });
});
