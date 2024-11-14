// Ottieni il numero di volo dall'URL
const urlParams = new URLSearchParams(window.location.search);  // Estrae i parametri dalla stringa di query nell'URL
const flightNumber = urlParams.get("flightNumber");  // Recupera il numero di volo dai parametri URL

// Mostra i dettagli del volo (simulazione)
const flightDetailsDiv = document.getElementById("flight-details");
flightDetailsDiv.innerHTML = `<p>Stai prenotando il volo numero: <strong>${flightNumber}</strong></p>`;  // Inserisce i dettagli del volo nel div

// Gestione del modulo di conferma
document.getElementById("confirmation-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Previene il comportamento predefinito di invio del form

    // Crea un oggetto con i dati della prenotazione
    const bookingData = {
        flightNumber: flightNumber,  // Numero del volo selezionato
        name: document.getElementById("name").value,  // Nome completo del passeggero
        email: document.getElementById("email").value,  // Email del passeggero
        phone: document.getElementById("phone").value  // Numero di telefono del passeggero
    };

    // Invia la richiesta al backend per confermare la prenotazione
    fetch("http://127.0.0.1:5000/confirm-booking", {
        method: "POST",  // Metodo HTTP POST per inviare dati
        headers: {
            "Content-Type": "application/json"  // Specifica il tipo di contenuto come JSON
        },
        body: JSON.stringify(bookingData)  // Converte i dati della prenotazione in formato JSON
    })
    .then(response => response.json())  // Converte la risposta in JSON
    .then(data => {
        alert("Prenotazione confermata con successo!");  // Mostra un messaggio di conferma all'utente
        window.location.href = `edit.html?bookingId=${data.bookingId}`;  // Reindirizza alla pagina di modifica con l'ID della prenotazione
    })
    .catch(error => {
        console.error("Errore durante la conferma della prenotazione:", error);  // Log dell'errore in console
        alert("Errore durante la conferma. Riprova.");  // Notifica di errore all'utente
    });
});
