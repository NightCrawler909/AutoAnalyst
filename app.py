import streamlit as st
from dotenv import load_dotenv

# Import Developer 1's backend logic
from crew_logic import run_analysis_crew

# Load environment variables (API keys)
load_dotenv()

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AutoAnalyst | Multi-Agent AI",
    page_icon="📈",
    layout="centered"
)

st.title("📈 AutoAnalyst: Intelligence Briefing")
st.write("Deploy autonomous AI agents to research and synthesize an executive report on any company.")

# ==========================================
# 2. USER INTERFACE
# ==========================================
# Text input for the target company
company_name = st.text_input("Enter Target Company (e.g., Nvidia, Tesla, Stripe):")

# Generate Button
if st.button("Generate Executive Briefing"):
    
    # Input Validation
    if not company_name:
        st.warning("⚠️ Please enter a company name to begin.")
    else:
        # ==========================================
        # 3. BACKEND INTEGRATION & EXECUTION
        # ==========================================
        # The spinner keeps the user engaged while the agents run (takes 1-2 mins)
        with st.spinner(f"Agents deployed. Researching and analyzing {company_name}..."):
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
              
