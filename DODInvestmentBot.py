#Created by Kenny Grossman July, 2019
#This project is intended to be used for interview purposes only
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
Helper Functions 
'''
#Function for more visible test headers
def printTestName(message):
	bufferTiles = 24 - (int)(len(message)/2)
	print("\n###################################################")
	print(bufferTiles*"#",message, bufferTiles*"#")
	print("###################################################")

#Clear screen to prep for testing
def testCleanup():
	clearButton.click()

#Search string using program search return boolean value
def programSearch(searchString):
	programSearchBox.send_keys(searchString)
	searchButton.click()

	#Wait for search results to appear
	try:
		#TODO: MAKE THIS WORK ON SINGLE PAGE RESULTS
	    element = WebDriverWait(driver, 5).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'record-listing'))
	    )
	except:
		return False
	else:
		return True

#Grab all search results from all pages and return list of objects
def collectSearchResults(searchString):
	if (programSearch(searchString)):
		try:
			nextPageButtonContainer = driver.find_element(By.XPATH, '/html/body/div[3]/div/ng-include/div/dir-pagination-controls[1]/div/ul/li[5]')
			nextPageButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/ng-include/div/dir-pagination-controls[1]/div/ul/li[5]/a')
		except:
			pass

		searchResults = []

		#Loop through all pages
		hasNextPage = True
		while(hasNextPage):
			#Grab all results and add to searchResult list
			tempResults = driver.find_elements(By.CLASS_NAME, 'record-listing')

			for result in tempResults:
				searchResults.append(result.get_property('innerText'))

			#Determine if another page exists
			try:
				buttonClasses = nextPageButtonContainer.get_attribute( "class" ).split(' ')
				hasNextPage = "disabled" not in buttonClasses
			except:
				hasNextPage = False
			
			if(hasNextPage):
				nextPageButton.click()
				time.sleep(.5)

		return searchResults
	else:
		print('Fail: no search results found')
		return []

'''
Helper functions that have not yet been implemented
'''
def revealAndClickBudetOptions():
	#Reveal Drop down for budget 
	budgetYearsDropDownButton.click()

	#Print and click all buttons in drop down
	for element in budgetYearsDropDownItems:
		print(element.get_property("outerText"))
		element.click()

def revealAndClickBudetOptions():
	#Reveal Drop down for agencies
	agenciesYearsDropDownButton.click()

	#Print and click all buttons in drop down
	for element in agenciesYearsDropDownItems:
		print(element.get_property("outerText"))
		element.click()	

'''
Test Functions
'''
def testSuite(searchString):
	searchTest(searchString)
	searchCorrectnessTest(searchString)
	validateNumberofResults(searchString)
	validateLinkAccuracy(searchString)
	clearButtonTest()

#Attempt to search in program element number search field
def searchTest(searchString):
	testCleanup()
	printTestName('Starting Search Test')
	
	if (programSearch(searchString)):
		resultsValue = int(resultsNumber.get_property("outerText").strip("Results: "))
		print('Pass: Search provided {} results'.format(resultsValue))
	else:
		print('Fail: no search results found')

#Check if search string appears in the Program Element number field of all results
def searchCorrectnessTest(searchString):
	testCleanup()
	printTestName('Starting Search Correctness Test')

	searchResults = collectSearchResults(searchString)

	#Loop through search results to verify search String appears in each result
	testPassed = True if len(searchResults) > 0 else False;	

	for result in searchResults:
		# print('Result: {}'.format(result.get_property('innerText')))
		if searchString not in result:
			testPassed = False

	#Print test results
	if testPassed:
		print('Pass: Search term found in all results')
	else:
		print('Fail: Search term did not appear in all results')

#Ensure the correct number of results appear
def validateNumberofResults(searchString):
	testCleanup()
	printTestName('Starting Validate Number of Results Test')	
	searchResults = collectSearchResults(searchString)
	
	#Strip "Results: " from string leaving only the integer
	resultsValue = int(resultsNumber.get_property("outerText").strip("Results: "))
	
	testPassed = True if resultsValue == len(searchResults) else False
	print('Found {} results and expected {} results'.format(len(searchResults), resultsValue))

	#Print test results
	if testPassed:
		print('Pass: Number of results are accurate')
	else:
		print('Fail: Search provided a different number of results than expected')	

#Validate that links on page match filenames
def validateLinkAccuracy(searchString):
	printTestName('Validate links match filenames')	
	testCleanup()
	searchResults = collectSearchResults(searchString)
	

#Ensure clear button clears text field and results
def clearButtonTest():
	printTestName('Test Clear Button functionality')	
	testCleanup()
	if programSearchBox.get_property("value") == "" and resultsNumber.get_property("outerText") == "Results: ":
		testPassed = True
	else:
		testPassed = False

	#Print test results
	if testPassed:
		print('Pass: Clear Button Successfully cleared program element number search field')
	else:
		print('Fail: Clear Button did not reset some elements')	

'''
Main Body
'''
#Add location of downloaded selenium chrome driver
#Drivers can be found at https://www.seleniumhq.org/download/
driverPath = '/Users/kennygrossman/Projects/Bots/Drivers/chromedriver'
URL = 'https://apps.dtic.mil/dodinvestment/#/advancedSearch'
webpageTimeout = 30
searchString = '0603680F'

#Initialize Chrome driver and load webpage
driver = webdriver.Chrome(driverPath)
driver.get(URL)

#Wait for page and searchfield to load before proceeding
try:
    element = WebDriverWait(driver, webpageTimeout).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="budgetNumObj_value"]'))
    )
except:
	print("Failed to load webpage")
else:
	#Identify page objects for later use
	searchButton = driver.find_element(By.XPATH, '//*[@id="performSearch"]')
	clearButton = driver.find_element(By.XPATH, '//*[@id="clearSearch"]')
	programSearchBox = driver.find_element(By.XPATH, '//*[@id="budgetNumObj_value"]')
	resultsNumber = driver.find_element(By.XPATH, '//*[@id="navbarCollapse"]/ul/li[2]/a/strong')
	budgetYearsDropDownButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[1]/am-multiselect/div/button')
	budgetYearsDropDownItems = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[1]/am-multiselect/div/ul').get_property("children")
	agenciesYearsDropDownButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[2]/am-multiselect/div/button')
	agenciesYearsDropDownItems = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[2]/am-multiselect/div/ul').get_property("children")

	#Run Test Suite
	testSuite(searchString)
	