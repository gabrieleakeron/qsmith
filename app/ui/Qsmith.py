import streamlit as st

st.set_page_config(page_title="Qsmith UI", layout="wide")

st.sidebar.title("Qsmith")


brokers = st.Page("pages/2_Brokers.py", title="Brokers")
queues = st.Page("pages/2_Queues.py", title="Queues")
queue_details = st.Page("pages/2_Queue_details.py", title="Queue details")
datasources = st.Page("pages/3_datasources.py", title="Data Sources")
scenarios = st.Page("pages/4_scenarios.py", title="Scenarios")
tools = st.Page("pages/5_tools.py", title="Tools")
logs = st.Page("pages/6_logs.py", title="Logs")

st.sidebar.subheader("Brokers & Queues")
st.sidebar.page_link(brokers, label="Brokers")
st.sidebar.page_link(queues, label="Queues")
st.sidebar.subheader("Datasources")
st.sidebar.page_link(datasources, label="Data Sources")
st.sidebar.subheader("Scenarios")
st.sidebar.page_link(scenarios, label="Scenarios")
st.sidebar.subheader("Logs & Tools")
st.sidebar.page_link(logs, label="Logs")
st.sidebar.page_link(tools, label="Tools")

st.sidebar.divider()
st.sidebar.subheader("Quick actions")
st.sidebar.write("Create scenarios, configure brokers, or add data sources.")

pg = st.navigation(
    {
        "Brokers & Queues": [brokers, queues, queue_details],
        "Data Sources": [datasources],
        "Scenarios": [scenarios],
        "Logs & Tools": [logs, tools]
    },
    position="hidden",
)

pg.run()
