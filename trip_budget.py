import streamlit as st

def show_trip_budget_page():
    st.title("Travel Budget Planner")
   
    # 1. Completely Blank Live Input Fields
    destination = st.text_input("Destination City:", value="")
    total_budget = st.number_input("Total Budget:", min_value=0.0, value=0.0)
    currency = st.selectbox("Currency:", ["NGN", "USD", "GBP", "EUR", "CAD"])
    duration_days = st.number_input("Number of Days:", min_value=1, value=1)
   
    st.subheader("Estimated Expenses")
    hotel_cost = st.number_input("Hotel Cost:", min_value=0.0, value=0.0)
    food_cost = st.number_input("Food Cost:", min_value=0.0, value=0.0)
    transport_cost = st.number_input("Transport Cost:", min_value=0.0, value=0.0)
   
    if st.button("Calculate Budget"):
        # If the user clicks calculate without entering a city, give them a warning
        if not destination.strip():
            st.warning("Please enter a destination city first!")
            return
           
        total_spent = hotel_cost + food_cost + transport_cost
        remaining_budget = total_budget - total_spent
       
        # Save EVERYTHING globally so your AI module can read it instantly
        st.session_state["destination"] = destination
        st.session_state["total_budget"] = total_budget
        st.session_state["currency"] = currency
        st.session_state["duration_days"] = duration_days
        st.session_state["total_spent"] = total_spent
        st.session_state["remaining_budget"] = remaining_budget
        st.session_state["expense_summary"] = {
            "Hotel": hotel_cost,
            "Food": food_cost,
            "Transport": transport_cost
        }
        st.session_state["budget_calculated"] = True
       
        # Display baseline math results to user
        st.markdown("---")
        st.subheader("Budget Breakdown")
        st.write(f"**Destination:** {destination}")
        st.write(f"**Total Spent:** {total_spent:,.2f} {currency}")
        st.write(f"**Remaining Balance:** {remaining_budget:,.2f} {currency}")