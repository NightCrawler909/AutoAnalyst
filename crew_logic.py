import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool # NEW: Import the CrewAI tool decorator
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI 

# 1. Initialize the raw LangChain tools
tavily_raw = TavilySearchResults(max_results=3)

# 2. NEW: Wrap it in a CrewAI native tool to bypass the Pydantic error
@tool("Web Search Tool")
def search_tool(search_query: str) -> str:
    """Search the web for recent news, market shifts, and information."""
    return tavily_raw.invoke({"query": search_query})

# 3. Initialize the Gemini LLM
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # CHANGED: 1.5 is retired, 2.5 is the current active model
    google_api_key=os.environ.get("GEMINI_API_KEY")
)

def run_analysis_crew(company_name):
    """Kicks off the multi-agent workflow for a given company."""
    
    # DEFINE THE AGENTS
    researcher = Agent(
        role='Senior Market Researcher',
        goal=f'Uncover the latest news, market shifts, and critical events for {company_name}',
        backstory="You are a veteran Wall Street researcher. You excel at finding hidden risks and financial shifts.",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool], # Now using the wrapped CrewAI tool!
        llm=gemini_llm  
    )

    analyst = Agent(
        role='Financial Strategist',
        goal=f'Synthesize research into a crisp, professional markdown executive summary for {company_name}',
        backstory="You are a top-tier financial analyst who presents actionable insights to C-level executives.",
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm  
    )

    # DEFINE THE TASKS
    research_task = Task(
        description=f'Search the web for the most recent news regarding {company_name}. Focus on product launches, earnings, or threats.',
        expected_output='A detailed text summary of relevant news.',
        agent=researcher
    )

   report_task = Task(
        description=f'''Review the raw research for {company_name}. 
        You MUST output your final analysis strictly as a raw JSON object. Do not include markdown formatting blocks (like ```json).
        
        You must adhere to this exact schema:
        {{
            "company_name": "{company_name}",
            "overall_sentiment_score": <an integer between 0 and 100 based on the news>,
            "sentiment_label": "<Bullish, Bearish, or Neutral>",
            "key_metrics": {{
                "<Metric Name 1 (e.g., Stock Trend)>": "<Value>",
                "<Metric Name 2 (e.g., Market Risk)>": "<Value>",
                "<Metric Name 3 (e.g., Competitor Threat)>": "<Value>"
            }},
            "critical_news": [
                {{"headline": "...", "impact_level": "High/Medium/Low"}}
            ],
            "executive_summary": "<A detailed 2-paragraph markdown summary of the situation>"
        }}''',
        expected_output='A strict JSON object containing the financial analysis.',
        agent=analyst
    )

    # ORCHESTRATE THE CREW
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, report_task],
        process=Process.sequential 
    )

    return crew.kickoff()
