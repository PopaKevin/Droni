const orderId = 1; // Puoi recuperarlo da URL o input utente (per test si usa 1)
document.getElementById("order-id").textContent = orderId;
const API_BASE_URL = "http://127.0.0.1:5001"; // Porta aggiornata a 5001

// Mostra dettagli ordine
axios.get(`${API_BASE_URL}/ordini/${orderId}`)
.then(res => {
    const info = res.data;
    let html = `<p><strong>ID Ordine:</strong> ${info.ID}</p>`;
    html += `<p><strong>Destinazione:</strong> ${info.IndirizzoDestinazione}</p>`;
    html += `<p><strong>Peso totale:</strong> ${info.PesoTotale} kg</p>`;
    html += `
        <h4 class="font-semibold mt-3">Prodotti:</h4>
        <ul class="list-disc pl-5 space-y-1">`;
    info.prodotti.forEach(p => {
        html += `<li>${p.nome} (${p.categoria}) - ${p.Quantita} pezzi, ${p.peso} kg</li>`;
    });
    html += `</ul>`;
    document.getElementById("order-info").innerHTML = html;
})
.catch(err => {
    console.error("Errore nel recupero dettagli ordine:", err);
    document.getElementById("order-info").innerHTML = `<p class="text-red-600">Non è stato possibile caricare i dettagli dell'ordine ${orderId}.</p>`;
});

// Mostra tracce drone sulla mappa
const map = L.map('map').setView([45.4642, 9.19], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

axios.get(`${API_BASE_URL}/missioni/${orderId}/tracce`)
.then(res => {
    const tracce = res.data;
    if (tracce.length === 0) {
        console.log("Nessuna traccia trovata per questa missione.");
        return;
    }
    const latlngs = tracce.map(t => [t.Latitudine, t.Longitudine]);
    L.polyline(latlngs, {color: '#1d4ed8', weight: 4}).addTo(map);
    
    // Aggiungi marker di inizio e fine
    L.marker(latlngs[0]).addTo(map).bindPopup("Partenza").openPopup();
    L.marker(latlngs[latlngs.length - 1], {icon: L.divIcon({className: 'bg-green-500 rounded-full p-2 w-4 h-4 shadow-lg'})}).addTo(map).bindPopup("Destinazione");

    map.fitBounds(latlngs, { padding: [50, 50] });
})
.catch(err => console.error("Errore nel recupero tracce:", err));

// Invia valutazione
document.getElementById("submit-rating").addEventListener("click", () => {
    const ratingInput = document.getElementById("rating");
    const val = parseInt(ratingInput.value);
    const statusDiv = document.getElementById("rating-status");
    statusDiv.textContent = "";

    if (isNaN(val) || val < 1 || val > 5) {
        statusDiv.className = "mt-2 text-sm font-medium text-red-600";
        statusDiv.textContent = "Inserisci una valutazione valida (1-5).";
        return;
    }

    statusDiv.className = "mt-2 text-sm font-medium text-blue-600";
    statusDiv.textContent = "Invio in corso...";

    axios.post(`${API_BASE_URL}/valutazioni`, {
        id_missione: orderId,
        valutazione: val // CORREZIONE: usiamo la variabile 'val'
    })
    .then(res => {
        if (res.data.successo) {
            statusDiv.className = "mt-2 text-sm font-medium text-green-600";
            statusDiv.textContent = "Valutazione inviata con successo! Grazie.";
            ratingInput.disabled = true;
            document.getElementById("submit-rating").disabled = true;
        }
    })
    .catch(err => {
        statusDiv.className = "mt-2 text-sm font-medium text-red-600";
        statusDiv.textContent = `Errore nell'invio della valutazione: ${err.response ? err.response.data.errore : err.message}`;
        console.error("Errore valutazione:", err);
    });
});