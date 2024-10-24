# filename: about_us.py
import streamlit as st
from helper import llm


st.title("About Us")

project_details = """

## Project Scope:

A user-friendly assistant app designed to help entrepreneurs establish new businesses by providing guidance on navigating government schemes, tax incentives, and financial support options tailored to their specific needs.

## Objective:

1. To assist business owners, startup founders, and investors by guiding them through the business registration process and regulatory requirements.
2. To help business owners access information on various financial support schemes, government assistance, tax incentives, and grants without the need to search multiple websites.

## Data Source:

The project leverages primary data from [www.acra.gov.sg](https://www.acra.gov.sg), [www.gobusiness.gov.sg](https://www.gobusiness.gov.sg), and [www.iras.gov.sg](https://www.iras.gov.sg). The system scrapes these three websites, retrieving up to five levels of links, and stores the data as JSON files in the local system. It also searches for relevant information across Singapore government websites with the domain "gov.sg" as a secondary data source.

## Features:

- **General:** The app validates user inputs to ensure no malicious prompts are entered and that queries remain within the app's designated focus area. The system is password-protected and accessible only to authorized users.
  
### Use Case 1: Starting a Business

The Singapore Business Startup Assistant allows users to specify the nature of the business they wish to establish, available funding, and other relevant details. Based on this input, it generates a report outlining the company registration process, licensing requirements, insurance, setting up a bank account, and other regulatory obligations needed to operate a business in Singapore. The report can be downloaded in markdown format.

### Use Case 2: Accessing Business Support

The Singapore Business Schemes Assistant enables users to find tailored government schemes, financial support, grants, and tax incentives based on the details they provide in the input chat. The report can be downloaded in markdown format.

## Developer:

This application was developed by Mya Thein @ Deepak as part of GovTech's AI Champions Bootcamp - Pilot Run (Whole-of-Government).

"""

st.markdown(project_details)