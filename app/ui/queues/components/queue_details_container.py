import streamlit as st

from brokers.components.common import format_count
from queues.services.queue_service import test_queue_connection


@st.dialog("Test connection")
def queue_test_connection_dialog(broker_id: str, queue_id: str):
    try:
        with st.spinner("Testing connection..."):
            result = test_queue_connection(broker_id, queue_id)
    except Exception as exc:
        st.error(f"Errore test connessione: {str(exc)}")
        return

    message = str(result.get("message", "Test completato."))
    if "not valid" in message.lower():
        st.error(message)
    else:
        st.success(message)
    st.json(result)


def render_queue_details_container(queue_data: dict, broker_id: str, queue_id: str):
    queue_label = queue_data.get("description") or queue_data.get("code") or queue_id
    st.header(queue_label)

    summary_cols = st.columns(2)
    summary_cols[0].metric("Messages sent", format_count(queue_data.get("messages_sent")))
    summary_cols[1].metric("Messages received", format_count(queue_data.get("messages_received")))

    tab_test, tab_send, tab_receive, tab_ack = st.tabs(
        ["test", "send messages", "receive messages", "ack messages"]
    )

    with tab_test:
        st.write("Verifica la connessione della queue e visualizza il risultato nel popup.")
        if st.button(
            "Test connection",
            key=f"queue_test_connection_{queue_id}",
            icon=":material/network_check:",
        ):
            queue_test_connection_dialog(broker_id, queue_id)

    with tab_send:
        st.info("Tab send messages pronto per implementazione.")

    with tab_receive:
        st.info("Tab receive messages pronto per QSM-011.")

    with tab_ack:
        st.info("Tab ack messages pronto per implementazione.")
