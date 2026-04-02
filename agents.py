import os
from dotenv import load_dotenv
from crewai import Agent
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# 1. Initialize the raw Tavily tool
raw_tavily = TavilySearchResults(max_results=4)

# 2. Wrap it in a standard adapter that CrewAI completely trusts
search_tool = Tool(
    name="Web Search",
    func=raw_tavily.invoke,
    description="Useful for searching the web for recent news, financial data, and market sentiment."
)

class CompanyAnalysisAgents:
    def researcher_agent(self):
        return Agent(
            role='Senior Market Researcher',
            goal='Find the most recent and critical news, financial shifts, and market sentiment about a given company',
            backstory='Expertise in scraping and analyzing real-time web data to uncover hidden market trends.',
            verbose=True,
            allow_delegation=False,
            tools=[search_tool]  # <-- Passing the cleanly wrapped tool here
        )

    def financial_analyst_agent(self):
        return Agent(
            role='Expert Financial Analyst',
            goal='Synthesize raw research into a crisp, professional markdown briefing with bullet points and risk factors',
            backstory='Background in investment banking and sharp, concise reporting.',
            verbose=True,
            allow_delegation=False
        )