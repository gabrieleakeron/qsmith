import streamlit as st

from brokers.components.dialogs import (
    add_broker_dialog,
    delete_broker_dialog,
    edit_broker_dialog,
)


def select_broker(broker_id: str):
    st.session_state["selected_broker_id"] = broker_id


def render_brokers_container(brokers: list[dict]):
    st.subheader("Brokers list")
    with st.container(border=True):
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
                        on_change=select_broker,
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
                        edit_broker_dialog(broker_item)
                with row_cols[3]:
                    if st.button(
                        "",
                        key=f"delete_broker_btn_{idx}",
                        type="secondary",
                        use_container_width=True,
                        help="Delete broker",
                        icon=":material/delete:",
                    ):
                        delete_broker_dialog(broker_item)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button(
            "Add broker connection",
            key="add_broker_btn",
            help="Add broker",
            use_container_width=True,
            icon=":material/add:",
        ):
            add_broker_dialog()

