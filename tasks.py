import datetime
from crewai import Task
from agents import schema_agent,delay_agent,query_agent,file_agent

def create_tasks(user_query:str,delay_seconds:int):
    """Creates a list of tasks for the Crew to execute."""

    
    get_schema_task = Task(
        description = "Analyze the databse schema to understand its structure.",
        expected_output = "A string containing the full database schema.",
        agent = schema_agent
    )

    delay_task = Task(
        description = f"Pause the workflow for exactly {delay_seconds} seconds.",
        expected_output = f"A confirmation message that delay of {delay_seconds} seconds.",
        agent = delay_agent
    )

    execute_query_task = Task(
        description = f"""Using the schema from the previous task,generate and execute a sql query to answer the users question: '{user_query}'
            The query must be a **read-only SELECT statement** and should **only include the columns required** to answer the question.
            """,
        expected_output = "A string containing the raw data results from the sql query.",
        context = [get_schema_task],
        agent = query_agent,
        # output_file=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(".csv")
    )

    create_csv_task = Task(
        description = f"""
                Take the raw results and user specified filename'.
                Format the results into a proper csv format and save the file.
                The input for this task should be a list of results in comma separated format.
                Example : '[query_result]' 
                Also, query_result should be looks like a list of strings.Example ["Text1","Text2","Text3"]
                Remove any special characters,newline characters.
                
            """,
        expected_output= "A confirmation message stating that the file was created successfully.",
        context = [execute_query_task],
        agent = file_agent,
    )

    return [get_schema_task,delay_task,execute_query_task,create_csv_task]