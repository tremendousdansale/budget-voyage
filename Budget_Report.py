import csv
import json
from trip_budget import show_trip_budget_page

class BudgetReport:
    def __init__(self, destination, total_budget, currency, duration_days, hotel_cost, food_cost, transport_cost):
        self.destination    = destination
        self.total_budget   = total_budget
        self.currency       = currency
        self.duration_days  = duration_days
        self.hotel_cost     = hotel_cost
        self.food_cost      = food_cost
        self.transport_cost = transport_cost

        self.total_spent      = hotel_cost + food_cost + transport_cost
        self.remaining_budget = total_budget - self.total_spent

    def to_dict(self):
        """Converts all the budget data into a dictionary."""
        return {
            "destination":      self.destination,
            "total_budget":     self.total_budget,
            "currency":         self.currency,
            "duration_days":    self.duration_days,
            "hotel_cost":       self.hotel_cost,
            "food_cost":        self.food_cost,
            "transport_cost":   self.transport_cost,
            "total_spent":      self.total_spent,
            "remaining_budget": self.remaining_budget,
        }

    def save_to_json(self, filename="trip_budget.json"):
        """Saves the budget data to a JSON file."""
        with open(filename, "w") as json_file:
            json.dump(self.to_dict(), json_file, indent=4)

    def save_to_csv(self, filename="trip_budget.csv"):
        """Saves the budget data to a CSV file."""
        data = self.to_dict()
        with open(filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    def save_all(self):
        self.save_to_json()
        self.save_to_csv()
