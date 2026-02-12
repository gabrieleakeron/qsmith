# Qsmith - Contesto Progetto per Codex

**Panoramica**
Qsmith e un backend FastAPI che gestisce configurazioni e orchestrazioni di elaborazioni (scenari, step, operazioni), con integrazione a broker di messaggistica, code e sorgenti dati. Usa PostgreSQL come storage principale e inizializza code ElasticMQ locali per lo sviluppo.

**Stack Tecnologico**
- Python 3.13
- FastAPI, Pydantic
- SQLAlchemy 2 + Alembic
- PostgreSQL
- ElasticMQ (emulatore SQS in locale)
- Docker, Testcontainers
- Streamlit (UI)

**Mappa Repository**
- `app/` codice applicazione FastAPI
- `app/ui/` UI web Streamlit
- `alembic/` migrazioni database
- `elasticmq/` docker-compose e config per ElasticMQ
- `docker/` Dockerfile
- `docs/` documentazione

**Entry Point e Flusso di Avvio**
- `app/main.py`:
  - carica `.env`
  - esegue migrazioni Alembic all avvio
  - inizializza ElasticMQ creando code per i broker `elasticmq`
  - registra router API e handler di eccezioni

**Concetti Chiave (Modello Dati)**
- `json_payloads` config JSON generiche con tipo (`BROKER_CONNECTION`, ecc.)
- `queues` configurazioni code legate a un broker
- `operations` definizioni di operazioni con `operation_type` e configurazione JSON
- `steps` definizioni di step con `step_type` e configurazione JSON
- `scenarios` elenco scenari
- `scenario_steps` collegamento scenario -> step con ordine e policy di errore
- `step_operations` collegamento step -> operazioni con ordine
- `logs` eventi applicativi

**Configurazione Ambiente**
File `.env` (valori di esempio, non usare credenziali reali nei documenti):
```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>
HOST_IP=<host>
```
Nota: l avvio locale non e previsto. Tutto gira via Docker.

**Avvio (Obbligatorio via Docker)**
Avvio solo tramite Docker:
```
docker compose -f docker-compose.yml up --build -d
```
Per fermare:
```
docker compose -f docker-compose.yml down
```
Script alternativo:
```
docker-run-dev.bat
```

**Docker**
- `docker-compose.yml` avvia:
  - `qsmith` (API FastAPI) su `:9082` con debugpy (porta `5678`)
  - `qsmith-ui` (Streamlit) su `:8501`
La UI usa `QSMITH_API_BASE_URL` (default in compose: `http://qsmith:9082`).

**ElasticMQ (SQS locale)**
- `elasticmq/docker-compose.yml`
- Console web: `http://localhost:9325`

**API e Strumenti**
- Swagger: `http://host:port/docs`
- OpenAPI: `http://host:port/openapi.json`
- UI Web (Streamlit): `http://localhost:8501`

**Test**
- `pytest app/test`
- Richiede Docker (Testcontainers avvia PostgreSQL)
