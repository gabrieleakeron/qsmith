import streamlit as st

from brokers.components.queues_container import render_queues_container
from brokers.services.data_loader_service import load_brokers


def _get_query_param(name: str) -> str | None:
    value = st.query_params.get(name)
    if isinstance(value, list):
        return value[0] if value else None
    return value


load_brokers()

brokers = st.session_state.get("brokers", [])
if not brokers:
    st.info("No brokers configured.")
    st.stop()

broker_by_id = {broker_item.get("id"): broker_item for broker_item in brokers if broker_item.get("id")}
broker_ids = list(broker_by_id.keys())

query_broker_id = _get_query_param("broker_id")
nav_broker_id = st.session_state.get("nav_broker_id")
if query_broker_id in broker_by_id:
    selected_broker_id = query_broker_id
elif nav_broker_id in broker_by_id:
    selected_broker_id = nav_broker_id
else:
    selected_broker_id = st.session_state.get("queues_filter_broker_id")
    if selected_broker_id not in broker_by_id:
        selected_broker_id = st.session_state.get("selected_broker_id")
    if selected_broker_id not in broker_by_id:
        selected_broker_id = broker_ids[0]

st.session_state["selected_broker_id"] = selected_broker_id
st.session_state["queues_filter_broker_id"] = selected_broker_id

st.subheader("Queues list")
st.divider()

selected_broker_id = render_queues_container(
    brokers=brokers,
    broker_by_id=broker_by_id,
    selected_broker_id=selected_broker_id,
)
st.session_state["selected_broker_id"] = selected_broker_id

st.query_params["broker_id"] = selected_broker_id
