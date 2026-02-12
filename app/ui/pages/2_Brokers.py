import streamlit as st

from brokers.components.brokers_container import render_brokers_container
from brokers.components.queues_container import render_queues_container
from brokers.services.data_loader_service import load_brokers

load_brokers()

brokers = st.session_state.get("brokers", [])
if not brokers:
    st.info("No brokers configured.")

broker_ids = [broker_item.get("id") for broker_item in brokers] if brokers else []
if brokers:
    if (
        "selected_broker_id" not in st.session_state
        or st.session_state["selected_broker_id"] not in broker_ids
    ):
        st.session_state["selected_broker_id"] = broker_ids[0]
else:
    st.session_state["selected_broker_id"] = None

col_left, col_right = st.columns([1, 4], gap="medium")

with col_left:
    render_brokers_container(brokers)

selected_broker_id = st.session_state.get("selected_broker_id")
broker = next((item for item in brokers if item.get("id") == selected_broker_id), None)

with col_right:
    render_queues_container(broker, selected_broker_id)
