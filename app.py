from flask import Flask, request, jsonify  # Importazione delle librerie necessarie per creare l'app Flask
from flask_cors import CORS  # Importa CORS per gestire richieste da domini diversi
import sqlite3  # Per gestire SQLite
import bcrypt  # Per la gestione sicura delle password
from flask import g  # Per il contesto del database
from flask import session  # Per gestire sessioni utente
from functools import wraps

app = Flask(__name__)  # Inizializza l'app Flask
app.secret_key = 'd0e5f645abc8f9d76a3c2e475b1d7d3a'
app.config['SESSION_COOKIE_SECURE'] = False  # Solo per sviluppo locale
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(app, supports_credentials=True)  # Abilita CORS per permettere richieste cross-origin
DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_tables():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS User (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Flight (
                flightID INTEGER PRIMARY KEY AUTOINCREMENT,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                price REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Booking (
                bookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER NOT NULL,
                flightID INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (userID) REFERENCES User(userID),
                FOREIGN KEY (flightID) REFERENCES Flight(flightID)
            );
        ''')
        db.commit()

def populate_test_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        import bcrypt
        users = [
            ("Mario Rossi", "mario.rossi@example.com", "+390123456789", bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')),
            ("Giulia Verdi", "giulia.verdi@example.com", "+390987654321", bcrypt.hashpw("mypassword".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        ]

        for user in users:
            try:
                cursor.execute('''
                    INSERT INTO User (name, email, phone, password) VALUES (?, ?, ?, ?)
                ''', user)
            except sqlite3.IntegrityError:
                print(f"Utente con email {user[1]} già esistente. Saltato.")
        
        db.commit()

#Necessaria l'autenticazione
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Autenticazione richiesta"}), 401
        return f(*args, **kwargs)
    return decorated_function

############################## GESTIONE VOLI ############################

# Endpoint per cercare voli disponibili
@app.route('/search-flights', methods=['POST'])
def search_flights():
    data = request.get_json()
    departure = data.get('departure')
    destination = data.get('destination')
    date = data.get('date')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT flightID, departure, destination, date, price
        FROM Flight
        WHERE departure = ? AND destination = ? AND date = ?
    ''', (departure, destination, date))
    flights = cursor.fetchall()

    return jsonify([
        {"flightID": row[0], "departure": row[1], "destination": row[2], "date": row[3], "price": row[4]}
        for row in flights
    ])

# Endpoint per aggiungere voli
@app.route('/add-flight', methods=['POST'])
def add_flight():
    data = request.get_json()
    departure = data.get('departure')
    destination = data.get('destination')
    date = data.get('date')
    price = data.get('price')

    if not all([departure, destination, date, price]):
        return jsonify({"error": "Tutti i campi sono obbligatori"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO Flight (departure, destination, date, price)
        VALUES (?, ?, ?, ?)
    ''', (departure, destination, date, price))
    db.commit()
    return jsonify({"message": "Volo aggiunto con successo"}), 201

############################## GESTIONE PRENOTAZIONI ############################

# Endpoint per confermare una nuova prenotazione
@app.route('/confirm-booking', methods=['POST'])
@login_required
def confirm_booking():
    data = request.get_json()
    user_id = session['user_id']
    flight_id = data.get('flightID')
    passengers = data.get('passengers', 1)  # Numero passeggeri
    status = "Confirmed"

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO Booking (userID, flightID, status)
        VALUES (?, ?, ?)
    ''', (user_id, flight_id, status))
    db.commit()

    return jsonify({"message": "Prenotazione confermata"}), 201

# Endpoint per ottenere i dettagli di una prenotazione specifica
@app.route('/get-bookings', methods=['GET'])
@login_required
def get_bookings():
    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT b.bookingID, f.departure, f.destination, f.date, f.price, b.status
        FROM Booking b
        JOIN Flight f ON b.flightID = f.flightID
        WHERE b.userID = ?
    ''', (user_id,))
    bookings = cursor.fetchall()
    return jsonify([{
        "bookingID": row[0],
        "departure": row[1],
        "destination": row[2],
        "date": row[3],
        "price": row[4],
        "status": row[5]
    } for row in bookings])

# Endpoint per aggiornare una prenotazione esistente
@app.route('/update-booking', methods=['PUT'])
def update_booking():

    data = request.get_json()
    booking_id = data.get('bookingID')
    flight_id = data.get('flightID')
    status = data.get('status')

    if not booking_id or not (flight_id or status):
        return jsonify({"error": "bookingID e almeno un campo (flightID o status) sono richiesti"}), 400

    db = get_db()
    cursor = db.cursor()

    # Costruisci dinamicamente l'update in base ai campi forniti
    update_fields = []
    values = []

    if flight_id:
        update_fields.append("flightID = ?")
        values.append(flight_id)
    if status:
        update_fields.append("status = ?")
        values.append(status)

    values.append(booking_id)  # bookingID va alla fine per la clausola WHERE

    update_query = f"UPDATE Booking SET {', '.join(update_fields)} WHERE bookingID = ?"
    cursor.execute(update_query, values)
    db.commit()

    if cursor.rowcount > 0:
        return jsonify({"message": "Prenotazione aggiornata con successo"}), 200
    else:
        return jsonify({"error": "Nessuna prenotazione trovata con l'ID specificato"}), 404

# Endpoint per cancellare una prenotazione
@app.route('/cancel-booking', methods=['DELETE'])
@login_required
def cancel_booking():
    booking_id = request.args.get('bookingId')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE Booking SET status = 'Cancelled' WHERE bookingID = ?
    ''', (booking_id,))
    db.commit()
    return jsonify({"message": "Prenotazione annullata"}), 200

############################## GESTIONE UTENTI ############################

#Verifica se l'utente è autenticato o meno
@app.route('/is_authenticated', methods=['GET'])
def is_authenticated():
    print(f"Session during is_authenticated: {session}")
    print(f"Cookie received: {request.cookies}")  # Debug cookie
    if 'user_id' in session:
        return jsonify({"is_authenticated": True}), 200
    else:
        return jsonify({"is_authenticated": False}), 200

# Registrazione utente
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    if not name or not email or not phone or not password or len(password) < 8:
        return jsonify({"error": "Tutti i campi sono obbligatori e la password deve avere almeno 8 caratteri."}), 400

    # Hash della password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO User (name, email, phone, password) VALUES (?, ?, ?, ?)
        ''', (name, email, phone, hashed_password))
        db.commit()
        return jsonify({"message": "Registrazione completata con successo"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "L'email è già registrata"}), 400

#Login utente
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT userID, password FROM User WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        session['user_id'] = user[0]
        print(f"Session after login: {session}")  # Debug
        return jsonify({"message": "Login effettuato con successo"}), 200
    else:
        return jsonify({"error": "Email o password non corretti"}), 401
    
#Logout utente
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout effettuato con successo"}), 200

if __name__ == "__main__":
    create_tables()
    #populate_test_data() # Popolare i dati di test
    app.run(debug=True) # Avvia il server Flask in modalità di debug per lo sviluppo