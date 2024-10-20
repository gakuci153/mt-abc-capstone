import streamlit as st
from helper import utility
from logics import validator, business_assistant as bs

st.subheader("Singapore Business Setup Assistant", divider=True)

with st.expander("**DISCLAIMER**"):
    st.write("""
    **IMPORTANT NOTICE**: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    **Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

    Always consult with qualified professionals for accurate and personalized advice.
    """)

utility.show_sample_prompt()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = utility.OPENAI_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

if "init_query" not in st.session_state:
    st.session_state["init_query"] = ""

if "crew_result" not in st.session_state:
    st.session_state["crew_result"] = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

response = ""

if prompt := st.chat_input("Hi, how may I assist you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state["init_query"] = prompt
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.status("Trying to answer...", expanded=True) as status:

            try:
                st.write("Validating user query...")
                # validate the user input to ensure the necessary input are provided
                validation_response = validator.validate_user_input(st.session_state["init_query"])

                user_input = {}

                # check if further information is still needed to capture
                if(validation_response["valid_query"]):
                    user_input["init_query"] = st.session_state["init_query"]
                    user_input["industry"] = validation_response["industry"]
                    user_input["company_capital"] = validation_response["company_capital"]
                    user_input["business_type"] = validation_response["business_type"]
                    st.write(f"Ok. {user_input}")

                    ### this execution will take a few minutes to run
                    st.write("I am working on it. It will take a few minutes!!")
                    
                    result = bs.business_assistant_crew().kickoff(inputs=user_input)
                                        
                    st.session_state["crew_result"] = result.tasks_output[2]
                    response = "Report is ready!!!"
                    st.write(response)
                    st.session_state["init_query"] = ""
            
                    status.update(label="Report is ready. Yayyy!!!", state="complete", expanded=False)
                else:
                    response = "I can't help with query. " + validation_response["reason"] 
                    st.write(response)
                    st.session_state["crew_result"] = ""
                    status.update(label="Sorry. Please try again!!!", state="error", expanded=False)
            except:
                response = "Sorry! I failed due to technical error."
                st.write(response)
                status.update(label="Opps.. something went wrong!!!", state="error", expanded=False)
                st.session_state["init_query"] = ""
                st.session_state["crew_result"] = ""

        st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state["crew_result"] != "":
    st.markdown(st.session_state["crew_result"])

if st.button("Clear chat history..."):
    st.session_state.messages = []
    st.session_state["init_query"] = ""
    st.session_state["crew_result"] = ""
    response = ""