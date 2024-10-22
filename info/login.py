# filename: login.py
import streamlit as st  
import hmac 

if "password_match" not in st.session_state:
    st.session_state["password_match"] = ""

def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
            st.session_state["password_match"] = "OK"
            del st.session_state["password"]  # Don't store the password.  
        else:  
            st.session_state["password_match"] = "😕 Password incorrect! Please try again or contact mya_thein@nlb.gov.sg"
            
st.set_page_config(
    page_title="Business Startup Assistant",
    page_icon=":material/smart_toy:",
)

# Show input for password.  
st.title("Welcome to Capstone Project C!!")
st.text_input("Please enter the password to continue", type="password", on_change=password_entered, key="password")  

if st.session_state["password_match"] == "":  
    st.empty()  
elif st.session_state["password_match"] == "OK":
    st.session_state["logged_in"] = True
    st.switch_page(st.Page("usecases/usecase_1.py", title="Use Case 1", icon=":material/tips_and_updates:"))
else:
     st.error(st.session_state["password_match"])