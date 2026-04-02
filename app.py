import streamlit as st
from dotenv import load_dotenv
import os

# Import Developer 1's backend logic
# (This will work once Dev 1 uploads crew_logic.py to the repo)
from crew_logic import run_analysis_crew

# Load environment variables (API keys)
load_dotenv()

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AutoAnalyst | Multi-Agent AI",
    page_icon="📈",
    layout="centered"
)

st.title("📈 AutoAnalyst: Intelligence Briefing")
st.write("Deploy autonomous AI agents to research and synthesize an executive report on any company.")
st.markdown("---")

# ==========================================
# USER INTERFACE
# ==========================================
# Text input for the target company
company_name = st.text_input("Enter Target Company (e.g., Nvidia, Tesla, Stripe):")

# Generate Button
if st.button("Generate Executive Briefing", type="primary"):
    
    # Input Validation
    if not company_name:
        st.warning("⚠️ Please enter a company name to begin.")
    else:
        # ==========================================
        # BACKEND INTEGRATION & EXECUTION
        # ==========================================
        # The spinner keeps the user engaged while the agents run
        with st.spinner(f"Deploying agents... Researching and analyzing {company_name}. This takes 1-2 minutes."):
            try:
                # Call Developer 1's function
                final_report = run_analysis_crew(company_name)
                
                # Render the final output
                st.success("Analysis Complete!")
                st.markdown("---")
                
                # Streamlit natively renders markdown strings beautifully
                st.markdown(final_report)
                
            except Exception as e:
                # Catch API errors, missing keys, or timeouts
                st.error(f"An error occurred during execution: {e}")
                st.info("Troubleshooting: Ensure Developer 1 has uploaded crew_logic.py and your API keys are correct in the secrets menu.")
