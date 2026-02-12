import streamlit as st

from brokers.components.common import format_count, format_last_update
from brokers.components.dialogs import (
    add_queue_dialog,
    delete_queue_dialog,
    queue_settings_dialog,
)
from brokers.services.data_loader_service import load_queues


def _open_queue_page(broker_id: str | None, queue_id: str | None):
    if not broker_id or not queue_id:
        st.error("Impossibile aprire il dettaglio della queue.")
        return
    st.session_state["selected_broker_id"] = broker_id
    st.session_state["nav_broker_id"] = broker_id
    st.session_state["nav_queue_id"] = queue_id
    st.switch_page("queues/components/queue_details.py")


def render_queues_container(
    brokers: list[dict],
    broker_by_id: dict[str, dict],
    selected_broker_id: str | None,
) -> str | None:
    broker_ids = [broker_item.get("id") for broker_item in brokers if broker_item.get("id")]
    if not broker_ids:
        st.info("Nessun broker configurato.")
        return None

    bar_cols = st.columns([3, 3, 1, 1], gap="small", vertical_alignment="center")
    with bar_cols[0]:
        selected_broker_id = st.selectbox(
            "Broker",
            options=broker_ids,
            format_func=lambda broker_id: broker_by_id[broker_id].get("description")
            or broker_by_id[broker_id].get("code")
            or broker_id,
            key="queues_filter_broker_id",
            label_visibility="collapsed",
        )

    broker = broker_by_id.get(selected_broker_id)
    if broker:
        load_queues(broker.get("id"))
        queues = st.session_state.get("queues", [])
    else:
        queues = []

    with bar_cols[2]:
        st.button(
            "",
            key="refresh_queues_btn",
            on_click=lambda: load_queues(selected_broker_id, force=True),
            use_container_width=True,
            icon=":material/refresh:",
        )
    with bar_cols[3]:
        if st.button(
            "",
            key="add_queue_btn",
            use_container_width=True,
            disabled=not bool(broker),
            icon=":material/add:",
        ):
            add_queue_dialog(broker)

    if not queues:
        st.info("Nessuna queue configurata.")
    else:
        for queue_item in queues:
            with st.container(border=True):
                row_cols = st.columns([4, 2, 2, 1, 1, 1], gap="small", vertical_alignment="center")
                queue_label = queue_item.get("description") or queue_item.get("code") or "-"
                row_cols[0].write(queue_label)
                with row_cols[1]:
                    st.write("Sent: " + format_count(queue_item.get("messages_sent")))
                with row_cols[2]:
                    st.write("Received: " + format_count(queue_item.get("messages_received")))
                with row_cols[3]:
                    if st.button(
                        "",
                        key=f"queue_open_{queue_item.get('id')}",
                        type="secondary",
                        use_container_width=True,
                        help="Open queue page",
                        icon=":material/open_in_new:",
                    ):
                        _open_queue_page(selected_broker_id, queue_item.get("id"))
                with row_cols[4]:
                    if st.button(
                        "",
                        key=f"queue_settings_{queue_item.get('id')}",
                        type="secondary",
                        use_container_width=True,
                        help="Settings",
                        icon=":material/settings:",
                    ):
                        queue_settings_dialog(selected_broker_id, queue_item.get("id"))
                with row_cols[5]:
                    if st.button(
                        "",
                        key=f"queue_delete_{queue_item.get('id')}",
                        type="secondary",
                        use_container_width=True,
                        help="Delete",
                        icon=":material/delete:",
                    ):
                        delete_queue_dialog(selected_broker_id, queue_item)

    loaded_at = st.session_state.get("queues_loaded_at")
    timestamp_label = format_last_update(loaded_at) if loaded_at else "-"
    footer_cols = st.columns([2, 1], gap="small", vertical_alignment="center")
    with footer_cols[1]:
        st.caption(f"Updated at: {timestamp_label}")

    return selected_broker_id
