# Qsmith - Istruzioni Operative per Codex

Leggi prima `docs/CODEX_CONTEXT.md` per contesto e comandi principali.

**Regole di Lavoro**
- Evita di inserire segreti o credenziali reali nei file del repo.
- Se tocchi i modelli SQLAlchemy in `app/_alembic/models`, aggiorna le migrazioni in `alembic/`.
- Per ricerche nel repo preferisci `rg` (ripgrep).
- Mantieni la logica di fetch API concentrata nei service per facilitare test e riuso.
- In UI, se possibile estrai componenti in file separati e organizzali per package (esempio: `brokers.components`).
- Le chiamate API per le queue devono stare in servizi dedicati (`queues.services.queue_service`).
- Quando identifichi una modifica strutturale o in generale quando e necessario, chiedi sempre di aggiornare questo file.
- Prima di iniziare una modifica, leggi sempre `SPEC.md` per analisi funzionale e `TASK.md` come piano di lavoro.
- Se una modifica impatta specifiche o piano di lavoro, chiedi sempre di aggiornare `SPEC.md` e/o `TASK.md` e/o `README.md` e\o `CODEX_CONTEXT.md`

**Esecuzione e Test**
- Avvio obbligatorio via Docker:
```
docker compose -f docker-compose.yml up --build -d
```
- UI Streamlit via Docker: usa lo stesso `docker-compose.yml` (porta `8501`)
  - Base URL configurata con `QSMITH_API_BASE_URL`
- Test:
```
pytest app/test
```
I test usano Docker (Testcontainers per PostgreSQL).

**Punti di Ingresso**
- API principale: `app/main.py`
- UI Streamlit: `app/ui/app.py`
- Migrazioni: `alembic/`
