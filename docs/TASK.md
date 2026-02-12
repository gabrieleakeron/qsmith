# SurfaceAI - Expense Demo
## Task Breakdown

---

## QSM-007 - Home
- [x] aggiornare l'home con le nuove specifiche

---

## QSM-008 - Brokers&Queues
- [x] il caricamento dei brokers deve avvenire subito
- [x] alla selezione di un broker si devono caricare le code con le info necessarie:
     - numero di messaggi inviati
     - numero di messaggi ricevuti
     - data ultimo aggiornamento
- [x] aggiungere un pulsante di refresh per aggiornare i dati delle code
- [x] aggiunta\modifica broker
- [x] aggiunta\modifica queue  

---

## QSM-009 - Queues
- [x] aggiunta sotto pagina per la gestione della singola coda (Queue)
- [x] aggiungere pulsante per navigare alla pagina
- [x] la pagina � composta da questi tab:
     - [x] test
     - [x] send messages
     - [x] receive messages
     - [x] ack messages

---

## QSM-010 - Test Queue
- [x] nella pagina Queue aggiungere al tab dei test pulsante `test connection` con popup con risultati

---

## QSM-011 - Queue - Send messages 
- [x] nella pagina Queue aggiungere al tab dei send messages una tool bar contenente:
          - un bottone `select datasource` con i json-array
          - un bottone `beautify` per la formattazione dei messaggi
          - un bottone `send messages` per l'invio dei messaggi sulla coda
- [x] nella pagina Queue aggiungere al tab dei send messages due aree di testo:
          - l'area di testo editabile (body) in cui l'utente scriverà l'array di json da inviare come messaggi
          - bottone `save json-array`
          - tabella (results) in cui verranno scritti i risultati dell'invio 
- [x] alla selezione del datasource si apre un popup :
          - a sinistra i vari json-array con le loro descrizioni
          - a destra la preview degli array
- [x] scelto un json-array il body viene svuotato e riempito con l'array e formattato 
- [x] all'invio dei messaggi il results viene svuotato e riempito con i risultati
- [x] alla selezione `beautify` body viene formattato json like
- [x] alla selezione `save json-array` viene richiesto con popup codice e descrizione e viene salvato il json-array

---

## QSM-012 - Queue - Receive messages
- [ ]  nella pagina Queue aggiungere al tab dei receive messages una tool bar contenente:
          - un bottone `receive messages` per la ricezione dei messaggi sulla coda

- [ ] nella pagina Queue aggiungere al tab dei receive messages una area di testo:
          - l'area di testo non editabile (body) in cui verranno scritti i messaggi ricevuti
          - un bottone `copy to clipboard` per la copia dei messaggi ricevuti
          - un bottone `extract json-array` per estrarre il json-array dal body dei messaggi ricevuti
          - un bottone `clean` per pulire il body 
- [ ] alla selezione `receive messages` vengono ricevuti i messaggi dalla coda e il body viene formattato json like 
- [ ] alla selezione `copy to clipboard` il body viene formattato json like e copiato nella clipboard
- [ ] alla selezione `extract json-array` dal body vengono estratti i Body e aperto un dialog con:
          - textfield per code
          - textfield per descrizione
          - preview del json
          - bottone di salva che salva il json array

## QSM-030 - Azioni rapide in Home
- [] crea scenario
- [] aggiungi sorgente dati
- [] aggiungi broker

---



