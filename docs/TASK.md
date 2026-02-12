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
- [x] la pagina Queues deve mostrare i dati del broker selezionato (`broker_id`)
- [x] la pagina e' composta da questi tab:
     - [x] test
     - [x] send messages
     - [x] receive messages
     - [x] ack messages

---

## QSM-010 - Test Queue
- [x] nella pagina Queue aggiungere al tab dei test pulsante `test connection` con popup con risultati

---

## QSM-011 - Queue - Send messages
- [x] nel tab Send la UI e' strutturata in 3 colonne:
     - colonna sinistra: azioni su json-array (`create/edit`, `select datasource`, `save json-array`)
     - colonna centrale: preview non editabile del body in formato json
     - colonna destra: invio messaggi e apertura risultati
- [x] `create/edit` apre un dialog `Write json-array` con:
     - area di testo `body`
     - bottone `beautify`
     - bottone `OK` per confermare e chiudere
- [x] `select datasource` apre un dialog con:
     - selectbox con descrizioni dei json-array
     - preview del payload selezionato
     - bottone `use datasource` che aggiorna il body
- [x] `save json-array` apre un dialog con:
     - textfield `code`
     - textfield `description`
     - preview del payload
     - bottone `save` per salvare in datasource
- [x] `send messages` invia l'array JSON sulla queue e aggiorna i risultati visualizzabili in dialog

---

## QSM-012 - Queue - Receive messages
- [x] nel tab Receive la UI e' strutturata in 3 colonne:
     - colonna di sinistra: bottone `receive messages`
     - colonna centrale: preview JSON non editabile dei messaggi ricevuti
     - colonna di destra: bottoni `ack messages`, `extract json-array` e `clean`
- [x] alla selezione `receive messages` vengono ricevuti i messaggi dalla queue e la preview viene valorizzata
- [x] alla selezione `extract json-array` dal body di ogni messaggio vengono estratti i dati e si apre un dialog per salvarli:
     - textfield `code`
     - textfield `description`
     - preview del json-array estratto
     - bottone `save` che salva il json-array

## QSM-013 - Queue - Ack messages
- [x] aggiunto bottone `ack messages` nella colonna azioni del tab Receive
- [x] invio payload `messages` a endpoint `PUT /broker/{broker_id}/queue/{queue_id}/messages`
- [x] fix endpoint backend per leggere `QueueMessagesDto` da body JSON
- [x] dopo ack riuscito la preview dei messaggi viene pulita

---

## QSM-014 - Queue metrics refresh
- [x] dopo `send messages` i dati queue (numero messaggi) vengono aggiornati
- [x] dopo `receive messages` i dati queue (numero messaggi) vengono aggiornati
- [x] aggiunto bottone `refresh` accanto a `test connection` nella pagina dettaglio queue

---

## QSM-015 - UI navigation refactor
- [x] rinominati i file sotto `app/ui/pages` rimuovendo il prefisso numerico
- [x] aggiornata la navigazione sidebar con bottoni per tutte le pagine principali

## QSM-030 - Azioni rapide in Home
- [] crea scenario
- [] aggiungi sorgente dati
- [] aggiungi broker

---
