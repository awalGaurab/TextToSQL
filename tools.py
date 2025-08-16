import os,csv,time,datetime,json
from crewai.tools import tool
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from sqlalchemy import create_engine

load_dotenv()
llm = ChatOllama(model="ollama/gemma3:latest", #gemma3:latest ", #"llama3.2:latest",
          temperature = 0.5,
          max_retries = 5,
          timeout=120
        )

#------------------------------------------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mypostgresql@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)
db = SQLDatabase(engine)
#------------------------------------------------------------------------------------------------------------

# Tool 1 : Schema Tool
@tool("Database Schema Tool")
def get_db_schema() -> str:
    """
        Returns the schema of all tables in the database.
        This is used to understand the database structure.
    """
    return db.get_table_info()

# Tool 2 : Query Tool
@tool("Sql query execution tool")
def execute_sql_query(user_query: str) -> str:
    """
        Generated,re-checks and execute a sql query on the database based on natutal language request.
        The input is the user's natural language question. The tool will return the raw results from the query.
    """

    try:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Trying to run a query.  @@@@@@@@@@@@@@@@@@@@@@")
        print(user_query)
        result = db.run(user_query)

        return str(result)
    except Exception as e:
        return f"An error occurred while executing the query: {e}"
    
@tool("CSV Creator tool")
def create_csv_file(data_list:list)-> list:
    """
    Take raw query results as a string and a filename,then writes the data to a csv file.
    The input should be a single list in the format : 'flename.csv|data'.
    """
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(".csv")

    try:
        with open(filename,'w',newline='') as f:
            csv_writer = csv.writer(f)
            for row in json.loads(data_list):
                csv_writer.writerow(row)
        
        return f"Successfully file created."
    
    except Exception as e:
        return f"An error occurred while creating the csv file: {e}"
    

@tool("Delay Tool")
def delay_tool(seconds:int)-> str:
    """
    A tool to pause execution for a specified number of seconds.
    """

    print(f"/n[Delay Tool] Pausing execution for {seconds} seconds...")
    time.sleep(seconds)
    return f"Execution resumed after a delay of {seconds} seconds..."    