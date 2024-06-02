import streamlit as st


def authenticated_menu():
  st.sidebar.page_link("pages/profile.py", label="Profile")
  st.sidebar.page_link("pages/establishments.py", label="Establishments")
  st.sidebar.page_link("pages/my_establishment.py", label="My Establishment")
  st.sidebar.page_link("pages/signout.py", label="Sign out")

def unauthenticated_menu():
  st.sidebar.page_link("app.py", label="Auth")


def menu():
  if "user" not in st.session_state or st.session_state.user is None:
      unauthenticated_menu()
      return
  authenticated_menu()


def menu_with_redirect():
  if "auth" not in st.session_state or st.session_state.auth is None:
      st.switch_page("app.py")
  menu()
