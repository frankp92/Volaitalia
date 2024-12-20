// Ottieni l'ID della prenotazione dall'URL
const urlParams = new URLSearchParams(window.location.search);  // Crea un oggetto per gestire i parametri URL
const bookingId = urlParams.get("bookingId");  // Recupera l'ID della prenotazione dai parametri URL

// Carica i dati della prenotazione esistente dal backend
fetch(`http://127.0.0.1:5000/get-booking?bookingId=${bookingId}`)
    .then(response => response.json())  // Converte la risposta in formato JSON
    .then(data => {
        // Popola i campi del form con i dati della prenotazione
        document.getElementById("name").value = data.name;
        document.getElementById("email").value = data.email;
        document.getElementById("phone").value = data.phone;
    })
    .catch(error => console.error("Errore nel caricamento della prenotazione:", error));  // Gestisce eventuali errori nel caricamento

// Gestione del form di modifica della prenotazione
document.getElementById("edit-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Previene il comportamento predefinito di invio del form

    // Crea un oggetto con i dati aggiornati della prenotazione
    const updatedData = {
        bookingId: bookingId,  // Include l'ID della prenotazione per identificare quale aggiornare
        name: document.getElementById("name").value,  // Nome aggiornato
        email: document.getElementById("email").value,  // Email aggiornata
        phone: document.getElementById("phone").value  // Telefono aggiornato
    };

    // Invia la richiesta per aggiornare la prenotazione
    fetch("http://127.0.0.1:5000/update-booking", {
        method: "PUT",  // Utilizza il metodo PUT per aggiornare i dati
        headers: {
            "Content-Type": "application/json"  // Specifica il tipo di contenuto come JSON
        },
        body: JSON.stringify(updatedData)  // Converte i dati aggiornati in formato JSON
    })
    .then(response => response.json())  // Converte la risposta in JSON
    .then(data => {
        alert("Prenotazione aggiornata con successo!");  // Mostra un messaggio di conferma
        window.location.href = "index.html";  // Reindirizza alla pagina principale
    })
    .catch(error => {
        console.error("Errore durante l'aggiornamento della prenotazione:", error);  // Log dell'errore in console
        alert("Errore durante l'aggiornamento. Riprova.");  // Notifica di errore all'utente
    });
});

// Gestione del pulsante per cancellare la prenotazione
document.getElementById("delete-button").addEventListener("click", function() {
    // Chiede conferma all'utente prima di procedere
    const confirmed = confirm("Sei sicuro di voler cancellare questa prenotazione?");
    if (confirmed) {
        // Invia la richiesta di cancellazione al backend
        fetch(`http://127.0.0.1:5000/delete-booking?bookingId=${bookingId}`, {
            method: "DELETE"  // Utilizza il metodo DELETE per rimuovere la prenotazione
        })
        .then(response => response.json())  // Converte la risposta in JSON
        .then(data => {
            alert("Prenotazione cancellata con successo!");  // Mostra un messaggio di conferma
            window.location.href = "index.html";  // Reindirizza alla pagina principale
        })
        .catch(error => {
            console.error("Errore durante la cancellazione della prenotazione:", error);  // Log dell'errore in console
            alert("Errore durante la cancellazione. Riprova.");  // Notifica di errore all'utente
        });
    }
});