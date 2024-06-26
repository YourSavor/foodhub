import requests
import streamlit as st

if "auth" not in st.session_state:
    st.session_state.auth = "Sign In"

if "user" not in st.session_state:
  st.session_state.user = None

st.markdown("""
    <style>
        div.stButton > button {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

def authentication():
    if st.session_state.auth == "Sign In":
        signin()
    elif st.session_state.auth == "Sign Up":
        signup()

def signin():
    st.title("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        response = requests.post(f"{API_URL}/users/signin", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            st.session_state.user = response.json().get("user")
            st.session_state.page = 'stream'
            st.rerun()
        elif response.status_code == 400:
            st.toast(response.json().get("detail"))
        else:
            st.toast("Unable to sign in due to internal error. Please try again later!")


    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
            cursor: pointer;
            border: none !important;
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: black !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Don't have an account? Register",  type="primary"):
        st.session_state.auth = "Sign Up"
        st.rerun()

def signup():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    first_name = st.text_input("First name")
    middle_name = st.text_input("Middle name")
    last_name = st.text_input("Last name")

    if st.button("Sign Up"):
        response = requests.post(f"{API_URL}/users/signup", json={
            "username": username,
            "password": password,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name
        })

        if response.status_code == 200:
            st.toast("You have successfully signed up!")
        else:
            st.toast(response.json().get("detail"))

    st.markdown(
        """
        <style>
        button[kind="primary"] {
            background: none!important;
            border: none;
            padding: 0!important;
            color: black !important;
            text-decoration: none;
            cursor: pointer;
            border: none !important;
        }
        button[kind="primary"]:hover {
            text-decoration: none;
            color: black !important;
        }
        button[kind="primary"]:focus {
            outline: none !important;
            box-shadow: none !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Already have an account? Sign In", type="primary"):
        st.session_state.auth = "Sign In"
        st.rerun()

from menu import menu

if st.session_state.user is not None:
  st.switch_page("pages/profile.py")

if st.session_state.user is None:
  authentication()
