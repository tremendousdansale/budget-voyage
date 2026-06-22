import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from trip_budget import show_trip_budget_page
from travel_advisor import TravelAdvisor

st.set_page_config(page_title="Currency and Travel Budget Planner")

st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Choose a section",
    ["Travel Budget Planner", "Currency Converter"],
)

if page == "Travel Budget Planner":
    # Render the input fields page
    show_trip_budget_page()
   
    # Check if the user has clicked "Calculate Budget"
    if st.session_state.get("budget_calculated", False):
        st.markdown("---")
        st.subheader("🤖 AI Travel Advisor Insights")
       
        # Read the real-time dynamic entries from session state
        live_city = st.session_state["destination"]
       
        with st.spinner(f"Consulting Gemini AI for {live_city}..."):
            try:
                advisor = TravelAdvisor()
               
                # Fire the exact dynamic data straight to Gemini
                ai_insights = advisor.generate_advice(
                    destination=live_city,
                    total_budget=float(st.session_state["total_budget"]),
                    currency=st.session_state["currency"],
                    duration_days=int(st.session_state["duration_days"]),
                    remaining_budget=float(st.session_state["remaining_budget"]),
                    total_spent=float(st.session_state["total_spent"]),
                    expense_summary=st.session_state["expense_summary"]
                )
                st.info(ai_insights)
               
            except Exception as e:
                st.error(f"Could not load AI Insights: {e}")

else:
    st.title("Currency Converter")
    st.info("Currency converter section will be added by the currency developer.")