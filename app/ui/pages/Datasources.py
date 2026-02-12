import streamlit as st

from api_client import api_get


st.header("Datasources")
st.caption("Catalogo sorgenti dati e configurazioni di accesso.")

col1, col2 = st.columns(2)
with col1:
    if st.button("Ricarica Database Connections"):
        try:
            st.session_state["db_connections"] = api_get("/database/connection")
        except Exception as exc:
            st.error("Errore database connections")
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
        except Exception as exc:
            st.error("Errore JSON arrays")
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
