from bs4 import BeautifulSoup
import urllib.request as req
import time
import os
import sqlite3


#prevents overwriting of data
def clearData():
	conn=sqlite3.connect('internshala.db')
	conn.execute("DELETE from data;")
	conn.commit()
	conn.close()

#prints options for filtering
def printList(domain_list,city_list):
	print("\n")
	print("List of Domains: ")
	for ele in domain_list:
		print(ele,end = "  |  ")
	print("\n")	
	print("List of Cities: ")		
	for ele in city_list:
		print(ele,end = "  |  ")
	print("\n")	

#scrapes header and details for each cell on internshala and inserts into database
def scraper(url,toggle):
	if toggle == True:
		clearData()
	else:
		pass
	#print("Into scraper..")
	print("\nFetching internships from: "+url)

	response = req.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data,"lxml")

	individual_internship_header_list = []
	individual_internship_details_list = []
	base_a_link="https://internshala.com"
	tabular_data = soup.find_all("div", class_="individual_internship_header")
	for new_row in tabular_data:
		int_link = ""
		int_name = ""
		int_company = ""
		cnt = 0
		for row in new_row.find_all("h4"):
			for alink in row.find_all("a"):
				if cnt == 0:
					int_link = base_a_link+str(alink['href']).strip()
					int_name = str(alink.text).strip()
					cnt += 1
				else:
					int_company = str(alink.text).strip()
		individual_internship_header_list.append((int_name,int_link,int_company))
	#print(individual_internship_header_list)

	tabular_data = soup.find_all("div", class_="individual_internship_details")
	for new_row in tabular_data:
		int_startTime = ""
		int_duration = ""
		int_stipend = ""
		int_postedOn = ""
		int_applyBy = ""
		cnt = 0
		row = new_row.find("div",class_="table-responsive")
		row = row.find("table",class_="table")
		row = row.find("tbody")
		row = row.find("tr")
		for ele in row.find_all("td"):
			if cnt == 0:
				int_startTime = str(ele.find("div").text).strip()
			elif cnt == 1:
				int_duration = str(ele.text).strip()
			elif cnt == 2:
				int_stipend = str(ele.text).strip()
			elif cnt == 3:
				int_postedOn = str(ele.text).strip()
			elif cnt == 4:
				int_applyBy = str(ele.text).strip()
				cnt = 0
			cnt += 1
		individual_internship_details_list.append((int_startTime,int_duration,int_stipend,int_postedOn,int_applyBy))
	#print(individual_internship_details_list)

	zipped_data = zip(individual_internship_header_list,individual_internship_details_list)
	internship_data = []
	for ele in zipped_data:
		internship_data.append(ele[0]+ele[1])
	print("\n-----------------------------List of internships---------------------------------\n")

	for ele in internship_data:
		print(ele)
		print("\n")
	
	#insert into database
	try:
		conn = sqlite3.connect('internshala.db')
		table_name = 'data'
		cursor = conn.cursor()
		#cursor.execute('CREATE TABLE {tn} ({n}, {c}, {da}, {du}, {s}, {p}, {a}, {l})'.format(tn = table_name, n='name', c='company', da='date', du='duration', s='stipend', p='postedon', a='applyby', l='link'))
		cursor.execute('''
			CREATE TABLE if not exists data(name TEXT,company TEXT,sdate TEXT,duration TEXT,stipend TEXT,postedon TEXT,applyby TEXT,link TEXT);
			''')
	except Exception as e:
		print(e)

	for value in internship_data:
		name = value[0]
		link = value[1]
		company = value[2]
		date = value[3]
		duration = value[4]
		stipend = value[5]
		postedon = value[6]
		applyby = value[7]
		cursor.execute("INSERT INTO data(name,company,sdate,duration,stipend,postedon,applyby,link) VALUES (?,?,?,?,?,?,?,?);",(name,company,date,duration,stipend,postedon,applyby,link))
	conn.commit()
	conn.close()


#fetches url to scrape depending on the user filters
def getInternshipURL(toggle):
	

	domain_list = ['computer_science','finance','marketing','hr','digital_marketing','civil','content_writing','electronics']
	city_list = ['mumbai','delhi','chennai','hyderabad','pune','bangalore','kolkata','jaipur']

	printList(domain_list,city_list)

	base_url = "https://internshala.com/internships/"
	cinput = int(input("Enter your internship filtering criteria:\n\n1. Domain \n2. City\n3. Domain and City\n"))


	if cinput == 1:
		choice1 = str(input("\nEnter domain: "))
		choice1 = ' '.join(choice1.split())
		whitespace_removed = choice1.strip()
		whitespace_replaced = whitespace_removed.replace(" ", "_")
		lower_string = whitespace_replaced.lower()
		#print(lower_string)
		if lower_string in domain_list:
				print("\nDomain Exists..")
				if lower_string == "computer_science" or lower_string == "digital_marketing" or lower_string == "content_writing":
					request_string = lower_string.replace("_","%20")
					#print(request_string)
					complete_url  = base_url + request_string + "-internship"
					scraper(complete_url,toggle)
				else:
					complete_url  = base_url + lower_string + "-internship"
					scraper(complete_url,toggle)
		else:
			print("\nDomain Doesnt Exist.!")
			print("Quitting..")
			time.sleep(1)
			exit()
 
	elif cinput == 2:
		choice2 = str(input("\nEnter city: "))
		choice2 = ' '.join(choice2 .split())
		whitespace_removed = choice2.strip()
		whitespace_replaced = whitespace_removed.replace(" ", "_")
		lower_string = whitespace_replaced.lower()
		#print(lower_string)
		if lower_string in city_list:
				print("\nCity Exists..")
				complete_url  = base_url + "internship-in-" + lower_string
				scraper(complete_url,toggle)
		else:
			print("\nCity Doesn't Exist.!")
			print("Quitting..")
			time.sleep(1)
			exit()
		
	elif cinput == 3:
		choice3a = str(input("\nEnter domain: "))
		choice3b = str(input("\nEnter city: "))
		choice3a = ' '.join(choice3a.split())
		choice3b = ' '.join(choice3b.split())
		whitespace_removeda = choice3a.strip()
		whitespace_replaceda = whitespace_removeda.replace(" ", "_")
		lower_stringa = whitespace_replaceda.lower()
		whitespace_removedb = choice3b.strip()
		whitespace_replacedb = whitespace_removedb.replace(" ", "_")
		lower_stringb = whitespace_replacedb.lower()
		#print(lower_stringa)
		#print(lower_stringb)

		if lower_stringa in domain_list and lower_stringb in city_list:
				print("\nCity and Domain Exists..")
				if lower_stringa == "computer_science" or lower_stringa == "digital_marketing" or lower_stringa == "content_writing":
					request_string = lower_stringa.replace("_","%20")
					#print(request_string)
					complete_url  = base_url + request_string + "-internship-in-" + lower_stringb
					scraper(complete_url,toggle)
				else:
					complete_url  = base_url + lower_stringa + "-internship-in-" + lower_stringb
					scraper(complete_url,toggle)
		else:
			print("\nCity Doesn't Exist.!")
			print("Quitting..")
			time.sleep(1)
			exit()

	else:
		print("Showing results without filters..")
		getInternshipURL("")


def main():
	db = "internshala.db"
	path_to_db = os.getcwd()+"/"+ db
	if os.path.exists(path_to_db):
		getInternshipURL(True)
	else:
		getInternshipURL(False)

if __name__ == '__main__':
	main()