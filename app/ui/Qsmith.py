import streamlit as st

st.set_page_config(page_title="Qsmith UI", layout="wide")

st.sidebar.title("Qsmith")
st.sidebar.subheader("Brokers and queues manager")
st.sidebar.write("Crea scenari, configura broker o aggiungi sorgenti dati.")

brokers = st.Page("pages/2_Brokers.py", title="Brokers")
queues = st.Page("pages/2_Queues.py", title="Queues")
datasources = st.Page("pages/3_datasources.py", title="Data Sources")
scenarios = st.Page("pages/4_scenarios.py", title="Scenarios")
tools = st.Page("pages/5_tools.py", title="Tools")
logs = st.Page("pages/6_logs.py", title="Logs")

pg = st.navigation(
    {
        "Brokers & Queues": [brokers, queues],
        "Data Sources": [datasources],
        "Scenarios": [scenarios],
        "Logs & Tools": [logs, tools]
    }
)

pg.run()