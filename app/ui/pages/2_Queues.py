import streamlit as st

from api_client import api_get
from brokers.components.common import format_count


def _get_query_param(name: str) -> str | None:
    value = st.query_params.get(name)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _load_queue_data(broker_id: str, queue_id: str) -> dict | None:
    try:
        queues = api_get(f"/broker/{broker_id}/queue")
        queue_item = next((item for item in queues if item.get("id") == queue_id), None)
        if queue_item:
            return queue_item
        queue_item = api_get(f"/broker/{broker_id}/queue/{queue_id}")
        queue_item["messages_sent"] = None
        queue_item["messages_received"] = None
        return queue_item
    except Exception:
        return None

st.sidebar.title("Queue")

if st.button("Back to Brokers", icon=":material/arrow_back:"):
    st.switch_page("pages/2_Brokers.py")

broker_id = _get_query_param("broker_id")
queue_id = _get_query_param("queue_id")

if not broker_id or not queue_id:
    st.error("Queue non selezionata. Apri questa pagina dalla lista queue in Brokers.")
    st.stop()

queue_data = _load_queue_data(broker_id, queue_id)
if not queue_data:
    st.error("Errore caricamento dettaglio queue.")
    st.stop()

queue_label = queue_data.get("description") or queue_data.get("code") or queue_id
st.header(queue_label)

summary_cols = st.columns(2)
summary_cols[0].metric("Messages sent", format_count(queue_data.get("messages_sent")))
summary_cols[1].metric("Messages received", format_count(queue_data.get("messages_received")))

tab_test, tab_send, tab_receive, tab_ack = st.tabs(
    ["test", "send messages", "receive messages", "ack messages"]
)

with tab_test:
    st.info("Tab test pronto per QSM-010.")

with tab_send:
    st.info("Tab send messages pronto per implementazione.")

with tab_receive:
    st.info("Tab receive messages pronto per QSM-011.")

with tab_ack:
    st.info("Tab ack messages pronto per implementazione.")

