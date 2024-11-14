// Aggiunge un listener per l'invio del form di ricerca voli
document.getElementById("flight-search-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Previene il comportamento predefinito di invio del form

    // Raccoglie i dati della form
    const departure = document.getElementById("departure").value;  // Aeroporto di partenza
    const destination = document.getElementById("destination").value;  // Aeroporto di destinazione
    const date = document.getElementById("date").value;  // Data di partenza
    const passengers = document.getElementById("passengers").value;  // Numero di passeggeri

    // Crea un oggetto con i dati della ricerca
    const requestData = {
        departure: departure,
        destination: destination,
        date: date,
        passengers: passengers
    };

    // Invia i dati della ricerca al server Flask
    fetch("http://127.0.0.1:5000/search-flights", {
        method: "POST",  // Utilizza il metodo POST per inviare i dati
        headers: {
            "Content-Type": "application/json"  // Specifica il tipo di contenuto come JSON
        },
        body: JSON.stringify(requestData)  // Converte i dati della ricerca in formato JSON
    })
    .then(response => response.json())  // Converte la risposta in formato JSON
    .then(data => {
        displayFlightResults(data);  // Visualizza i risultati dei voli
    })
    .catch(error => {
        console.error("Errore durante la ricerca dei voli:", error);  // Log dell'errore in console
    });
});

// Funzione per mostrare i risultati dei voli
function displayFlightResults(flights) {
    const flightsList = document.getElementById("flights-list");
    flightsList.innerHTML = "";  // Pulisce la lista dei voli precedenti

    flights.forEach(flight => {
        const flightItem = document.createElement("div");
        flightItem.classList.add("flight-item");  // Aggiunge una classe CSS per stilizzare i risultati

        // Aggiunge i dettagli del volo con pulsante per prenotare
        flightItem.innerHTML = `
            <div class="flight-info">
                Numero Volo: ${flight.flight_number} - Prezzo: €${flight.price}
            </div>
            <div>Partenza: ${flight.departure} - Destinazione: ${flight.destination} - Data: ${flight.date}</div>
            <button onclick="confirmBooking('${flight.flight_number}')">Prenota</button>
        `;

        flightsList.appendChild(flightItem);  // Aggiunge il volo alla sezione risultati
    });
}

// Funzione per reindirizzare alla pagina di conferma prenotazione
function confirmBooking(flightNumber) {
    // Reindirizza a confirm.html con il numero di volo selezionato nell'URL
    window.location.href = `confirm.html?flightNumber=${flightNumber}`;
}