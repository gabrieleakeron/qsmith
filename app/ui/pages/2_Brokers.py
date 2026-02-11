from datetime import datetime

import streamlit as st

from api_client import api_delete, api_get, api_post, api_put


def _load_brokers(force: bool = False):
    if force or "brokers" not in st.session_state:
        try:
            st.session_state["brokers"] = api_get("/broker/connection")
        except Exception as exc:
            st.session_state["brokers"] = []
            st.error("Errore caricamento broker")


def _load_queues(broker_id: str, force: bool = False):
    if not broker_id:
        return
    if force or st.session_state.get("queues_for_broker_id") != broker_id:
        try:
            queues = api_get(f"/broker/{broker_id}/queue")
            st.session_state["queues"] = queues
            st.session_state["queues_for_broker_id"] = broker_id
            st.session_state["queues_loaded_at"] = datetime.now()
        except Exception as exc:
            st.session_state["queues"] = []
            st.error("Errore caricamento code")

def _format_count(value):
    if isinstance(value, int):
        return str(value)
    return value if value is not None else "-"


def _format_last_update(value):
    if not value:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", ""))
        except ValueError:
            return value
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)


BROKER_TYPE_OPTIONS = {
    "Elasticmq": "elasticmq",
    "Amazon": "amazon-sqs",
}
BROKER_TYPE_LABELS = {value: label for label, value in BROKER_TYPE_OPTIONS.items()}


def _pick_broker_type_label(source_type: str | None) -> str:
    return BROKER_TYPE_LABELS.get(source_type or "", "Elasticmq")


def _select_broker(broker_id: str):
    st.session_state["selected_broker_id"] = broker_id


@st.dialog("Aggiungi broker")
def _add_broker_dialog():
    code = st.text_input("Code", key="add_broker_code")
    description = st.text_input("Description", key="add_broker_description")
    broker_type_label = st.selectbox(
        "Type",
        options=list(BROKER_TYPE_OPTIONS.keys()),
        key="add_broker_type",
    )
    endpoint_url = st.text_input("Endpoint url", key="add_broker_endpoint")
    region = None
    secrets_access_key = None
    access_key_id = None
    if broker_type_label == "Amazon":
        region = st.text_input("Region", key="add_broker_region")
        secrets_access_key = st.text_input(
            "Secrets access key",
            type="password",
            key="add_broker_secret",
        )
        access_key_id = st.text_input("Access key id", key="add_broker_access")

    if not st.button("Salva", key="add_broker_save"):
        return

    errors = []
    if not code:
        errors.append("Il campo Code e' obbligatorio.")
    if not endpoint_url:
        errors.append("Il campo Endpoint url e' obbligatorio.")
    if broker_type_label == "Amazon":
        if not region:
            errors.append("Il campo Region e' obbligatorio per Amazon.")
        if not secrets_access_key:
            errors.append("Il campo Secrets access key e' obbligatorio per Amazon.")
        if not access_key_id:
            errors.append("Il campo Access key id e' obbligatorio per Amazon.")

    if errors:
        st.error(" ".join(errors))
        return

    payload = {
        "sourceType": BROKER_TYPE_OPTIONS[broker_type_label],
        "endpointUrl": endpoint_url,
    }
    if broker_type_label == "Amazon":
        payload.update(
            {
                "region": region,
                "secretsAccessKey": secrets_access_key,
                "accessKeyId": access_key_id,
            }
        )

    try:
        response = api_post(
            "/broker/connection",
            {
                "code": code,
                "description": description,
                "payload": payload,
            },
        )
    except Exception:
        st.error("Errore salvataggio broker")
        return

    _load_brokers(force=True)
    new_id = response.get("id")
    if new_id:
        st.session_state["selected_broker_id"] = new_id
    st.rerun()


@st.dialog("Modifica broker")
def _edit_broker_dialog(broker_item: dict):
    broker_id = broker_item.get("id", "")
    payload = broker_item.get("payload") or {}
    code = st.text_input("Code", value=broker_item.get("code", ""), key=f"edit_code_{broker_id}")
    description = st.text_input(
        "Description",
        value=broker_item.get("description", ""),
        key=f"edit_description_{broker_id}",
    )
    broker_type_label = st.selectbox(
        "Type",
        options=list(BROKER_TYPE_OPTIONS.keys()),
        index=list(BROKER_TYPE_OPTIONS.keys()).index(_pick_broker_type_label(payload.get("sourceType"))),
        key=f"edit_type_{broker_id}",
    )
    endpoint_url = st.text_input(
        "Endpoint url",
        value=payload.get("endpointUrl", ""),
        key=f"edit_endpoint_{broker_id}",
    )
    region = None
    secrets_access_key = None
    access_key_id = None
    if broker_type_label == "Amazon":
        region = st.text_input(
            "Region",
            value=payload.get("region", ""),
            key=f"edit_region_{broker_id}",
        )
        secrets_access_key = st.text_input(
            "Secrets access key",
            type="password",
            value=payload.get("secretsAccessKey", ""),
            key=f"edit_secret_{broker_id}",
        )
        access_key_id = st.text_input(
            "Access key id",
            value=payload.get("accessKeyId", ""),
            key=f"edit_access_{broker_id}",
        )

    if not st.button("Salva modifiche", key=f"edit_save_{broker_id}"):
        return

    errors = []
    if not code:
        errors.append("Il campo Code e' obbligatorio.")
    if not endpoint_url:
        errors.append("Il campo Endpoint url e' obbligatorio.")
    if broker_type_label == "Amazon":
        if not region:
            errors.append("Il campo Region e' obbligatorio per Amazon.")
        if not secrets_access_key:
            errors.append("Il campo Secrets access key e' obbligatorio per Amazon.")
        if not access_key_id:
            errors.append("Il campo Access key id e' obbligatorio per Amazon.")

    if errors:
        st.error(" ".join(errors))
        return

    payload = {
        "sourceType": BROKER_TYPE_OPTIONS[broker_type_label],
        "endpointUrl": endpoint_url,
    }
    if broker_type_label == "Amazon":
        payload.update(
            {
                "region": region,
                "secretsAccessKey": secrets_access_key,
                "accessKeyId": access_key_id,
            }
        )

    try:
        api_put(
            "/broker/connection",
            {
                "id": broker_id,
                "code": code,
                "description": description,
                "payload": payload,
            },
        )
    except Exception:
        st.error("Errore aggiornamento broker")
        return

    _load_brokers(force=True)
    st.session_state["selected_broker_id"] = broker_id
    st.rerun()


@st.dialog("Conferma eliminazione")
def _delete_broker_dialog(broker_item: dict):
    broker_id = broker_item.get("id", "")
    broker_description = broker_item.get("description", "No name")
    st.write(f"Eliminare il broker '{broker_description}'?")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("Conferma", key=f"delete_confirm_{broker_id}"):
            try:
                api_delete(f"/broker/connection/{broker_id}")
            except Exception:
                st.error("Errore cancellazione broker")
                return

            _load_brokers(force=True)
            brokers_local = st.session_state.get("brokers", [])
            if brokers_local:
                st.session_state["selected_broker_id"] = brokers_local[0].get("id")
            else:
                st.session_state["selected_broker_id"] = None
            st.rerun()
    with col_cancel:
        st.button("Annulla", key=f"delete_cancel_{broker_id}")


@st.dialog("Aggiungi queue")
def _add_queue_dialog(broker_item: dict):
    broker_id = broker_item.get("id", "")
    broker_payload = broker_item.get("payload") or {}
    source_type = broker_payload.get("sourceType", "elasticmq")
    type_label = _pick_broker_type_label(source_type)

    code = st.text_input("Code", key=f"add_queue_code_{broker_id}")
    description = st.text_input("Description", key=f"add_queue_description_{broker_id}")
    st.text_input("Type", value=type_label, disabled=True, key=f"add_queue_type_{broker_id}")
    default_visibility = st.number_input(
        "Default visibility timeout (sec)",
        min_value=0,
        step=1,
        value=30,
        key=f"add_queue_visibility_{broker_id}",
    )
    receive_wait = st.number_input(
        "Receive message wait (sec)",
        min_value=0,
        step=1,
        value=0,
        key=f"add_queue_wait_{broker_id}",
    )

    fifo_queue = False
    content_based = False
    delay = 0
    if source_type == "elasticmq":
        fifo_queue = st.checkbox("FIFO queue", value=False, key=f"add_queue_fifo_{broker_id}")
        content_based = st.checkbox(
            "Content based deduplication",
            value=False,
            key=f"add_queue_dedupe_{broker_id}",
        )
        delay = st.number_input(
            "Delay (sec)",
            min_value=0,
            step=1,
            value=0,
            key=f"add_queue_delay_{broker_id}",
        )

    if not st.button("Salva", key=f"add_queue_save_{broker_id}"):
        return

    errors = []
    if not code:
        errors.append("Il campo Code e' obbligatorio.")
    if errors:
        st.error(" ".join(errors))
        return

    queue_config = {
        "sourceType": source_type,
        "defaultVisibilityTimeout": int(default_visibility),
        "receiveMessageWait": int(receive_wait),
    }
    if source_type == "elasticmq":
        queue_config.update(
            {
                "fifoQueue": fifo_queue,
                "contentBasedDeduplication": content_based,
                "delay": int(delay),
            }
        )

    try:
        api_post(
            f"/broker/{broker_id}/queue",
            {
                "code": code,
                "description": description,
                "queueConfiguration": queue_config,
                "save_on_db": True,
            },
        )
    except Exception:
        st.error("Errore salvataggio queue")
        return

    _load_queues(broker_id, force=True)
    st.rerun()


@st.dialog("Impostazioni queue")
def _queue_settings_dialog(broker_id: str, queue_id: str):
    try:
        queue = api_get(f"/broker/{broker_id}/queue/{queue_id}")
    except Exception:
        st.error("Errore caricamento queue")
        return

    config = queue.get("configurationQueue") or {}
    source_type = config.get("sourceType", "elasticmq")
    type_label = _pick_broker_type_label(source_type)

    st.text_input("Code", value=queue.get("code", ""), disabled=True, key=f"settings_code_{queue_id}")
    st.text_input(
        "Description",
        value=queue.get("description", ""),
        disabled=True,
        key=f"settings_description_{queue_id}",
    )
    st.text_input("Type", value=type_label, disabled=True, key=f"settings_type_{queue_id}")
    st.text_input(
        "URL",
        value=config.get("url", ""),
        disabled=True,
        key=f"settings_url_{queue_id}",
    )
    st.text_input(
        "Default visibility timeout (sec)",
        value=str(config.get("defaultVisibilityTimeout", "")),
        disabled=True,
        key=f"settings_visibility_{queue_id}",
    )
    st.text_input(
        "Receive message wait (sec)",
        value=str(config.get("receiveMessageWait", "")),
        disabled=True,
        key=f"settings_wait_{queue_id}",
    )
    if source_type == "elasticmq":
        st.text_input(
            "FIFO queue",
            value=str(config.get("fifoQueue", False)),
            disabled=True,
            key=f"settings_fifo_{queue_id}",
        )
        st.text_input(
            "Content based deduplication",
            value=str(config.get("contentBasedDeduplication", False)),
            disabled=True,
            key=f"settings_dedupe_{queue_id}",
        )
        st.text_input(
            "Delay (sec)",
            value=str(config.get("delay", 0)),
            disabled=True,
            key=f"settings_delay_{queue_id}",
        )


@st.dialog("Conferma eliminazione queue")
def _delete_queue_dialog(broker_id: str, queue_item: dict):
    queue_id = queue_item.get("id", "")
    queue_label = queue_item.get("description") or queue_item.get("code") or queue_id
    st.write(f"Eliminare la queue '{queue_label}'?")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("Conferma", key=f"delete_queue_confirm_{queue_id}"):
            try:
                api_delete(f"/broker/{broker_id}/queue/{queue_id}")
            except Exception:
                st.error("Errore cancellazione queue")
                return

            _load_queues(broker_id, force=True)
            st.rerun()
    with col_cancel:
        st.button("Annulla", key=f"delete_queue_cancel_{queue_id}")


st.set_page_config(page_title="Brokers & Queues", page_icon="📡", layout="wide")
st.sidebar.title("Brokers & Queues")

_load_brokers()

st.markdown(
    """
<style>
#brokers-list [data-testid="stCheckbox"] {
    display: flex;
    align-items: center;
    height: 100%;
    min-height: 2.5rem;
}
#brokers-list [data-testid="stCheckbox"] > label {
    margin: 0 !important;
    padding: 0 !important;
    align-items: center;
    height: 100%;
}
#brokers-list [data-testid="stCheckbox"] row-widget {
    margin-top: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

brokers = st.session_state.get("brokers", [])
if not brokers:
    st.info("No brokers configured.")

broker_ids = [b.get("id") for b in brokers] if brokers else []
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
    st.subheader("Brokers")

    st.markdown('<div id="brokers-list">', unsafe_allow_html=True)
    for idx, broker_item in enumerate(brokers):
        broker_id = broker_item.get("id")
        broker_description = broker_item.get("description", "No name")
        is_selected = broker_id == st.session_state.get("selected_broker_id")
        with st.container(border=True):
            row_cols = st.columns([2, 6, 3, 3], gap="small", vertical_alignment="center")
            with row_cols[0]:
                select_key = f"broker_select_{broker_id or idx}"
                st.session_state[select_key] = is_selected
                st.checkbox(
                    "",
                    key=select_key,
                    on_change=_select_broker,
                    args=(broker_id,),
                    label_visibility="hidden",
                )
            with row_cols[1]:
                st.write(broker_description)
            with row_cols[2]:
                if st.button(
                    "",
                    key=f"edit_broker_btn_{idx}",
                    type="secondary",
                    use_container_width=True,
                    help="Edit broker",
                    icon=":material/settings:",
                ):
                    _edit_broker_dialog(broker_item)
            with row_cols[3]:
                if st.button(
                    "",
                    key=f"delete_broker_btn_{idx}",
                    type="secondary",
                    use_container_width=True,
                    help="Delete broker",
                    icon=":material/delete:",
                ):
                    _delete_broker_dialog(broker_item)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Add broker connection", key="add_broker_btn", help="Add broker", use_container_width=True, icon=":material/add:"):
        _add_broker_dialog()

selected_broker_id = st.session_state.get("selected_broker_id")
broker = next((b for b in brokers if b.get("id") == selected_broker_id), None)

with col_right:
    if broker:
        _load_queues(broker.get("id"))
        queues = st.session_state.get("queues", [])
    else:
        queues = []

    col_subHeader, col_refresh, col_add = st.columns([2, 1, 1], gap="large")
    with col_subHeader:
        st.subheader("Queues")
    with col_refresh:
        st.button(
            "Refresh",
            key="refresh_queues_btn",
            on_click=lambda: _load_queues(selected_broker_id, force=True),
            use_container_width=True,
            icon=":material/refresh:",
        )
    with col_add:
        if st.button(
            "Add queue",
            key="add_queue_btn",
            use_container_width=True,
            disabled=not bool(broker),
            icon=":material/add:",
        ):
            _add_queue_dialog(broker)

    if not queues:
        st.info("Nessuna queue configurata.")
    else:
        for q in queues:
            with st.container(border=True):
                row_cols = st.columns([4, 2, 2, 1, 1], gap="small", vertical_alignment="center")
                queue_label = q.get("description") or q.get("code") or "-"
                row_cols[0].write(queue_label)
                with row_cols[1]:
                    st.write("Messages sent: "+_format_count(q.get("messages_sent")))
                with row_cols[2]:
                    st.write("Messages received: "+_format_count(q.get("messages_received")))
                with row_cols[3]:
                    if st.button(
                        "",
                        key=f"queue_settings_{q.get('id')}",
                        type="secondary",
                        use_container_width=True,
                        help="Settings",
                        icon=":material/settings:",
                    ):
                        _queue_settings_dialog(selected_broker_id, q.get("id"))
                with row_cols[4]:
                    if st.button(
                        "",
                        key=f"queue_delete_{q.get('id')}",
                        type="secondary",
                        use_container_width=True,
                        help="Delete",
                        icon=":material/delete:",
                    ):
                        _delete_queue_dialog(selected_broker_id, q)
     
    loaded_at = st.session_state.get("queues_loaded_at")
    timestamp_label = _format_last_update(loaded_at) if loaded_at else "-"
    st.caption(f"Aggiornate: {timestamp_label}")


   
