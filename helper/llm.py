# filename: llm.py
from openai import OpenAI
import tiktoken
from helper import utility as u

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=u.OPENAI_KEY)

def get_embedding(input, model=u.OPENAI_EMBEDDING):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model=u.OPENAI_MODEL, temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
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
def get_completion_by_messages(messages, model=u.OPENAI_MODEL, temperature=0, top_p=1.0, max_tokens=1024, n=1, stream=False):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        stream=stream
    )
    if stream:
       return response
    else:
        return response.choices[0].message.content


# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
def count_tokens(text):
    encoding = tiktoken.encoding_for_model(u.OPENAI_MODEL)
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model(u.OPENAI_MODEL)
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))
    