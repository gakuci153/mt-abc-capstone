from crewai import Agent, Task, Crew
from crewai_tools import YoutubeChannelSearchTool, FileReadTool

from helper import data_loader

data_files = data_loader.DATA_FILES

# Making sure the source data are loaded
#data_loader.prepare_data(data_files)

# Initialize the tool
#tool_acra_file = FileReadTool(file_path=data_files['acra'])
#tool_gobusiness_file = FileReadTool(file_path=data_files['gobusiness'])
#tool_iras_file = FileReadTool(file_path=data_files['iras'])

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
        Singapore Government website with "gov.sg" domain.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prerequisit = Task(
        description="""\
        Analyze the provided {init_query}, {industry}, {company_capital} and provide the step by step process to register the business.
        """,

        expected_output="""\
        Step by step guide for company registration with the original source as reference for the {industry}.
        """,

        agent=agent_business_advisor,

        async_execution=True # Will be executed asynchronously
    )

    agent_license_expert = Agent (
        role="License Expert",
        goal="Gather the licensing requirment for the businees type and industry consulsted by the Business Advisor.",

        backstory="""\
        You are the license expert who understands licensing needs and application processes in Singapore.
        You will provide the consultation based on the information from Singapore Government website with "gov.sg" domain.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_license_application = Task(
        description="""\
        Analyze the provided {industry}, {company_capital} and determine the licensing requirement specific to that industry. 
        Provide the details licensing requirements and regulatory compliance specific to the {industry}.
        """,

        expected_output="""\
        Step by step guide for license process and application with the original source as reference.
        """,
        #context=[task_prerequisit],
        agent=agent_license_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_consultant = Agent (
        role="Consultant",
        goal="Consolidate all the information from other agents and prepare the comphrensive guide for the client.",

        backstory="""\
        You are the consultant who consult and consolidate the reports from the other agents. With an eye for detail, you organize all the information into a coherent and comphrensive guide for the client.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_guide = Task(
        description="""\
        Gather all the reports from other agents and review carefully. And prepare the guide that contains 
        the step by step information on the {industry} specific business registration process, licensing process, 
        cost of registration, setting up the banks account and other regulatory compliance 
        that are essentials to start a business.
        """,

        expected_output="""\
        Final comphresive guide document for setting up business in Singapore with the original source as reference.
        The document will be presentable, consistent and error free with proper formatting and identation. 
        """,
        context=[task_prerequisit, task_license_application],
        agent=agent_consultant,

        async_execution=False
    )

    crew = Crew(
        agents=[agent_business_advisor, agent_license_expert, agent_consultant],
        tasks=[task_prerequisit, task_license_application, task_prepare_guide],
        verbose=True
    )

    return crew
