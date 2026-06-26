import streamlit as st
import requests
from dotenv import load_dotenv
import os
from holiday_tracker import Holiday_checker

# Load environment variables (make sure GEMINI_API_KEY is in your .env file)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from trip_budget import show_trip_budget_page
from travel_advisor import TravelAdvisor

# -------------------- Streamlit Config --------------------
st.set_page_config(page_title="Currency and Travel Budget Planner")

st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Choose a section",
    ["Travel Budget Planner", "Currency Converter", "Holiday Tracker"],
)

# -------------------- Currency Converter --------------------
CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "NGN", "CAD", "AUD",
    "CHF", "CNY", "KES", "GHS", "ZAR",
]

def show_currency_converter_page():
    st.title("Currency Converter")
    st.write("Convert between currencies using live exchange rates.")

    col1, col2 = st.columns(2)
    from_currency = col1.selectbox("From currency", CURRENCIES, index=CURRENCIES.index("USD"))
    to_currency = col2.selectbox("To currency", CURRENCIES, index=CURRENCIES.index("NGN"))
    amount = st.number_input("Amount", min_value=0.0, value=1.0, format="%.2f")

    if st.button("Convert"):
        if from_currency == to_currency:
            st.success(f"{amount:,.2f} {from_currency} = {amount:,.2f} {to_currency}")
            return

        url = f"https://v6.exchangerate-api.com/v6/2be5e59eb106bfa66422abfd/latest/{from_currency}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            rates = data.get("conversion_rates", {})

            if to_currency not in rates:
                raise ValueError(f"{to_currency} is not available in the exchange rates.")

            converted_amount = amount * rates[to_currency]
            st.success(f"{amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}")
            st.write(f"Exchange rate: 1 {from_currency} = {rates[to_currency]:,.4f} {to_currency}")

        except requests.exceptions.RequestException:
            st.error("Unable to fetch exchange rates. Please check your internet connection.")
        except ValueError as err:
            st.error(str(err))
        except Exception as err:
            st.error(f"An unexpected error occurred: {err}")
# -------------------- Travel Budget Planner --------------------
if page == "Travel Budget Planner":
    show_trip_budget_page()

    # Only show AI Advisor if budget is calculated
    if st.session_state.get("budget_calculated", False):
        st.markdown("---")
        st.subheader("🤖 AI Travel Advisor Insights")

        destination = st.session_state.get("destination", "Unknown")
        try:
            advisor = TravelAdvisor(api_key=GEMINI_API_KEY)  # Pass Gemini API key here
            ai_insights = advisor.generate_advice(
                destination=destination,
                total_budget=float(st.session_state.get("total_budget", 0)),
                currency=st.session_state.get("currency", "USD"),
                duration_days=int(st.session_state.get("duration_days", 1)),
                remaining_budget=float(st.session_state.get("remaining_budget", 0)),
                total_spent=float(st.session_state.get("total_spent", 0)),
                expense_summary=st.session_state.get("expense_summary", {}),
            )
            st.info(ai_insights)
        except Exception as e:
            st.error(f"Could not load AI Insights: {e}")

elif page == "Holiday Checker":
    checker = Holiday_checker()
    checker.show_holiday_checker_page()
    
else:
    show_currency_converter_page()
