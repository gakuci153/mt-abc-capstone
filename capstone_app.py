import streamlit as st
from helper import utility as u

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def logout():
    if st.button("Confirm to Log out?"):
        u.clear_all_sessions()
        st.rerun()

login_page = st.Page("info/login.py", title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

usecase_1 = st.Page("usecases/usecase_1.py", title="Starting a Business", icon=":material/tips_and_updates:", default=True)
usecase_2 = st.Page("usecases/usecase_2.py", title="Use Case 2", icon=":material/psychology:")

about_us = st.Page("info/about_us.py", title="About Us", icon=":material/person:")
methodology = st.Page("info/methodology.py", title="Methodology", icon=":material/polyline:")

if st.session_state["logged_in"]:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Use Cases": [usecase_1, usecase_2],
            "Notes": [methodology, about_us],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()