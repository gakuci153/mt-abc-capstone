# filename: utility.py
import json
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# """  
# This file contains the common components used in this project.    
# """  

"""Load the environment variables"""

if load_dotenv('.env'):
    
    # for local development
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL_NAME')
    OPENAI_EMBEDDING = os.getenv('OPENAI_EMBEDDING_NAME')
    FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
else:
    OPENAI_KEY = st.secrets['OPENAI_API_KEY']
    OPENAI_MODEL = st.secrets['OPENAI_MODEL_NAME']
    OPENAI_EMBEDDING = st.secrets['OPENAI_EMBEDDING_NAME']
    FIRECRAWL_API_KEY = st.secrets['FIRECRAWL_API_KEY']


def clear_all_sessions():
    """Clear all the sessions."""
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


def load_ds_file():
    """Load the datasource file"""
    with open('./data/source.json', 'r') as data_file:
        source_json = json.load(data_file)

    return source_json

def check_file(file_name):

    # Create a Path object
    file_path = Path(file_name)

    # Check if the file exists
    return file_path.exists()


def show_sample_prompt(usecase):

    all_samples = {
        "uc1" : [
            "Setting up a crypto trading company. I've a foreign investor.",
            "How to start the audit firm in Singapore. It will be a partnership with my colleague.",
            "My friend and I want to start a Space Launch Service company. We have 10 million capital.",
            "Process for starting a shipping business."
        ],
        "uc2" : [
            "Find out the business support schemes for IT business with revenue 10k but having negative cashflow.",
            "I want to find out business support schemes for IT business with revenue 10k but having negative cashflow",
            "I want to find out business support schemes for IT business with revenue 10k but having negative cashflow",
            "I want to find out business support schemes for IT business with revenue 10k but having negative cashflow"
        ]
    }

    html_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>2 Rows, 3 Columns Box</title>
            <style>
                .container {
                    display: grid;
                    grid-template-columns: repeat(2, auto);
                    grid-template-rows: repeat(2, auto);
                    gap: 10px;
                    padding: 20px;
                    max-width: 600px;
                    margin: auto;
                }

                .box {
                    background-color: #f0f0f0;
                    padding: 10px 20px;
                    text-align: center;
                    border: 1px solid #ccc;
                    border-radius: 10px; /* Rounded edges */
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="box">sample0</div>
                <div class="box">sample1</div>
                <div class="box">sample2</div>
                <div class="box">sample3</div>
            </div>
        </body>
        </html>
    """

    samples = all_samples[usecase]

    for i in range(4):
        html_code = html_code.replace(f"sample{i}", samples[i])

    st.html(html_code)

def show_disclaimer():

    with st.expander("**DISCLAIMER**"):
        st.write("""
        **IMPORTANT NOTICE**: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        **Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

        Always consult with qualified professionals for accurate and personalized advice.
        """)
