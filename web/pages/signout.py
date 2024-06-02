import streamlit as st

st.session_state.auth = "Sign In"
st.session_state.user = None
st.switch_page("app.py")
