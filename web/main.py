import requests
import streamlit as st
from streamlit_navigation_bar import st_navbar

API_URL = "http://127.0.0.1:8000"

def main():
    page = st_navbar(["Sign Up", "Sign In"])
    st.write(page)

    if page == "Sign Up":
        signup()
    elif page == "Sign In":
        signin()

def signin():
    st.title("Sign In")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if 'users' in st.session_state and username in st.session_state.users:
            user = st.session_state.users[username]
            if user["password"] == password:
                st.session_state.current_user = username
                st.success("You have successfully signed in!")
            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

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

      if response.status_code == 201:
          st.success("You have successfully signed up!")
          st.info("Go to Sign In page to log in.")
      else:
          st.error(response.json().get("message", "An error occurred"))

if __name__ == "__main__":
    main()
