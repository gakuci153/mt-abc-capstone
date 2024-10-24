import streamlit as st

from helper import utility as u
from logics import ai_assistant as a, validator as v

st.subheader("Singapore Business Schemes Assistant", divider=False)

u.show_disclaimer()

u.show_sample_prompt("uc2")

if "uc2_messages" not in st.session_state:
    st.session_state.uc2_messages = []

if "uc2_query" not in st.session_state:
    st.session_state["uc2_query"] = ""

if "uc2_result" not in st.session_state:
    st.session_state["uc2_result"] = ""

for uc2_message in st.session_state.uc2_messages:
    with st.chat_message(uc2_message["role"]):
        st.markdown(uc2_message["content"])

response = ""

if prompt := st.chat_input("Hi! Wondering about business schemes and benefits in Singapore?", key="usecase2"):
    st.session_state.uc2_messages.append({"role": "user", "content": prompt})
    st.session_state["uc2_query"] = prompt
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.status("Trying to find an answer...", expanded=True) as status:

            try:
                st.write("Validating user query...")
                # validate the user input to ensure the necessary input are provided
                validation_response = v.validate_user_input(st.session_state["uc2_query"], usecase="uc2")

                user_input = {}

                # check if further information is still needed to capture
                if(validation_response["valid_query"]):
                    user_input["init_query"] = st.session_state["uc2_query"]
                    user_input["industry"] = validation_response["industry"]
                    user_input["company_revenue"] = validation_response["company_revenue"]
                    user_input["business_type"] = validation_response["business_type"]
                    user_input["additional_info"] = validation_response["additional_info"]
                                        
                    st.write(f"{user_input}")

                    ### this execution will take a few minutes to run
                    st.write("I am working on it. It will take a few minutes!!")
                    
                    result = "Fake result"
                    result = a.schemes_assistant_crew().kickoff(inputs=user_input)        
                    st.session_state["uc2_result"] = result.tasks_output[2]
                    st.session_state["uc2_query"] = ""

                    response = "Report is ready!!!"
                    st.write(response)
                    
                    status.update(label="Report is ready. Yayyy!!!", state="complete", expanded=True)
                else:
                    response = "I am unable to proceed with the query. " + validation_response["reason"] 
                    st.write(response)
                    st.session_state["uc2_result"] = ""
                    status.update(label="Sorry. Please try again!!!", state="error", expanded=True)
            
            except Exception as e:
                response = "Sorry! I failed due to technical error. Try again!!!" + " " + repr(e)
                st.write(response)
                status.update(label="Opps.. something went wrong!!!", state="error", expanded=True)
                st.session_state["uc2_query"] = ""
                st.session_state["uc2_result"] = ""

        st.session_state.uc2_messages.append({"role": "assistant", "content": response})


if st.session_state["uc2_result"] != "":
    st.markdown(st.session_state["uc2_result"])

col1, col2 = st.columns(2)
    
with col1:
    if st.button("Clear chat history..."):
        st.session_state.uc2_messages = []
        st.session_state["uc2_query"] = ""
        st.session_state["uc2_result"] = ""
        response = ""

with col2:
    if st.session_state["uc2_result"] != "":
        st.download_button(
            label="Download Report", 
            data=str(st.session_state["uc2_result"]), 
            file_name="business_scheme_tax_guide.md", 
            icon=":material/download:"
        )