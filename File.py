import os
import json
from trip_budget import TripBudget
class BudgetReport:
    def __init__(self):
        self.budget = TripBudget()
    def save_budget(self):
        try:
            filename = "Budget_Report.json"
            with open(filename, "w", encoding = "utf-8") as f:
                json.dump(self.budget.__dict__, f, indent=4)
            print(f"Budget report saved to {filename} successfully.")
        except Exception as e:
            print(f"Error occurred while saving budget report: {e}")
    
    def load_budget(self):
        try:
            filename = "Budget_Report.json"
            if not os.path.exists(filename):
                print(f"No budget report found at {filename}.")
                return
            with open(filename, "r", encoding = "utf-8") as f:
                data = json.load(f)
                self.budget = TripBudget(data["destination"], data["days"])
                self.budget.hotel_cost = data["hotel_cost"]
                self.budget.food_cost = data["food_cost"]
                self.budget.transport_cost = data["transport_cost"]
            print(f"Budget report loaded from {filename} successfully.")
        except FileNotFoundError:
            print(f"Budget report file not found: {filename}")
        except Exception as e:
            print(f"Error occurred while loading budget report: {e}")