// Login Handler
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const loginData = {
        email: document.getElementById("login-email").value,
        password: document.getElementById("login-password").value
    };

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Login effettuato con successo!");
            window.location.href = "index.html"; // Reindirizza alla home
        } else {
            alert(data.error || "Errore durante il login. Riprova.");
        }
    })
    .catch(error => console.error("Errore durante il login:", error));
});

// Registration Handler
document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const registrationData = {
        name: document.getElementById("register-name").value,
        email: document.getElementById("register-email").value,
        phone: document.getElementById("register-phone").value,
        password: document.getElementById("register-password").value
    };
    
    if (!email || !password) {
        alert("Inserisci email e password.");
        return;
    }
    if (password.length < 8) {
        alert("La password deve avere almeno 8 caratteri.");
        return;
    }    
    
    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(registrationData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Registrazione completata con successo! Effettua il login.");
            document.getElementById("register-form").reset(); // Resetta il form
        } else {
            alert(data.error || "Errore durante la registrazione. Riprova.");
        }
    })
    .catch(error => console.error("Errore durante la registrazione:", error));
});