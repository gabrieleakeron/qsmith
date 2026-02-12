import json

import streamlit as st

from brokers.components.common import format_count
from queues.services.queue_service import (
    load_json_arrays,
    save_json_array,
    send_queue_messages,
    test_queue_connection,
)


def _send_body_key(queue_id: str) -> str:
    return f"queue_send_body_{queue_id}"


def _send_results_key(queue_id: str) -> str:
    return f"queue_send_results_{queue_id}"


def _send_write_dialog_open_key(queue_id: str) -> str:
    return f"queue_send_write_open_{queue_id}"


def _send_write_body_key(queue_id: str) -> str:
    return f"queue_send_write_body_{queue_id}"


def _parse_json_array(body_text: str) -> tuple[list[object] | None, str | None]:
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        return None, f"JSON non valido: {str(exc)}"
    if not isinstance(parsed, list):
        return None, "Il body deve contenere un array JSON."
    return parsed, None


def _pretty_json(value: object) -> str:
    return json.dumps(value, indent=2)


def _open_write_json_array_dialog(queue_id: str):
    st.session_state[_send_write_body_key(queue_id)] = st.session_state.get(_send_body_key(queue_id), "[]")
    st.session_state[_send_write_dialog_open_key(queue_id)] = True


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


@st.dialog("Select datasource",width="large")
def queue_select_datasource_dialog(queue_id: str):
    try:
        json_arrays = load_json_arrays()
    except Exception as exc:
        st.error(f"Errore caricamento json-array: {str(exc)}")
        return

    if not json_arrays:
        st.info("Nessun json-array disponibile.")
        return

    options = list(range(len(json_arrays)))
    selected_idx = st.selectbox(
        "Json arrays",
        options=options,
        format_func=lambda idx: json_arrays[idx].get("description") or "-",
        key=f"queue_send_datasource_{queue_id}",
    )
    selected_item = json_arrays[selected_idx]
    st.json(selected_item.get("payload") or [], expanded=False)

    if st.button("Use datasource", key=f"use_queue_send_datasource_{queue_id}"):
        st.session_state[_send_body_key(queue_id)] = _pretty_json(selected_item.get("payload") or [])
        st.rerun()


@st.dialog("Write json-array", width="large")
def queue_write_json_array_dialog(queue_id: str):
    write_body_key = _send_write_body_key(queue_id)
    if write_body_key not in st.session_state:
        st.session_state[write_body_key] = st.session_state.get(_send_body_key(queue_id), "[]")
    st.text_area(
        "Body",
        key=write_body_key,
        height=360,
    )
    action_cols = st.columns([1, 1], gap="small")
    with action_cols[0]:
        if st.button(
            "Beautify",
            key=f"queue_write_beautify_{queue_id}",
            icon=":material/auto_fix_high:",
            use_container_width=True,
        ):
            payload, error = _parse_json_array(st.session_state.get(write_body_key, "[]"))
            if error:
                st.error(error)
            else:
                st.session_state[write_body_key] = _pretty_json(payload)
                st.rerun()
                
    with action_cols[1]:
        if st.button(
            "OK",
            key=f"queue_write_ok_{queue_id}",
            icon=":material/check:",
            use_container_width=True,
        ):
            st.session_state[_send_body_key(queue_id)] = st.session_state.get(write_body_key, "[]")
            st.session_state[_send_write_dialog_open_key(queue_id)] = False
            st.rerun()


@st.dialog("Save json-array")
def queue_save_json_array_dialog(queue_id: str):
    body = st.session_state.get(_send_body_key(queue_id), "[]")
    payload, error = _parse_json_array(body)
    if error:
        st.error(error)
        return

    code = st.text_input("Code", key=f"queue_save_array_code_{queue_id}")
    description = st.text_input("Description", key=f"queue_save_array_description_{queue_id}")
    st.caption("Preview")
    st.json(payload, expanded=False)

    if not st.button("Save", key=f"queue_save_array_submit_{queue_id}"):
        return
    if not code:
        st.error("Il campo Code e' obbligatorio.")
        return

    try:
        save_json_array(code=code, description=description, payload=payload or [])
    except Exception as exc:
        st.error(f"Errore salvataggio json-array: {str(exc)}")
        return

    st.success("Json-array salvato correttamente.")
    st.rerun()

@st.dialog("Results", width="large")
def queue_send_results_dialog(queue_id: str):
    results_key = _send_results_key(queue_id)
    results = st.session_state.get(results_key, [])
    if results:
        st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.caption("Nessun risultato disponibile.")


def render_queue_details_container(queue_data: dict, broker_id: str, queue_id: str):
    
    queue_label = queue_data.get("description") or queue_data.get("code") or queue_id
    st.header(queue_label)

    col_sent, col_received, col_empty, col_test = st.columns([3, 3, 1, 1], gap="small", vertical_alignment="center")

    with col_sent:
        st.metric("Messages sent", format_count(queue_data.get("messages_sent")))
    with col_received:
        st.metric("Messages received", format_count(queue_data.get("messages_received"))) 
    with col_test:
        if st.button(
            "Test connection",
            key=f"queue_test_connection_{queue_id}",
            icon=":material/network_check:",
        ):
            queue_test_connection_dialog(broker_id, queue_id)

    tab_send, tab_receive, tab_ack = st.tabs(
        ["Send", "Receive", "Ack"]
    )

    with tab_send:
        body_key = _send_body_key(queue_id)
        results_key = _send_results_key(queue_id)
        write_open_key = _send_write_dialog_open_key(queue_id)
        if body_key not in st.session_state:
            st.session_state[body_key] = "[]"
        if results_key not in st.session_state:
            st.session_state[results_key] = []
        if write_open_key not in st.session_state:
            st.session_state[write_open_key] = False

        if st.session_state.get(write_open_key):
            queue_write_json_array_dialog(queue_id)

        col_buttons, col_preview, col_send = st.columns([1, 4, 1], gap="small",vertical_alignment="top")
        
        with col_buttons:
            st.caption("Create or import json-array")
            body_text = st.session_state.get(body_key, "[]")
            payload, error = _parse_json_array(body_text)
            body_has_value = body_text.strip() not in ("", "[]")
            if st.button(
                "",
                key=f"queue_send_edit_body_{queue_id}",
                icon=":material/edit:" if body_has_value else ":material/add:",
                help="Edit json-array" if body_has_value else "Create json-array",
                use_container_width=True,
            ):
                _open_write_json_array_dialog(queue_id)
                st.rerun()
            
            if st.button(
                "",
                key=f"queue_send_select_datasource_{queue_id}",
                icon=":material/download:",
                use_container_width=True,
                help="Select json-array from datasource",
            ):
                queue_select_datasource_dialog(queue_id)

            if st.button(
                "",
                key=f"queue_send_save_array_{queue_id}",
                icon=":material/save:",
                use_container_width=True,
                help="Save json-array to datasource",
            ):
                queue_save_json_array_dialog(queue_id)

        with col_preview:
            st.caption("Preview")
            if error:
                st.error(error)
            else:
                st.json(payload, expanded=False)

        with col_send:
            st.caption("Send messages")
            if st.button(
                "",
                key=f"queue_send_messages_{queue_id}",
                icon=":material/send:",
                use_container_width=True,
                help="Send messages to queue",
            ):
                payload, error = _parse_json_array(st.session_state.get(body_key, "[]"))
                if error:
                    st.error(error)
                else:
                    st.session_state[results_key] = []
                    try:
                        with st.spinner("Sending messages..."):
                            results = send_queue_messages(broker_id, queue_id, payload or [])
                    except Exception as exc:
                        st.error(f"Errore invio messaggi: {str(exc)}")
                    else:
                        st.session_state[results_key] = results if isinstance(results, list) else [results]
                        queue_send_results_dialog(queue_id)
            if st.button(
                    "View results",
                    key=f"queue_view_results_{queue_id}",
                    icon=":material/visibility:",
                    use_container_width=True,
                    help="View send results",
                ):
                queue_send_results_dialog(queue_id)
        

    with tab_receive:
        st.info("Tab receive messages pronto per QSM-011.")

    with tab_ack:
        st.info("Tab ack messages pronto per implementazione.")
