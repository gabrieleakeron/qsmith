import os
from datetime import date, datetime

import requests
import streamlit as st


API_BASE_URL = os.getenv("QSMITH_API_BASE_URL", "http://localhost:9082").rstrip("/")


def api_get(path: str):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=8)
    response.raise_for_status()
    return response.json()


def set_status(message: str):
    st.session_state["status"] = message


def render_home():
    st.title("Qsmith")
    st.caption("Brokers and queues manager.")

    col1 = st.columns(2)
    with col1:
        st.subheader("Azioni Rapide")
        st.write("Crea scenari, configura broker o aggiungi sorgenti dati.")


def render_brokers():
    st.header("Brokers & Queues")
    st.caption("Gestione delle connessioni ai broker e configurazione delle code.")

    if st.button("Ricarica Broker"):
        try:
            st.session_state["brokers"] = api_get("/broker/connection")
            set_status("Broker caricati")
        except Exception as exc:
            st.error("Errore caricamento broker")
            set_status(f"Errore broker: {exc}")

    brokers = st.session_state.get("brokers", [])
    broker_labels = [b.get("code", "Senza nome") for b in brokers]
    selected_index = st.selectbox(
        "Seleziona Broker",
        options=list(range(len(broker_labels))),
        format_func=lambda idx: broker_labels[idx],
        index=0 if broker_labels else None,
    )

    broker = brokers[selected_index] if brokers and selected_index is not None else None
    if broker:
        st.json(broker, expanded=False)

    if broker and st.button("Carica Code"):
        try:
            queues = api_get(f"/broker/{broker.get('id')}/queue")
            st.session_state["queues"] = queues
            set_status("Code caricate")
        except Exception as exc:
            st.error("Errore caricamento code")
            set_status(f"Errore code: {exc}")

    queues = st.session_state.get("queues", [])
    if queues:
        st.subheader("Code")
        st.table(
            [
                {
                    "code": q.get("code"),
                    "description": q.get("description"),
                    "id": q.get("id"),
                }
                for q in queues
            ]
        )


def render_datasources():
    st.header("Datasources")
    st.caption("Catalogo sorgenti dati e configurazioni di accesso.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ricarica Database Connections"):
            try:
                st.session_state["db_connections"] = api_get("/database/connection")
                set_status("Database connections caricate")
            except Exception as exc:
                st.error("Errore database connections")
                set_status(f"Errore database: {exc}")
        db_connections = st.session_state.get("db_connections", [])
        if db_connections:
            st.table(
                [
                    {
                        "code": d.get("code"),
                        "description": d.get("description"),
                        "id": d.get("id"),
                    }
                    for d in db_connections
                ]
            )

    with col2:
        if st.button("Ricarica JSON Arrays"):
            try:
                st.session_state["json_arrays"] = api_get("/data-source/json-array")
                set_status("JSON arrays caricati")
            except Exception as exc:
                st.error("Errore JSON arrays")
                set_status(f"Errore JSON arrays: {exc}")
        json_arrays = st.session_state.get("json_arrays", [])
        if json_arrays:
            st.table(
                [
                    {
                        "code": j.get("code"),
                        "description": j.get("description"),
                        "id": j.get("id"),
                    }
                    for j in json_arrays
                ]
            )


def render_tools():
    st.header("Tools")
    st.caption("Utility operative e strumenti di supporto per Qsmith.")
    st.info("Utility operative in arrivo.")


def render_logs():
    st.header("Logs")
    st.caption("Visualizzazione e pulizia dei log applicativi.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Ricarica Logs"):
            try:
                logs = api_get("/logs/")
                st.session_state["logs"] = logs
                set_status("Logs caricati")
            except Exception as exc:
                st.error("Errore logs")
                set_status(f"Errore logs: {exc}")
    with col2:
        days = st.number_input("Cancella log piu vecchi di (giorni)", min_value=1, value=30, step=1)
        if st.button("Pulisci Logs"):
            try:
                api_get(f"/logs/{int(days)}")
                st.session_state["logs"] = []
                st.success("Logs puliti")
                set_status("Logs puliti")
            except Exception as exc:
                st.error("Errore pulizia logs")
                set_status(f"Errore pulizia logs: {exc}")

    logs = st.session_state.get("logs", [])
    if not logs:
        st.info("Nessun log caricato.")
        return

    st.subheader("Filtri")
    levels = sorted({l.get("level") for l in logs if l.get("level")})
    subject_types = sorted({l.get("subject_type") for l in logs if l.get("subject_type")})

    def parse_dt(value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            raw = value.rstrip("Z")
            try:
                return datetime.fromisoformat(raw)
            except ValueError:
                return None
        return None

    parsed_dates = [parse_dt(l.get("created_at")) for l in logs]
    parsed_dates = [d for d in parsed_dates if d is not None]
    min_date = min(parsed_dates).date() if parsed_dates else None
    max_date = max(parsed_dates).date() if parsed_dates else None

    colf1, colf2, colf3, colf4 = st.columns(4)
    with colf1:
        selected_levels = st.multiselect("Livelli", options=levels, default=levels)
    with colf2:
        selected_types = st.multiselect("Subject Type", options=subject_types, default=subject_types)
    with colf3:
        subject_query = st.text_input("Subject contiene")
    with colf4:
        message_query = st.text_input("Messaggio contiene")

    date_range = None
    if min_date and max_date:
        date_range = st.date_input(
            "Intervallo date",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        st.caption("Intervallo date non disponibile: formato data non riconosciuto.")

    def matches(log):
        if selected_levels and log.get("level") not in selected_levels:
            return False
        if selected_types and log.get("subject_type") not in selected_types:
            return False
        if subject_query and subject_query.lower() not in str(log.get("subject", "")).lower():
            return False
        if message_query and message_query.lower() not in str(log.get("message", "")).lower():
            return False
        if date_range and len(date_range) == 2:
            log_dt = parse_dt(log.get("created_at"))
            if log_dt is None:
                return False
            if not (date_range[0] <= log_dt.date() <= date_range[1]):
                return False
        return True

    filtered = [l for l in logs if matches(l)]
    st.caption(f"Log filtrati: {len(filtered)} / {len(logs)}")

    st.dataframe(
        [
            {
                "created_at": l.get("created_at"),
                "level": l.get("level"),
                "subject_type": l.get("subject_type"),
                "subject": l.get("subject"),
                "message": l.get("message"),
            }
            for l in filtered[:500]
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_scenarios():
    st.header("Scenarios")
    st.caption("Definizione e orchestrazione di scenari, step e operazioni.")

    if st.button("Ricarica Scenari"):
        try:
            st.session_state["scenarios"] = api_get("/elaborations/scenario")
            set_status("Scenari caricati")
        except Exception as exc:
            st.error("Errore scenari")
            set_status(f"Errore scenari: {exc}")

    scenarios = st.session_state.get("scenarios", [])
    scenario_labels = [s.get("code", "Senza nome") for s in scenarios]
    selected_index = st.selectbox(
        "Seleziona Scenario",
        options=list(range(len(scenario_labels))),
        format_func=lambda idx: scenario_labels[idx],
        index=0 if scenario_labels else None,
    )

    if scenarios and selected_index is not None:
        scenario = scenarios[selected_index]
        st.json(scenario, expanded=False)
        if st.button("Esegui Scenario"):
            try:
                api_get(f"/elaborations/scenario/{scenario.get('id')}/execute")
                st.success("Scenario avviato")
                set_status("Scenario avviato")
            except Exception as exc:
                st.error("Errore esecuzione scenario")
                set_status(f"Errore scenario: {exc}")


def render_sidebar():
    st.sidebar.title("Qsmith")
    st.sidebar.caption("Control Center")
    st.sidebar.write(f"API: `{API_BASE_URL}`")

    page = st.sidebar.radio(
        "Navigazione",
        options=["Home", "Brokers & Queues", "Datasources", "Tools", "Logs", "Scenarios"],
        label_visibility="collapsed",
    )

    st.sidebar.divider()
    status = st.session_state.get("status", "Pronto.")
    st.sidebar.caption(f"Stato: {status}")
    return page


def main():
    st.set_page_config(page_title="Qsmith UI", layout="wide")
    page = render_sidebar()

    if page == "Home":
        render_home()
    elif page == "Brokers & Queues":
        render_brokers()
    elif page == "Datasources":
        render_datasources()
    elif page == "Tools":
        render_tools()
    elif page == "Logs":
        render_logs()
    elif page == "Scenarios":
        render_scenarios()


if __name__ == "__main__":
    main()
