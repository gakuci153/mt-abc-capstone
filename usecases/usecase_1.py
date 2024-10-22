import streamlit as st

from helper import utility as u
from logics import ai_assistant as a, validator as v

st.subheader("Singapore Business Setup Assistant", divider=False)

u.show_disclaimer()

u.show_sample_prompt("uc1")

if "uc1_messages" not in st.session_state:
    st.session_state.uc1_messages = []

if "uc1_query" not in st.session_state:
    st.session_state["uc1_query"] = ""

if "uc1_result" not in st.session_state:
    st.session_state["uc1_result"] = ""

for uc1_message in st.session_state.uc1_messages:
    with st.chat_message(uc1_message["role"]):
        st.markdown(uc1_message["content"])

response = ""

if prompt := st.chat_input("Hi! Staring a business in Singapore?", key="usecase1"):
    st.session_state.uc1_messages.append({"role": "user", "content": prompt})
    st.session_state["uc1_query"] = prompt
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.status("Trying to answer...", expanded=True) as status:

            try:
                st.write("Validating user query...")
                # validate the user input to ensure the necessary input are provided
                validation_response = v.validate_user_input(st.session_state["uc1_query"], usecase="uc1")

                user_input = {}

                # check if further information is still needed to capture
                if(validation_response["valid_query"]):
                    user_input["init_query"] = st.session_state["uc1_query"]
                    user_input["industry"] = validation_response["industry"]
                    user_input["company_capital"] = validation_response["company_capital"]
                    user_input["business_type"] = validation_response["business_type"]
                    st.write(f"Ok. {user_input}")

                    ### this execution will take a few minutes to run
                    st.write("I am working on it. It will take a few minutes!!")
                    
                    result = a.business_assistant_crew().kickoff(inputs=user_input)        
                    st.session_state["uc1_result"] = result.tasks_output[3]
                    st.session_state["uc1_query"] = ""

                    response = "Report is ready!!!"
                    st.write(response)
                    
                    status.update(label="Report is ready. Yayyy!!!", state="complete", expanded=True)
                else:
                    response = "I am unable to proceed with the query. " + validation_response["reason"] 
                    st.write(response)
                    st.session_state["uc1_result"] = ""
                    status.update(label="Sorry. Please try again!!!", state="error", expanded=True)
            
            except Exception as e:

                response = "Sorry! I failed due to technical error. Try again!!!" + " " + repr(e)
                st.write(response)
                status.update(label="Opps.. something went wrong!!!", state="error", expanded=True)
                st.session_state["uc1_query"] = ""
                st.session_state["uc1_result"] = ""

        st.session_state.uc1_messages.append({"role": "assistant", "content": response})

if st.session_state["uc1_result"] != "":
    st.markdown(st.session_state["uc1_result"])

col1, col2 = st.columns(2)
    
with col1:
    if st.button("Clear chat history..."):
        st.session_state.uc1_messages = []
        st.session_state["uc1_query"] = ""
        st.session_state["uc1_result"] = ""
        response = ""

with col2:
    if st.session_state["uc1_result"] != "":
        st.download_button(
            label="Download Report", 
            data=str(st.session_state["uc1_result"]), 
            file_name="business_registration_guide.md", 
            icon=":material/download:"
        )