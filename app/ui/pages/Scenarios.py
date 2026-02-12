import streamlit as st

from api_client import api_get


st.header("Scenarios")
st.caption("Definizione e orchestrazione di scenari, step e operazioni.")

if st.button("Ricarica Scenari"):
    try:
        st.session_state["scenarios"] = api_get("/elaborations/scenario")

    except Exception as exc:
        st.error("Errore scenari")

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
        except Exception as exc:
            st.error("Errore esecuzione scenario")
