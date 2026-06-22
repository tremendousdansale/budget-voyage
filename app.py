import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from trip_budget import show_trip_budget_page


st.set_page_config(page_title="Currency and Travel Budget Planner")

st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Choose a section",
    ["Travel Budget Planner", "Currency Converter"],
)

if page == "Travel Budget Planner":
    show_trip_budget_page()
else:
    st.title("Currency Converter")
    st.info("Currency converter section will be added by the currency developer.")
