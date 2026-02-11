import streamlit as st

st.set_page_config(page_title="Qsmith UI", layout="wide")

st.sidebar.title("Qsmith")
st.sidebar.subheader("Brokers and queues manager")


st.markdown(
        """
        <div style="text-align:center;">
            <h3>Azioni Rapide</h3>
            <p>Crea scenari, configura broker o aggiungi sorgenti dati.</p>
        </div>
        """,
        unsafe_allow_html=True,
)