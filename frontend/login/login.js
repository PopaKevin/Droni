const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const errorMsg = document.getElementById("error-msg");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorMsg.classList.add("hidden");
    errorMsg.textContent = "";

    const email = emailInput.value;
    const password = passwordInput.value;

    try {
        // Nota: ho modificato la porta da 5000 a 5001 per coerenza con app.py
        const response = await axios.post("http://127.0.0.1:5002/login", {
            email: email,
            password: password
        });

        if (response.data.successo) {
            const ruolo = response.data.ruolo;
            // Esempio di reindirizzamento
            if (ruolo === "Admin") {
                // Sostituisci con il percorso corretto se diverso
                window.location.href = "admin.html"; 
            } else if (ruolo === "Cliente") {
                // I clienti probabilmente andranno alla loro dashboard o tracciamento
                window.location.href = "customer.html";
            } else {
                // Altri ruoli
                window.location.href = "/dashboard";
            }
        }
    } catch (error) {
        let message = "Errore di connessione al server.";
        if (error.response && error.response.data && error.response.data.errore) {
            message = error.response.data.errore;
        }
        errorMsg.textContent = message;
        errorMsg.classList.remove("hidden");
    }
});