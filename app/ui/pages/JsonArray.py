import streamlit as st

from json_arrays.components.json_arrays_container import render_json_arrays_container
from json_arrays.services.data_loader_service import load_json_arrays

load_json_arrays()

st.subheader("Json arrays list")
st.caption("Configure JSON array data sources to use them in queues or in scenarios.")
st.divider()

json_arrays = st.session_state.get("json_arrays", [])
render_json_arrays_container(json_arrays if isinstance(json_arrays, list) else [])
