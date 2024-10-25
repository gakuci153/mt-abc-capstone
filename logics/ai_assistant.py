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
        goal="Gather the necessary information for business setup and outline the detailed process for company registration in Singapore.",

        backstory="""\
        As a Business Advisor, your expertise in the business setup process in Singapore is unmatched. 
        You provide the consultation based on information from official Singapore government websites 
        ending in '.gov.sg'.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_prerequisit = Task(
        description="""\
        Analyze the provided input for the industry, considering an initial capital and business type. 
        They are all provided in <input>, <industry>, <busines_type> and <initial_capital> xml tags respectively.
        I would like you to outline the step-by-step process for registering the business, 
        including specific documentation needed and any relevant government agencies involved. 
        Additionally, detail other legal requirements, such as licenses or permits, as well as compliance 
        measures that must be adhered to throughout the registration process. Any insights into 
        industry-specific regulations or best practices would also be greatly appreciated.

        input : <input>{init_query}</input>
        industry : <industry>{industry}</industry>
        business type : <business_type>{business_type}</business_type>
        initial capital : <initial_capital>{company_capital}</initial_capital>
        
        """,

        expected_output="""\
        Create a step-by-step guide for company registration in the {industry} industry and 
        all the mandatory requirements and criteria, along with references to the original sources. 
        Additionally, advise on the best company structure to adopt.
        """,

        agent=agent_business_advisor,

        async_execution=True # Will be executed asynchronously
    )

    agent_license_expert = Agent (
        role="License Expert",
        goal="""\
        Gather the necessary information on business, professional and industrial licensing requirements in Singapore.
        """,

        backstory="""\
        You are a licensing expert knowledgeable about licensing requirements and application processes 
        in Singapore. You provide the consultation based on information from official Singapore government 
        websites ending in '.gov.sg'.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_license_application = Task(
        description="""\
        Analyze the provided input in the context of the industry, considering an initial capital and business type. 
        They are all provided in <input>, <industry>, <busines_type> and <initial_capital> xml tags respectively.
        You need to determine the specific licensing requirements relevant to that industry, 
        including any necessary permits or certifications. 
        Additionally, provide comprehensive details on regulatory compliance obligations, such as ongoing reporting 
        requirements and adherence to industry standards. If possible, include any relevant government 
        agencies or resources where further information or assistance regarding these requirements can be found.
        
        input : <input>{init_query}</input>
        industry : <industry>{industry}</industry>
        business type : <business_type>{business_type}</business_type>
        initial capital : <initial_capital>{company_capital}</initial_capital>

        """,

        expected_output="""\
        Create a list of licenses required, documentation needed, and a step-by-step guide for 
        the license application process, and license fees if any along with references to the original sources.
        """,
        
        agent=agent_license_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_insurance_expert = Agent (
        role="Insurance Expert",
        goal="""\
        Gather the necessary information on the business insurances available in Singapore and 
        outline the detailed requirement and application process.
        """,

        backstory="""\
        You are an expert in business insurance with knowledge of regulatory requirements in Singapore. 
        You provide consultation based on information from official Singapore government websites 
        ending in '.gov.sg' and the insurance companies registered in Singapore.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[tool_web_rag]
        #tools=[tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_acra_json, tool_web_rag]
    )

    task_insurance_application = Task(
        description="""\
        Analyze the provided input for the industry, considering initial capital and business type.
        They are all provided in <input>, <industry>, <busines_type> and <initial_capital> xml tags respectively.
        Determine the regulatory insurance requirements specific to that business type 
        and industry, and provide details on the insurance requirements from companies in Singapore only.
        
        input : <input>{init_query}</input>
        industry : <industry>{industry}</industry>
        business type : <business_type>{business_type}</business_type>
        initial capital : <initial_capital>{company_capital}</initial_capital>
        
        """,

        expected_output="""\
        Create a list of required insurance policies, including their coverage details, premium costs, 
        and a step-by-step application guide for the company, along with references to original sources. 
        Additionally, include recommendations.
        """,
        
        agent=agent_insurance_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_consultant = Agent (
        role="Consultant",
        goal="Consolidate all information from other agents and prepare a comprehensive guide for the client.",

        backstory="""\
        You are a consultant skilled in consolidating reports from other agents. 
        With a keen eye for detail, organize all information into a coherent and comprehensive report for the client.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_guide = Task(
        description="""\
        Gather and carefully review all reports from other agents. 
        Prepare a comprehensive guide by consolidating all the information in a single report.
        """,
        
        expected_output="""\
        Create a final guide for setting up a business in Singapore, 
        including references to original sources. The document should be presentable, consistent, 
        error-free, and properly formatted with appropriate indentation.
        """,
        
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
        Gather information on business support schemes, financial assistance, and grants available in Singapore.
        """,

        backstory="""\
        As a Business Scheme Expert, your knowledge of business support schemes, financial assistance, and grants in Singapore is exceptional. 
        You provide the consultation based on information from Singapore government websites ending in '.gov.sg'.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[]
        #tools=[tool_gobusiness_json,tool_serperweb, tool_scrapeweb]
        tools=[tool_gobusiness_json, tool_web_rag]
    )

    task_gather_schemes_info = Task(
        description="""\
        Analyze the provided input, industry, business type, company revenue, and additional info. 
        They are all provided in <input>, <industry>, <business_type>, <company_revenue> and <additional_info> xml tags respectively.
        Provide the information on Singapore government schemes, financial assistance, 
        grants, and any other relevant benefits that closely match these input.

        input : <input>{init_query}</input>
        industry : <industry>{industry}</industry>
        business type : <business_type>{business_type}</business_type>
        company revenue : <company_revenue>{company_revenue}</company_revenue>
        additional info : <additional_info>{additional_info}</additional_info>

        """,

        expected_output="""\
        Create a list of available Singapore government schemes, financial assistance, 
        grants, and other relevant benefits that match user input. Include eligibility criteria 
        for each scheme, required documents, and a step-by-step application process, 
        along with references to original sources. Include recommendations.
        """,

        agent=agent_scheme_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_tax_expert = Agent (
        role="Tax Expert",
        goal="""\
        Gather information on taxation requirements, tax incentives, tax relief, and other tax benefits 
        relevant to Singapore.
        """,

        backstory="""\
        As a Tax Expert, your knowledge of corporate tax matters in Singapore is exceptional. 
        You provide the consultation based on information from Singapore government websites ending in '.gov.sg'.
        """, 
        
        allow_delegation=False,
        verbose=True,

        #tools=[]
        #tools=[tool_gobusiness_json,tool_serperweb, tool_scrapeweb]
        tools=[tool_iras_json, tool_web_rag]
    )

    task_gather_tax_info = Task(
        description="""\
        Analyze the provided input, industry, business type, company revenue, and additional info. 
        They are all provided in <input>, <industry>, <business_type>, <company_revenue> and <additional_info> xml tags respectively. 
        Gather relevant Singapore government tax incentives, exemptions, claims, and other beneficial 
        information that closely aligns with these input and is advantageous for the business. 
        Then, provide detailed information on taxation, tax incentives, tax relief, tax exemptions and the steps for claims or submissions.
        
        input : <input>{init_query}</input>
        industry : <industry>{industry}</industry>
        business type : <business_type>{business_type}</business_type>
        company revenue : <company_revenue>{company_revenue}</company_revenue>
        additional info : <additional_info>{additional_info}</additional_info>
        
        """,

        expected_output="""\
        Provide details on Singapore government taxation requirements, tax incentives, tax relief, 
        tax exemptions, and other relevant information that benefits the business based on user inputs. 
        Include a list of required documents, eligibility criteria, and step-by-step processes to claim tax benefits, 
        along with references to original sources.
        """,

        agent=agent_tax_expert,

        async_execution=True # Will be executed asynchronously
    )

    agent_report_writer = Agent (
        role="Report Writer",
        goal="Consolidate all information from other agents and prepare a comprehensive guide for the client.",
        
        backstory="""\
        You are the report writer responsible for reviewing and consolidating reports from other agents. 
        With a keen eye for detail, you will organize the information into a coherent and comprehensive guide for the client.
        """, 
        
        allow_delegation=False,
        verbose=True,

        tools=[]
    )

    task_prepare_report = Task(
        description="""\
        Gather and carefully review all reports from other agents. 
        Compile a comprehensive guide by consolidating all the information in a single report.
        """,

        expected_output="""\
        Create a final guide on business support schemes in Singapore including references to original sources.
        The document should be presentable, consistent, error-free and properly formated with appropriate identation. 
        """,

        context=[task_gather_schemes_info, task_gather_tax_info],
        agent=agent_report_writer,

        #tools=[tool_dalle],
        async_execution=False
    )

    crew = Crew(
        agents=[agent_scheme_expert, agent_tax_expert, agent_report_writer], 
        tasks=[task_gather_schemes_info, task_gather_tax_info, task_prepare_report],
        verbose=True
    )

    return crew
