import streamlit as st
from helper import llm

st.title("Ask me anything!!")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = llm.OPENAI_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        with st.status("Trying to answer...", expanded=True) as status:
            stream = llm.get_completion_by_messages(messages=messages, stream=True)
            response = st.write_stream(stream)
            status.update(label="Done. Is the answer helpful?", state="complete")
        #st.markdown(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})