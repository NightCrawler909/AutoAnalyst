import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
from crew_logic import run_analysis_crew

load_dotenv()

st.set_page_config(page_title="AutoAnalyst | Intelligence", page_icon="📈", layout="wide")

st.title("📈 AutoAnalyst: Live Market Intelligence")
st.markdown("---")

company_name = st.text_input("Enter Target Company (e.g., Nvidia, Tesla, Stripe):")

if st.button("Generate Dashboard", type="primary"):
    if not company_name:
        st.warning("⚠️ Please enter a company name.")
    else:
        with st.spinner(f"Agents deployed. Analyzing live data for {company_name}..."):
            try:
                # 1. Get the raw string from the agents
                raw_result = run_analysis_crew(company_name)
                
                # 2. Clean the string (in case the LLM adds markdown backticks) and parse the JSON
                clean_json = str(raw_result).replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_json)

                st.success("Intelligence Gathered Successfully!")
                
                # ==========================================
                # TOP ROW: METRICS & SENTIMENT CHART
                # ==========================================
                st.subheader(f"📊 {data['company_name']} Overview")
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    st.metric(label="Market Sentiment", value=data['sentiment_label'])
                    
                    # Iterate through the dynamic key metrics the AI found
                    for key, value in data['key_metrics'].items():
                        st.metric(label=key, value=value)

                with col3:
                    # Build a dynamic gauge chart based on the AI's sentiment score
                    score = data['overall_sentiment_score']
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        title = {'text': "AI Sentiment Score", 'font': {'size': 20, 'color': 'white'}},
                        gauge = {
                            'axis': {'range': [0, 100], 'tickcolor': "white"},
                            'bar': {'color': "#3b82f6" if score > 50 else "#ef4444"},
                            'steps': [
                                {'range': [0, 40], 'color': "#3f1a1a"},
                                {'range': [40, 60], 'color': "#333333"},
                                {'range': [60, 100], 'color': "#1a3f28"}],
                        }
                    ))
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300)
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # ==========================================
                # BOTTOM ROW: NEWS TABLE & SUMMARY
                # ==========================================
                col_left, col_right = st.columns([1.5, 1])

                with col_left:
                    st.subheader("📰 Critical Market Signals")
                    # Turn the AI's list of news into a clean Pandas dataframe table
                    df = pd.DataFrame(data['critical_news'])
                    st.dataframe(df, use_container_width=True, hide_index=True)

                with col_right:
                    st.subheader("🤖 Executive Briefing")
                    st.info(data['executive_summary'])

            except json.JSONDecodeError:
                st.error("Failed to parse the AI output. The model did not return valid JSON. Please try generating again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
