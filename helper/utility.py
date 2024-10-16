# filename: utility.py
import streamlit as st

# """  
# This file contains the common components used in this project.    
# """  

def clear_all_sessions():
    """Clear all the sessions."""
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)