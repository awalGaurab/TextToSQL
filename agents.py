import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_ollama import ChatOllama
from tools import get_db_schema,execute_sql_query,create_csv_file,delay_tool

load_dotenv()
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

llm = ChatOllama(model="ollama/gemma3:latest", #gemma3:latest ", #"llama3.2:latest",
          temperature = 0.5,
          max_retries = 5,
          timeout=120
        )

# First Agent
schema_agent = Agent(
    role = "Database Schema Analyst",
    goal = """
        Understand the structure of the database by listing tables and their schemas.
        Provide this information to the other agents.
    """,
    backstory="""
        You are a meticulous database expert.Your job is to analyze the database structure and 
        provide a detailed overview of tables and coluns so that read only queries can be formed correctly using given tool.
    """,
    tools=[get_db_schema],
    llm=llm,
    verbose = True,
    allow_delegation=False
)

# Second Agent
query_agent = Agent(
    role = "SQL query executor for read only operations.",
    goal = """
        Generate,re-check and execute a read-only sql query based on a users request.
        The query must not contain destructive statements and should select only necessary columns.
        """,
    backstory="""
        You are master of safe sql practices.Your primary function is to translate natural language 
        into efficient and error free **read-only** sql queries.You strictly adhere to the principle of least 
        privilege,never performing destructive operations like UPDATE or DELETE, 
        and always select only column needed to answer the questions.
        """,
    tools=[execute_sql_query],
    llm=llm,
    verbose = True,
    allow_delegation=False
)

# Third Agent
file_agent = Agent(
    role = "Data formatter and file creator.",
    goal = """
        Take raw query results and create a structured csv file.
        """,
    backstory="""
        You are data management specialist.Your task is to take unformatted data and store it neatly in a csv file.
        """,
    tools=[create_csv_file],
    llm=llm,
    verbose = True
)

#  Foruth Agent
delay_agent = Agent(
    role = "Workflow pacer.",
    goal = """
        Introduce a deliberate time lag in a workflow.
        """,
    backstory="""
        You are a meticulous workflow manager who ensures tasks are executed at a controlled pace.
        """,
    tools=[delay_tool],
    llm=llm,
    verbose = True
)