import time
from crewai import Crew,Process
from agents import schema_agent,query_agent,file_agent,delay_agent
from tasks import create_tasks

if __name__ == "__main__":
    user_query = input("Enter your query : ")

    tasks_list = create_tasks(user_query = user_query,delay_seconds = 2)

    project_crew = Crew(
        agents = [schema_agent,delay_agent,query_agent,file_agent],
        tasks = tasks_list,
        process = Process.sequential,
        verbose = True
    )

    try:
        results = project_crew.kickoff()
        time.sleep(2)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Try and Catch   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(results)
    except Exception as e:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ",e)