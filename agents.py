import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

class CompanyAnalysisAgents:
    def researcher_agent(self):
        return Agent(
            role='Senior Market Researcher',
            goal='Find the most recent and critical news, financial shifts, and market sentiment about a given company',
            backstory='Expertise in scraping and analyzing real-time web data to uncover hidden market trends and critical shifts.',
            verbose=True,
            allow_delegation=False
        )

    def financial_analyst_agent(self):
        return Agent(
            role='Expert Financial Analyst',
            goal='Synthesize raw research into a crisp, professional markdown briefing with bullet points and risk factors',
            backstory='Background in investment banking and sharp, concise reporting. You deliver actionable insights and identify key risk factors.',
            verbose=True,
            allow_delegation=False
        )
