import requests
import datetime
class Holiday_checker:
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

Check = Holiday_checker()
country_code = input("Enter the country code(e.g NG, US, GB): ").upper().strip()
trip_date = input("Enter the travel date (YYYY-MM-DD): ")
Check.main(country_code, trip_date)