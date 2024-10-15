import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import tiktoken

load_dotenv('.env')

if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
   OPENAI_MODEL = os.getenv('OPENAI_MODEL_NAME')
   OPENAI_EMBEDDING = os.getenv('OPENAI_EMBEDDING_NAME')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']
   OPENAI_MODEL = st.secrets['OPENAI_MODEL_NAME']
   OPENAI_EMBEDDING = st.secrets['OPENAI_EMBEDDING_NAME']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)

def get_embedding(input, model=OPENAI_EMBEDDING):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model=OPENAI_MODEL, temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content


# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(messages, model=OPENAI_MODEL, temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content


# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
def count_tokens(text):
    encoding = tiktoken.encoding_for_model(OPENAI_MODEL)
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model(OPENAI_MODEL)
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))
