import requests
import datetime
import streamlit as st
class Holiday_checker:
    def show_holiday_checker_page(self):
        st.title("Holiday Checker")
        country_code = st.text_input("Enter country code (e.g US, NG, GB):", value = "")
        trip_date = st.text_input("Enter the travel date (YYYY-MM-DD): ", value="")
        if st.button("Check Holiday"):
            if country_code == "" or trip_date == "":
                st.warning("Please fill in both the country code and trip date")
                return
            if not self.validate_date(trip_date):
                st.error("Invalid date format. Please use YYYY-MM-DD e.g 2025-06-28")
                return
            days = self.days_until_trip(trip_date)
            if days < 0:
                st.error("The date selected has already passed.")
                return
            holiday = self.check_holiday(country_code, trip_date)
            if holiday:
                st.warning("The selected date is a public holiday")
            else:
                st.success("The selected date is not on a public holiday ")

    def validate_date(self, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def days_until_trip(self, trip_date):
        today = datetime.datetime.today()
        trip = datetime.datetime.strptime(trip_date, "%Y-%m-%d")
        difference = trip - today
        return difference.days
    
    def check_holiday(self, country_code, trip_date):
        year = trip_date.split("-")[0]
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                holidays = response.json()
                for holiday in holidays:
                    if holiday["date"] == trip_date:
                        return holiday["localName"]
                return None
            else:
                print("Unable to retrieve holiday information")
                return None
        except Exception as e:
            print("An error occurred: {e}")
            return None
    
    def main(self, country_code, trip_date):
        if not self.validate_date(trip_date):
            print("Invalid Date. Please use format YYYY-MM-DD e.g 2025-12-25")
            days = self.days_until_trip(trip_date)
            if days < 0:
                print("The date selected has already passed.")
                return
            print(f"Your trip is in {days} days.")
            holiday = self.check_holiday(country_code, trip_date)
            if holiday:
                print("The selected date is a public holiday")
            else:
                print("The selected date is not on a public holiday ")
        
