import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI # NEW: Import Gemini

# Initialize the real-time web search tool
search_tool = TavilySearchResults(max_results=3)

# NEW: Initialize the Gemini LLM (Using flash for speed)
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.environ.get("GEMINI_API_KEY")
)

def run_analysis_crew(company_name):
    """Kicks off the multi-agent workflow for a given company."""
    
    # 1. DEFINE THE AGENTS (Now using Gemini)
    researcher = Agent(
        role='Senior Market Researcher',
        goal=f'Uncover the latest news, market shifts, and critical events for {company_name}',
        backstory="You are a veteran Wall Street researcher. You excel at finding hidden risks and financial shifts.",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=gemini_llm  # NEW: Assign Gemini
    )

    analyst = Agent(
        role='Financial Strategist',
        goal=f'Synthesize research into a crisp, professional markdown executive summary for {company_name}',
        backstory="You are a top-tier financial analyst who presents actionable insights to C-level executives.",
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm  # NEW: Assign Gemini
    )

    # 2. DEFINE THE TASKS
    research_task = Task(
        description=f'Search the web for the most recent news regarding {company_name}. Focus on product launches, earnings, or threats.',
        expected_output='A detailed text summary of relevant news.',
        agent=researcher
    )

    report_task = Task(
        description='Review the raw research. Format it into a highly professional executive briefing in Markdown format with headings: Executive Summary, Key Developments, Market Sentiment, and Risks.',
        expected_output='A polished markdown report.',
        agent=analyst
    )

    # 3. ORCHESTRATE THE CREW
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, report_task],
        process=Process.sequential 
    )

    return crew.kickoff()
