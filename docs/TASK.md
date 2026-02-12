# Qsmith - Task Breakdown

## Stato generale
- [x] Baseline UI multipage Streamlit configurata
- [x] Baseline API FastAPI configurata
- [x] Avvio stack via `docker-compose.yml`

---

## QSM-008 - Brokers & Queues
- [x] Caricamento brokers all'avvio UI
- [x] Visualizzazione queue per broker selezionato
- [x] Metriche queue (messages sent/received + last update)
- [x] Refresh lista queue
- [x] CRUD broker connection
- [x] CRUD queue
- [x] Navigazione a `Queue details`

---

## QSM-009 - Queue details
- [x] Pagina dedicata gestione singola queue
- [x] Context sync (`broker_id`, `queue_id`) via stato/query params
- [x] Header con metriche queue + azioni refresh/test
- [x] Tab `Send`
- [x] Tab `Receive`

---

## QSM-011 - Queue Send
- [x] Layout 3 colonne (azioni / preview / send)
- [x] Dialog `Write json-array` (body, beautify, conferma)
- [x] Dialog `Select datasource` con preview payload
- [x] Dialog `Save json-array` in datasource
- [x] Invio messaggi a queue
- [x] Dialog risultati invio

---

## QSM-012 - Queue Receive
- [x] Ricezione messaggi
- [x] Preview JSON messaggi ricevuti
- [x] Ack messaggi ricevuti (`PUT /broker/{broker_id}/queue/{queue_id}/messages`)
- [x] Extract json-array da messaggi ricevuti
- [x] Salvataggio extracted json-array in datasource
- [x] Pulizia preview

---

## QSM-016 - Json array datasources
- [x] Pagina elenco json-array
- [x] CRUD json-array
- [x] Integrazione json-array con flussi queue send/receive

---

## QSM-020 - Scenarios
- [x] Pagina scenarios
- [x] Caricamento elenco scenari
- [x] Esecuzione scenario selezionato
- [ ] Gestione completa CRUD scenari/step/operations da UI

---

## QSM-021 - Logs
- [x] Pagina logs
- [x] Ricarica elenco logs
- [x] Filtri lato UI (livello, tipo, subject, messaggio, data)
- [x] Pulizia log vecchi (`DELETE /logs/{days}`)

---

## QSM-030 - Home & Quick Actions
- [ ] Home page dedicata
- [ ] Quick action: crea scenario
- [ ] Quick action: aggiungi sorgente dati
- [ ] Quick action: aggiungi broker

---

## QSM-040 - Tools
- [x] Pagina `Tools` placeholder
- [ ] Utility operative reali da definire

---

## QSM-050 - Documentazione
- [x] Riallineamento `README.md` alla codebase
- [x] Riallineamento `AGENT.md` ai path reali
- [x] Riallineamento `docs/CODEX_CONTEXT.md`
- [x] Aggiornamento `docs/SPEC.md`
- [ ] Stesura documentazione funzionale su Confluence
