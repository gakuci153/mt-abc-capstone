import streamlit as st  
import hmac 

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def password_entered():  
        """Checks whether a password entered by the user is correct."""  
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):  
            st.session_state["password_correct"] = True  
            st.session_state["logged_in"] = True
            del st.session_state["password"]  # Don't store the password.  
        else:  
            st.session_state["password_correct"] = False  
            

# Show input for password.  
st.title("Welcome to Capstone Project C!!")
st.text_input("Please enter the password to continue", type="password", on_change=password_entered, key="password")  

if st.session_state["password_correct"] == False:  
    st.error("😕 Password incorrect! Please try again or contact mya_thein@nlb.gov.sg")  
