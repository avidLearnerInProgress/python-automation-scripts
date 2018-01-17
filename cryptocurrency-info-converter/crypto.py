from bs4 import BeautifulSoup
from urllib.request import urlopen as req
import json,csv
import pandas as pd


def getJSONResponse(extension):

	base_url = 'https://min-api.cryptocompare.com/data/'
	complete_url = base_url + extension

	response = req(complete_url)
	data = response.read()
	soup = BeautifulSoup(data,"html.parser")
	json_data = json.loads(str(soup))
	return json_data


def getAllCoinDetails():
	coinlist = []
	all_coins = getJSONResponse('all/coinlist')
	data_coins = all_coins['Data']
	print(len(data_coins))
	cnt = 1
	#print(data_coins)
	for coin_details in data_coins:
		for k,v in data_coins[coin_details].items():
			if k == 'CoinName':
				coin_name = str(v)
			if k == 'FullName':
				coin_full_name = str(v)
			if k == 'Algorithm':
				coin_algorithm = str(v)
			if k == 'ProofType':
				coin_prooftype = str(v)
			if k == 'TotalCoinSupply':
				coin_tcs = str(v)

		each_coin_detail = [coin_name,coin_full_name,coin_algorithm,coin_prooftype,coin_tcs]
		print(cnt)
		print(each_coin_detail)
		coinlist.append(each_coin_detail)
		cnt += 1
	
	my_df = pd.DataFrame(coinlist)
	my_df.to_csv('my_csv.csv', index=False, header=['Coin Name','Complete Name','Algorithm','Proof Type','Total Coin Supply'])
	

	'''coin_name = coin[5]
	coin_full_name = coin.get('FullName')
	coin_algorithm = coin.get('Algorithm')
	coin_pot = coin.get('ProofOfType')
	print(coin_name)
	print(coin_full_name)
	print(coin_algorithm)
	print(coin_pot)
	break'''

def getCryptoPriceInOtherCurrency():

	print("\nConverts 1 unit of currency to another currency.")
	print("\nExample: 1 BTC EQUALS ? in USD.")
	#https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR
	fromsystem = str(input("\nEnter input currency symbol: ").upper())
	tosys_num = int(input("\nEnter number of output currencies: "))
	tosys_str = ""
	print("\nEnter output currency symbols: ")
	for i in range(tosys_num):
		name = str(input("").upper())
		tosys_str += name
		tosys_str += ","
	tosystems = tosys_str.rstrip(',')
	try:
		data = getJSONResponse('price?fsym=' + fromsystem + "&tsyms=" + tosystems)
		for k,v in data.items():
			value = str(k)
			print("\n1 " + fromsystem + " equals " ,str(v) + " " ,str(k))
	except Exception as e:
		print("Error." + str(e))
  

def getMatrixCurrencyPrices():

	print("\nConverts 1 unit of currency to another currency.")
	print("\nExample: 1 BTC EQUALS ? in USD.")
	#https://min-api.cryptocompare.com/data/price?fsym=ETH,DASH&tsyms=BTC,USD,EUR

	fromsys_num = int(input("\nEnter number of input currencies: "))
	fromsys_str = ""
	print("\nEnter input currency symbols: ")
	for i in range(fromsys_num):
		name = str(input("").upper())
		fromsys_str += name
		fromsys_str += ","
	fromsystems = fromsys_str.rstrip(',')
	
	print(fromsystems)

	tosys_num = int(input("\nEnter number of output currencies: "))
	tosys_str = ""
	print("\nEnter output currency symbols: ")
	for i in range(tosys_num):
		name = str(input("").upper())
		tosys_str += name
		tosys_str += ","
	tosystems = tosys_str.rstrip(',')

	try:
		data = getJSONResponse('pricemulti?fsyms=' + fromsystems + "&tsyms=" + tosystems)
		for ele in data:
			print("\n1 "+ ele + " equals: ")	
			for k,v in data[ele].items():
				print("\n" ,str(v) + " " ,str(k))
			
	except Exception as e:
		print("Error." + str(e))


def main():
	
	a = '''1. List all coin details and export it to csv.\n2. Convert one cryptocurrency to other currencies.\n23. Convert multiple cryptocurrencies to other currencies.'''
	print(a)

	choice = int(input("\nEnter choice:\n"))

	if choice == 1:
		getAllCoinDetails()
	if choice == 2:
		getCryptoPriceInOtherCurrency()
	if choice == 3:
		getMatrixCurrencyPrices()
	


if __name__ == '__main__':
	main()