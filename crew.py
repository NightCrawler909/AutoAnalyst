from crewai import Crew, Process
from agents import CompanyAnalysisAgents
from tasks import CompanyAnalysisTasks

def run_analysis_crew(company_name: str):
    # Instantiate the agent and task classes
    agents_factory = CompanyAnalysisAgents()
    tasks_factory = CompanyAnalysisTasks()

    # Create the agent instances
    researcher = agents_factory.researcher_agent()
    analyst = agents_factory.financial_analyst_agent()

    # Create the task instances
    research_task = tasks_factory.research(researcher, company_name)
    analyze_task = tasks_factory.analyze(analyst, company_name)

    # Instantiate the Crew
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analyze_task],
        process=Process.sequential
    )

    # Kickoff the crew process and return the result
    result = crew.kickoff()
    return result
