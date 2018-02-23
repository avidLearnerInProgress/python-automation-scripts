from selenium import webdriver
import getpass
import time

username = "#####"
password = getpass.getpass("Password: ")
problem = input("Problem code: ")
submission_file = input("Submission file: ")

with open(submission_file, 'r') as f:
	code = f.read()

browser = webdriver.Firefox()
browser.get('httpswww.codechef.com')

nameElem = browser.find_element_by_id('edit-name')
nameElem.send_keys(username)
passElem = browser.find_element_by_id('edit-pass')
passElem.send_keys(password)

browser.find_element_by_id('edit-submit').click()
browser.get("https://www.codechef.com/submit"+problem)
time.sleep(10)
browser.find_element_by_id(edit_area_toggle_checkbox_edit-program).click()

inputElem = browser.find_element_by_id('edit-program')
inputElem.send_keys(code)

browser.find_element_by_id(edit-submit).click()
result = browser.find_element_by_id(display_result).text
print(result)