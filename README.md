# Volaitalia

Questo documento fornisce una guida dettagliata per testare il codice del sistema di prenotazione voli sviluppato in HTML, CSS, JavaScript, e Flask per il back-end. Segui questi passaggi per installare le dipendenze, avviare il server, e testare il progetto.

## Requisiti Prerequisiti

1. **Python 3.x**
2. **Flask**
3. **Visual Studio Code (o un altro editor di codice a scelta)**
4. **Browser Web**

## Installazione e Configurazione

1. **Clona il Repository**: Clona questo progetto dalla tua repository locale o scarica i file necessari.

2. **Installa le Dipendenze**: Installa le librerie Python richieste, inclusa Flask.

   ```sh
   pip install Flask flask-cors
   ```

## Avvio del Server Flask

1. **Avvia il Server**: Utilizza `app.py` per avviare il server Flask. Assicurati di essere nella directory principale del progetto.

   ```sh
   python app.py
   ```

2. **Verifica il Server**: Il server sarà disponibile all'indirizzo `http://127.0.0.1:5000`. Assicurati che il terminale indichi che il server è in esecuzione in modalità di debug.

## Test del Front-End

1. **Apri la Pagina di Ricerca**: Apri il file `index.html` utilizzando un browser web (è possibile fare doppio clic sul file o aprirlo direttamente dal browser).

2. **Compila il Form di Ricerca**: Inserisci i dettagli richiesti (partenza, destinazione, data, numero di passeggeri) e premi il pulsante "Cerca Voli". I voli disponibili verranno visualizzati dinamicamente nella pagina.

3. **Conferma la Prenotazione**:
   - Dopo aver scelto un volo, premi il pulsante "Prenota". Questo ti reindirizzerà alla pagina `confirm.html`.
   - Inserisci il nome completo, l'email e il numero di telefono per confermare la prenotazione.

4. **Modifica la Prenotazione**:
   - Dopo la conferma, verrai reindirizzato alla pagina `edit.html`, dove puoi aggiornare i dettagli della tua prenotazione o scegliere di cancellarla.

## Note Importanti

- Assicurati che il **server Flask** sia sempre in esecuzione quando interagisci con il front-end, poiché il front-end comunica con il server per tutte le operazioni di ricerca, conferma, modifica, e cancellazione.
- Il progetto utilizza **CORS** (Cross-Origin Resource Sharing) per consentire al front-end di comunicare con il server locale.

## Risoluzione Problemi

- **Errore "Method Not Allowed (405)"**: Assicurati che il metodo HTTP utilizzato sia corretto e che il server sia attivo.
- **Nessuna Risposta dal Server**: Verifica che il server Flask sia in esecuzione e che l'endpoint sia corretto (`http://127.0.0.1:5000`).
- **Problemi di Connessione**: Controlla la configurazione CORS e assicurati che il browser non stia bloccando le richieste.
