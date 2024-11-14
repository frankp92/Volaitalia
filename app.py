from flask import Flask, request, jsonify  # Importazione delle librerie necessarie per creare l'app Flask
from flask_cors import CORS  # Importa CORS per gestire richieste da domini diversi

app = Flask(__name__)  # Inizializza l'app Flask
CORS(app)  # Abilita CORS per permettere richieste cross-origin

# Endpoint per cercare voli disponibili
@app.route('/search-flights', methods=['POST'])
def search_flights():
    data = request.get_json()  # Riceve i dati della richiesta JSON inviata dal frontend

    # Otteniamo i dettagli della richiesta
    departure = data.get('departure')  # Aeroporto di partenza
    destination = data.get('destination')  # Aeroporto di destinazione
    date = data.get('date')  # Data di partenza
    passengers = data.get('passengers')  # Numero di passeggeri (opzionale, se gestito dal frontend)

    # Esempio di risposta simulata per i voli
    flights = [
        {"flight_number": "ITA2024", "departure": departure, "destination": destination, "date": date, "price": 120},
        {"flight_number": "ITA3035", "departure": departure, "destination": destination, "date": date, "price": 150},
        {"flight_number": "ITA4045", "departure": departure, "destination": destination, "date": date, "price": 200},
    ]

    # Restituisce la lista dei voli come JSON
    return jsonify(flights), 200

# Endpoint per confermare una nuova prenotazione
@app.route("/confirm-booking", methods=["POST"])
def confirm_booking():
    booking_data = request.get_json()  # Ottiene i dati della prenotazione dal frontend

    # Recupera i dettagli della prenotazione
    flight_number = booking_data["flightNumber"]  # Numero del volo
    name = booking_data["name"]  # Nome del passeggero
    email = booking_data["email"]  # Email del passeggero
    phone = booking_data["phone"]  # Numero di telefono del passeggero

    # Qui potremmo inserire la logica per salvare i dati della prenotazione in un database

    # Risponde con un messaggio di successo alla conferma della prenotazione
    return jsonify({"message": "Prenotazione confermata"}), 200

# Endpoint per ottenere i dettagli di una prenotazione specifica
@app.route("/get-booking", methods=["GET"])
def get_booking():
    booking_id = request.args.get("bookingId")  # Recupera l'ID della prenotazione dai parametri URL

    # Logica per recuperare i dettagli della prenotazione usando l'ID (attualmente restituisce dati fittizi)
    booking_data = {
        "name": "Mario Rossi",  # Nome fittizio
        "email": "mario.rossi@example.com",  # Email fittizia
        "phone": "+39 123456789"  # Telefono fittizio
    }

    # Restituisce i dati della prenotazione come JSON
    return jsonify(booking_data), 200

# Endpoint per aggiornare una prenotazione esistente
@app.route("/update-booking", methods=["PUT"])
def update_booking():
    updated_data = request.get_json()  # Riceve i dati aggiornati della prenotazione

    # Recupera i dettagli aggiornati della prenotazione
    booking_id = updated_data["bookingId"]
    name = updated_data["name"]
    email = updated_data["email"]
    phone = updated_data["phone"]

    # Logica per aggiornare i dati della prenotazione (attualmente non aggiorna un database)

    # Risponde con un messaggio di successo alla modifica della prenotazione
    return jsonify({"message": "Prenotazione aggiornata"}), 200

# Endpoint per cancellare una prenotazione
@app.route("/delete-booking", methods=["DELETE"])
def delete_booking():
    booking_id = request.args.get("bookingId")  # Recupera l'ID della prenotazione da cancellare

    # Logica per cancellare la prenotazione usando l'ID (attualmente solo un messaggio di successo)

    # Risponde con un messaggio di successo alla cancellazione della prenotazione
    return jsonify({"message": "Prenotazione cancellata con successo"}), 200

if __name__ == '__main__':
    app.run(debug=True)  # Avvia il server Flask in modalità di debug per lo sviluppo
