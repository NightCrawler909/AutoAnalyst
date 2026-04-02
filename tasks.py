from crewai import Task

class CompanyAnalysisTasks:
    def research(self, agent, company_name):
        return Task(
            description=f'Conduct comprehensive web research on {company_name}. Find the most recent news, market shifts, and overall sentiment.',
            expected_output='A detailed, bulleted summary of key market findings, recent events, and relevant financial data points.',
            agent=agent
        )

    def analyze(self, agent, company_name):
        return Task(
            description=f'Analyze the raw research provided. Synthesize this data into a structured financial briefing on {company_name}.',
            expected_output='A professional markdown report with clear headings, actionable bullet points, and a dedicated section for potential risk factors.',
            agent=agent
        )
