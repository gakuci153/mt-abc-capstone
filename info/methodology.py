# filename: methodology.py
import streamlit as st

overview = """

# Methodology

## 1. Overview

This document outlines the methodology and technical specifications for this application that provides structured guidance for starting a business in Singapore and accessing the business schemes. Built with Python, Streamlit, OpenAI’s LLM models, LangChain, and CrewAI, the application is deployed on Streamlit Community Cloud.

---

## 2. Technology Stack

- **Programming Language**: Python
- **Web Framework**: Streamlit
- **Language Models**: OpenAI’s Large Language Models (LLMs)
- **Data Orchestration Framework**: LangChain
- **Agent Framework**: CrewAI
- **Deployment Platform**: Streamlit Community Cloud

---

## 3. Data Flow Overview

The application follows a structured approach to data ingestion, storage, retrieval, and validation to ensure accurate information is accessible.

### 3.1 Data Ingestion

- **Primary Data Sources**:
  - The application scrapes primary government data sites from IRAS, GoBusiness and ACRA, using LangChain’s RecursiveURLLoader.
  

- **Data Storage**:
  - Collected data is saved locally in JSON format, capturing metadata such as the URL reference, title, and content.

### 3.2 Data Retrieval

- **Local Data Retrieval**:
  - **Tool**: JSON RAG (Retrieval Augmented Generation) Search Tool from CrewAI.
  - **Function**: Retrieves relevant data from locally stored JSON files.

- **External Data Retrieval**:
  - **Tool**: Website RAG Search Tool from CrewAI.
  - **Function**: Accesses supplementary information from government websites under the `gov.sg` domain if it is not available in local data.

---

## 4. User Query Processing and Validation

1. **Input Validation**:
   - Validates user input to confirm it aligns with the application’s domain and ensures it is free from harmful or inappropriate content.
  
   
2. **Requirement Extraction**:
   - The LLM interprets user requirements to define the specific use case. If key information is missing, the system prompts the user for additional input.

   
3. **Workflow Activation**:
   - Upon gathering all required information, CrewAI initiates a structured workflow, triggering a series of agent actions to gather relevant data and generate reports.

---

## 5. Agent Structure and Responsibilities

The application employs multiple CrewAI agents, each specialized in different domains, to ensure comprehensive data collection and reporting.

### 5.1 Use Case 1

"""
#: Singapore Business Startup Assistant

uc1_agent_detail = """
#### Agent Details

- **Business Agent**  
  - **Role**: Collects information required for business setup and outlines company registration procedures in Singapore.

  
- **License Expert Agent**  
  - **Role**: Gathers information on business, professional, and industrial licensing requirements in Singapore.

  
- **Insurance Expert Agent**  
  - **Role**: Collects data on business insurance options, eligibility, and application processes available in Singapore.

  
- **Consultant Agent**  
  - **Role**: Consolidates information from the Business, License Expert, and Insurance Expert Agents to prepare a comprehensive business startup guide.

### 5.2 Use Case 2

"""
#: Singapore Business Schemes Assistant

uc2_agent_detail = """
#### Agent Details

- **Business Scheme Expert Agent**  
  - **Role**: Gathers details on business support schemes, financial assistance, and grant options in Singapore.

  
- **Tax Expert Agent**  
  - **Role**: Collects data on tax requirements, incentives, reliefs, and benefits available for Singapore businesses.

  
- **Report Writer Agent**  
  - **Role**: Reviews findings from the Business Scheme Expert and Tax Expert Agents and consolidates them into a comprehensive guide on business schemes and tax benefits.

---
"""

deployment = """
## 6. Deployment

The application is hosted on Streamlit Community Cloud.

"""

st.markdown(overview)

st.image("./images/use_case1.png", caption="Use Case 1 : Singapore Business Startup Assistant")

st.markdown(uc1_agent_detail)

st.image("./images/use_case2.png", caption="Use Case 2 : Singapore Business Schemes Assistant")

st.markdown(uc2_agent_detail)

st.markdown(deployment)