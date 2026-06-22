import requests
class UnknownCurrency(Exception):
    pass

class CurrencyConverter:
    def __init__(self, USD, NGN, GBP, JPY):
        self.USD = USD
        self.NGN = NGN
        self.GBP = GBP
        self.JPY = JPY
        pass

    def exchange_rates(self):
        url = "https://v6.exchangerate-api.com/v6/2be5e59eb106bfa66422abfd/latest/USD"
        try:
            response = requests.get(url)
            print(response.status_code)
            response.raise_for_status()
            data = response.json()
            conv_rates = data["conversion_rates"]
            print("Currency exchange rates have been successfully retrieved")
        except requests.exceptions.ConnectionError:
            conv_rates = None
            print("Cant connect to network")
        except Exception as e:
            conv_rates = None
            print(f"Error: {e}")

        user_currency = input("Enter the currency currently being used: ")
        user_currency = user_currency.upper().strip()

        accepted_currency = input("Enter the currency accepted in the place of visit: ")
        accepted_currency = accepted_currency.upper().strip()

        if user_currency == "" or accepted_currency == "":
            print("No selected currency")
            return

        try:
            amount = float(input("Enter the amount you want converted: "))
        except ValueError:
            print("Please enter a valid numeric amount.")
            return

        try:
            if conv_rates:
                if user_currency not in conv_rates or accepted_currency not in conv_rates:
                    raise UnknownCurrency(f"Unsupported currency: {user_currency} or {accepted_currency}")

                amount_in_usd = amount / conv_rates[user_currency]
                convert = amount_in_usd * conv_rates[accepted_currency]
                print(f"{amount} {user_currency} = {convert:.2f} {accepted_currency}")
                return

            # Offline fallback
            print("Using offline rates. Available currencies: USD, JPY, GBP, NGN")
            rates = {
                "USD": self.USD,
                "NGN": self.NGN,
                "GBP": self.GBP,
                "JPY": self.JPY,
            }

            if user_currency not in rates or accepted_currency not in rates:
                raise UnknownCurrency(f"Unsupported currency: {user_currency} or {accepted_currency}")

            amount_in_usd = amount / rates[user_currency]
            convert = amount_in_usd * rates[accepted_currency]
            print(f"{amount} {user_currency} = {convert:.2f} {accepted_currency}")
        except UnknownCurrency as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

roll = CurrencyConverter(USD=1, NGN=1357.59, GBP= 0.74, JPY= 160.35)
roll.exchange_rates()

