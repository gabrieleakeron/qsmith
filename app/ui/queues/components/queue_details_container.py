import streamlit as st

from brokers.components.common import format_count


def render_queue_details_container(queue_data: dict, queue_id: str):
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
