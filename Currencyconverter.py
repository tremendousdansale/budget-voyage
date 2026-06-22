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
            user_currency = input("Enter the currency currently being used: ")
            user_currency= user_currency.upper().strip()

            accepted_currency = input("Enter the currency accepted in the place of visit: ")
            accepted_currency = accepted_currency.upper().strip()
            amount = float(input("Enter the amount you want converted: "))

            if user_currency == "" or accepted_currency == "":
                print("No selected currency")
            amount_in_usd = amount / conv_rates[user_currency]
            convert = amount_in_usd * conv_rates[accepted_currency]

            if user_currency in conv_rates or accepted_currency in conv_rates:
                    print(f"{amount} {user_currency} = {convert:.2f} {accepted_currency}")
        except user_currency not in conv_rates or accepted_currency not in conv_rates:
            raise UnknownCurrency
        except requests.exceptions.ConnectionError:
            while True:
                print("Cant connect to network")
                prompt = input("Would you like to use our offline services, yes/no: ")
                prompt = prompt.lower().strip()
                if prompt == "yes":
                    print("The only available currencies are USD, JPY, GBP, NGN")
                    user_currency = input("Enter the currency currently being used: ")
                    user_currency= user_currency.upper().strip()

                    accepted_currency = input("Enter the currency accepted in the place of visit: ")
                    accepted_currency = accepted_currency.upper().strip()
                    amount = float(input("Enter the amount you want converted: "))

                    if user_currency == "" or accepted_currency == "":
                        print("No selected currency")
                    rates = {
                    "USD": self.USD,
                    "NGN": self.NGN,
                    "GBP": self.GBP,
                    "JPY": self.JPY
                    }
                    amount_in_usd = amount / rates[user_currency]
                    convert = amount_in_usd * rates[accepted_currency]
                    try:
                        if user_currency not in rates or accepted_currency not in rates:
                            raise UnknownCurrency
                        if user_currency in rates or accepted_currency in rates:
                            print(f"{amount} {user_currency} = {convert:.2f} {accepted_currency}")
                    except Exception as e:
                        print(f"Error: {e}")
                elif prompt == "no":
                    print("Thank you")
                    break
                else:
                    print("Incorrect response. Please answer with a yes/no")
        except Exception as e:
            print(f"Error: {e}")

c = CurrencyConverter(USD=1, NGN=1357.59, GBP= 0.74, JPY= 160.35)
c.exchange_rates()