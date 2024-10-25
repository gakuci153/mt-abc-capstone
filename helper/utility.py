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
            "I’m starting a cryptocurrency trading company backed by a foreign investor. Can you outline the regulatory requirements, licensing, and compliance obligations? Also, are there any restrictions or special considerations for foreign investments in this sector?",
            "I want to start an audit firm in Singapore as a partnership with my colleague. Could you provide the essential steps, including qualifications, regulatory requirements, registration, and licensing, as well as advice on structuring the partnership and ensuring compliance?",
            "My friend and I want to start a Space Launch Service company with $10 million in capital. Could you outline the critical steps, including licensing, regulatory requirements, and operational setup? Any insights on managing capital for initial stages would also be helpful.",
            "What are the key steps to start a shipping business, including regulatory requirements, licenses, and initial funding needs? Any insights on business structure and compliance would be helpful."
        ],
        "uc2" : [
            "My friend and I co-own a small IT business generating $10,000 monthly but facing negative cash flow. Can you help us find government assistance programs or support schemes, such as grants or low-interest loans, for small IT companies in financial difficulty?",
            "I want to expand my business reach to European and Latin American clients . Get me the government support schemes to help my business grow. I am in tourism with 10 employees. Current revenue is 70000 SGD.",
            "I own a food stall generating $10,000 monthly but lack savings to expand. Can you help me find government grants or financial assistance programs for small food businesses, including eligibility and application details?",
            "I am a regional director of an MNC in the manufacturing sector. I would like to know if there are any business support options available to help hedge against the current economic downturn. Last year, my company's revenue was $1 million."
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

    with st.expander("Sample Prompts"):
        st.html(html_code)

def show_disclaimer():

    with st.expander("**DISCLAIMER**"):
        st.write("""
        **IMPORTANT NOTICE**: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        **Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

        Always consult with qualified professionals for accurate and personalized advice.
        """)
