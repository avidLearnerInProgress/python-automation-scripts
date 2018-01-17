import requests

def convert():

	print("Enter currency denomination like 'INR' for Indian Rupee.")
	currencies = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]
	print("Supported currencies are: ")
	for ele in currencies:
		print(ele,end=' | ')

	amount = float(input("\n\nEnter amount: "))
	from_currency = str(input("\n\nEnter currency from: ").upper())
	to_currency = str(input("\n\nEnter currency to: ").upper())

	url = 'http://api.fixer.io/latest?base=' + from_currency

	if from_currency in currencies and to_currency in currencies:
		if from_currency != to_currency:
			req = requests.get(url).json()
			exchange_rates = req['rates'][to_currency]
			#print(exchange_rates)
			converted_amount = str(round(float(amount)*exchange_rates,2))
			print("\nConverted amount is: " + converted_amount + " " + str(to_currency))
		else:
			print("\nFrom and To currencies match! Conversion not possible.")
	else:
		print("\nNo support for given currencies")

def main():
	convert()


if __name__ == '__main__':
	main()
	
