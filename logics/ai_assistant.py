__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent, Task, Crew
from crewai_tools import JSONSearchTool, SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, DallETool

from helper import data_loader

data_files = data_loader.DATA_FILES

# Make sure the source data are loaded
data_loader.prepare_data(data_files)

# Initialize the local JSON search tool
tool_gobusiness_json = JSONSearchTool(json_path=data_files['gobusiness'])
tool_acra_json = JSONSearchTool(json_path=data_files['acra'])
tool_iras_json = JSONSearchTool(json_path=data_files['iras'])

# Initialize the web search tool
tool_web_rag = WebsiteSearchTool()

#tool_serperweb = SerperDevTool(country="sg", location="Singapore")
#tool_scrapeweb = ScrapeWebsiteTool()

tool_dalle = DallETool()

# Initialize the tool with a specific Youtube channel handle for target search
#tool_acra_youtube = YoutubeChannelSearchTool(youtube_channel_handle='@acraadmin')
#tool_iras_youtube = YoutubeChannelSearchTool(youtube_channel_handle='@IRASSpore')

def business_assistant_crew():

    agent_business_advisor = Agent (
        role="Business Advisor",
        goal="Gather the information required for business setup and provide the detail process of company registration.",

        backstory="""\
        As a Business Advisor, your expertise in understanding the business setup process in Singapore 
        is unparalleled. You will provide the consultation based on the information from 
        Singapore Government websites which have the domain name ending with "gov.sg".
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_prerequisit = Task(
        description="""\
        Analyze the provided input {init_query}, {industry} industry, initial capital {company_capital} 
        provide the step by step process to register the business as well as other legal requirements and compliances.
        """,

        expected_output="""\
        List of documents needed and step by step guide for company registration with the original source as reference for the {industry} industry.
        """,

        agent=agent_business_advisor,

        async_execution=True # Will be executed asynchronously
    )

    agent_license_expert = Agent (
        role="License Expert",
        goal="""\
        Gather the licensing requirment for the {business_type} businees type and {industry} industry 
        consulsted by the Business Advisor based on the {init_query}
        """,

        backstory="""\
        You are the license expert who understands licensing needs and application processes in Singapore.
        You will provide the consultation based on the information from Singapore Government websites 
        which have the domain name ending with "gov.sg".
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_license_application = Task(
        description="""\
        Analyze the provided {init_query}, {industry} industry, initial capital {company_capital} and 
        determine the licensing requirement specific to that industry. Provide the details licensing 
        requirements and regulatory compliance specific to the {industry} industry.
        """,

        expected_output="""\
        List of licenses needed and step by step guide for license process and application for the company
        with the original source as reference.
        """,
        
        agent=agent_license_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_insurance_expert = Agent (
        role="Insurance Expert",
        goal="""\
        Gather the insurance needs for the {business_type} businees type and {industry} industry 
        consulsted by the Business Advisor based on the {init_query}.
        """,

        backstory="""\
        You are the expert in business insurance who know the regulatory requirements in Singapore.
        You will provide the consultation based on the information from Singapore Government websites 
        which have the domain name ending with "gov.sg".
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_insurance_application = Task(
        description="""\
        Analyze the provided {init_query}, {industry} industry, initial capital {company_capital} and 
        determine the regulatory requirements for insurance, specific to that business type and industry. 
        Provide the details insurance requirements for the {industry} industry from insurance companies in Singapore only.
        """,

        expected_output="""\
        List of insurance needed, their coverage, premium cost and step by step application guide and application process for the company
        with the original source as reference.
        """,
        
        agent=agent_insurance_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_consultant = Agent (
        role="Consultant",
        goal="Consolidate all the information from other agents and prepare the comphrensive guide for the client.",

        backstory="""\
        You are the consultant who is excellent in consolidating the reports from the other agents. 
        With an eye for detail, you organize all the information into a coherent and comphrensive report for the client.
        You will also prepare the summary process flow in a concise steps for image generator to use.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_guide = Task(
        description="""\
        Gather all the reports from other agents and review carefully. And prepare the guide that contains 
        the list of documents required, eligibility criteria, the step by step guide on the {industry} specific business registration process, licensing process, 
        cost of registration, capital requirements, steps for opening business bank accounts and supporting documents, 
        list of insurance needed, their coverage, premium cost and detail steps on the application process as well as other regulatory 
        compliance that are essentials to start a business. 
        
        """,
        #At the end of the report, an image will be show with a list of topics and its major steps summarized.

        expected_output="""\
        Final comphresive guide document for setting up business in Singapore with the original source as reference.
        The document will be presentable, consistent and error free with proper formatting and identation.  
        """,
        #At the end of the report, a flow chart image will be added which shows the topics from the report and its logical steps.

        context=[task_prerequisit, task_license_application, task_insurance_application],
        agent=agent_consultant,

        #tools=[tool_dalle],
        async_execution=False
    )

    crew = Crew(
        agents=[agent_business_advisor, agent_license_expert, agent_insurance_expert, agent_consultant], 
        tasks=[task_prerequisit, task_license_application, task_insurance_application, task_prepare_guide], 
        verbose=True
    )

    return crew

def schemes_assistant_crew():

    agent_scheme_expert = Agent (
        role="Business Scheme Expert",
        goal="""\
        Gather the business support schemes, tax incentives, financial assistance and grants available 
        on Singapore Government websites which have the domain name ending with "gov.sg".
        """,

        backstory="""\
        As a Business Scheme Expert, your expertise in business support schemes, tax incentives, 
        financial assistances and grants in Singapore is unparalleled. You will provide the consultation 
        based on the information from Singapore Government websites which have the domain name ending with "gov.sg".
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[]
        #tools=[tool_gobusiness_json,tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_web_rag]
    )

    task_gather_schemes_info = Task(
        description="""\
        Analyze the provided inputs {init_query}, {industry} industry, revenue {company_revenue}, 
        {additional_info} and provide the Singapore Government schemes, tax incentives, financial assistants,
        other benefial information which is suitable and closely matched with inputs.
        """,

        expected_output="""\
        Singapore Government schemes, tax incentives, financial assistants, other benefial information which
        are relevants to user inputs and their eligibility criteria, grant amounts, and application processes 
        with the original source as reference.
        """,

        agent=agent_scheme_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_tax_expert = Agent (
        role="Tax Expert",
        goal="""\
        Gather the taxation and tax relief information on Singapore Government websites 
        which have the domain name ending with "gov.sg".
        """,

        backstory="""\
        As a Tax Expert, your expertise in corporate tax matter in Singapore is unparalleled. 
        You will provide the consultation based on the information from Singapore Government websites 
        which have the domain name ending with "gov.sg".
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[]
        #tools=[tool_gobusiness_json,tool_serperweb, tool_scrapeweb]
        tools=[tool_iras_json, tool_web_rag]
    )

    task_gather_tax_info = Task(
        description="""\
        Analyze the provided inputs {init_query}, {industry} industry, revenue {company_revenue}, 
        {additional_info} and gather the Singapore Government tax incentives, taxation and
        other benefial information which is suitable and closely matched with inputs and beneficial to the business.
        And then, you will provide the details information on taxataion, tax relief, steps to claims or submit.
        """,

        expected_output="""\
        Details on Singapore Government tax incentives, taxation requirement, tax relief and exemption, other benefial information which
        are relevants to user inputs and beneficial to the business. And step by step processes with the original source as reference.
        """,

        agent=agent_tax_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_report_writer = Agent (
        role="Report Writer",
        goal="Consolidate all the information from other agents and prepare the comphrensive guide for the client.",

        backstory="""\
        You are the report writer who review and consolidate the reports from the other agents. With an eye for detail, 
        you organize all the information into a coherent and comphrensive guide for the client.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_report = Task(
        description="""\
        Gather all the reports from other agents and review carefully. And compile the report that contains 
        the detail information specific to schemes, tax incentives, financial assistants, other benefial information which
        are relevants to user inputs.
        """,

        expected_output="""\
        Final comphresive guide document on business support schemes in Singapore with the original source as reference.
        The document will be presentable, consistent and error free with proper formatting and identation. 
        At the end of the report, provide the summary in a graphical form with logical flow chart for the management.
        Make sure the image is clear and professional.
        """,
        context=[task_gather_schemes_info],
        agent=agent_report_writer,

        tools=[tool_dalle],
        async_execution=False
    )

    crew = Crew(
        agents=[agent_scheme_expert, agent_tax_expert, agent_report_writer], 
        tasks=[task_gather_schemes_info, task_gather_tax_info, task_prepare_report],
        verbose=True
    )

    return crew


def tool_test_crew():
    agent_tax_researcher = Agent (
        role="Researcher",
        goal="Gather the tax incentives and taxation on Singapore Government websites with gov.sg domains",

        backstory="""\
        As a Tax Researcher, your expertise in tax incentives and taxation in Singapore is unparalleled. You will provide the consultation 
        based on the information from Singapore Government websites that have "gov.sg" domain.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[]
        #tools=[tool_gobusiness_json,tool_serperweb, tool_scrapeweb]
        tools=[tool_web_rag]
    )

    task_gather_tax_info = Task(
        description="""\
        Analyze the provided inputs {init_query}, {industry} industry, revenue {company_revenue}, 
        {additional_info} and provide the Singapore Government tax incentives, taxation and
        other benefial information which is suitable and closely matched with inputs.
        """,

        expected_output="""\
        Singapore Government tax incentives, taxation requirement, other benefial information which
        are relevants to user inputs and step by step processes with the original source as reference.
        """,

        agent=agent_tax_researcher,

        async_execution=True # Will be executed asynchronously
    )

    agent_report_writer = Agent (
        role="Report Writer",
        goal="Consolidate all the information from other agents and prepare the comphrensive guide for the client.",

        backstory="""\
        You are the report write who review and consolidate the reports from the other agents. With an eye for detail, you organize all the information into a coherent and comphrensive guide for the client.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_scheme_report = Task(
        description="""\
        Gather all the reports from other agents and review carefully. And compile the report that contains 
        the detail information specific to schemes, tax incentives, financial assistants, other benefial information which
        are relevants to user inputs.
        """,

        expected_output="""\
        Final comphresive guide document for the business support and tax incentives compiled from context text with the original source as reference.
        The document will be appropriately titled, presentable, consistent and error free with proper formatting and identation. 
        At the end summary of findings in a simple graphical image.
        """,
        context=[task_gather_tax_info],
        agent=agent_report_writer,
        tools=[tool_dalle],
        async_execution=False
    )

    crew = Crew(
        agents=[agent_tax_researcher, agent_report_writer], 
        tasks=[task_gather_tax_info, task_prepare_scheme_report],
        verbose=True
    )

    return crew