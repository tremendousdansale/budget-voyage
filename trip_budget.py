class TripBudget:
    """Calculate the estimated budget for a trip."""

    def __init__(self, destination, days):
        self.destination = destination
        self.days = self._validate_days(days)

        self.hotel_cost = 0.0
        self.food_cost = 0.0
        self.transport_cost = 0.0

    def _validate_days(self, days):
        if days <= 0:
            raise ValueError("Trip days must be greater than zero.")
        return days

    def _validate_cost(self, amount, cost_name):
        if amount < 0:
            raise ValueError(f"{cost_name} cannot be negative.")
        return float(amount)

    def set_hotel_cost(self, cost_per_night):
        cost_per_night = self._validate_cost(cost_per_night, "Hotel cost")
        self.hotel_cost = cost_per_night * self.days

    def set_food_cost(self, cost_per_day):
        cost_per_day = self._validate_cost(cost_per_day, "Food cost")
        self.food_cost = cost_per_day * self.days

    def set_transport_cost(self, transport_cost):
        self.transport_cost = self._validate_cost(transport_cost, "Transport cost")

    def total_trip_cost(self):
        return self.hotel_cost + self.food_cost + self.transport_cost

    def total_budget(self):
        return self.total_trip_cost()

    def daily_budget(self):
        return self.total_trip_cost() / self.days

    def _daily(self):
        return self.daily_budget()

    def budget_breakdown(self):
        return {
            "destination": self.destination,
            "days": self.days,
            "hotel_cost": self.hotel_cost,
            "food_cost": self.food_cost,
            "transport_cost": self.transport_cost,
            "total_trip_cost": self.total_budget(),
            "daily_budget": self._daily(),
        }

    def display_budget(self):
        breakdown = self.budget_breakdown()

        print("TRIP BUDGET ESTIMATE")
        print("--------------------")
        print(f"Destination: {breakdown['destination']}")
        print(f"Days: {breakdown['days']}")
        print(f"Hotel cost: {breakdown['hotel_cost']:.2f}")
        print(f"Food cost: {breakdown['food_cost']:.2f}")
        print(f"Transport cost: {breakdown['transport_cost']:.2f}")
        print(f"Total trip cost: {breakdown['total_trip_cost']:.2f}")
        print(f"Daily budget: {breakdown['daily_budget']:.2f}")


def show_trip_budget_page():
    import streamlit as st

    st.title("Travel Budget Planner")
    st.write("Estimate hotel, food, transport, total trip cost, and daily spending limit.")

    destination = st.text_input("Destination", placeholder="Example: Lagos")
    days = st.number_input("Number of trip days", min_value=1, value=1, step=1)

    st.subheader("Trip Costs")
    hotel_cost_per_night = st.number_input(
        "Hotel cost per night",
        min_value=0.0,
        value=0.0,
        step=1000.0,
    )
    food_cost_per_day = st.number_input(
        "Food cost per day",
        min_value=0.0,
        value=0.0,
        step=500.0,
    )
    transport_cost = st.number_input(
        "Total transport cost",
        min_value=0.0,
        value=0.0,
        step=1000.0,
    )

    if st.button("Calculate Budget"):
        if not destination.strip():
            st.error("Please enter your travel destination.")
            return

        trip = TripBudget(destination.strip(), days)
        trip.set_hotel_cost(hotel_cost_per_night)
        trip.set_food_cost(food_cost_per_day)
        trip.set_transport_cost(transport_cost)
        breakdown = trip.budget_breakdown()

        st.success("Budget calculated successfully.")

        col1, col2 = st.columns(2)
        col1.metric("Total Trip Cost", f"{breakdown['total_trip_cost']:,.2f}")
        col2.metric("Daily Spending Limit", f"{breakdown['daily_budget']:,.2f}")

        st.subheader("Budget Breakdown")
        st.write(f"Destination: {breakdown['destination']}")
        st.write(f"Number of days: {breakdown['days']}")
        st.write(f"Hotel cost: {breakdown['hotel_cost']:,.2f}")
        st.write(f"Food cost: {breakdown['food_cost']:,.2f}")
        st.write(f"Transport cost: {breakdown['transport_cost']:,.2f}")


if __name__ == "__main__":
    show_trip_budget_page()
