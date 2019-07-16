#Created by Kenny Grossman July, 2019
#This project is intended to be used for interview purposes only
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Function for more visible test headers
def printTestName(message):
	bufferTiles = 24 - (int)(len(message)/2)
	print("\n###################################################")
	print(bufferTiles*"#",message, bufferTiles*"#")
	print("###################################################")

#Clear screen to prep for testing
def testCleanup():
	clearButton.click()
	# print("Clearing screen for next test")

#Search string using program search return boolean value
def programSearch(searchString):
	programSearchBox.send_keys(searchString)
	searchButton.click()

	#Wait for search results to appear
	try:
	    element = WebDriverWait(driver, 5).until(
	        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/ng-include/div/dir-pagination-controls[1]/div/ul/li[3]/a'))
	    )
	except:
		return False
	else:
		return True

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

	if (programSearch(searchString)):
		nextPageButtonContainer = driver.find_element(By.XPATH, '/html/body/div[3]/div/ng-include/div/dir-pagination-controls[1]/div/ul/li[5]')
		nextPageButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/ng-include/div/dir-pagination-controls[1]/div/ul/li[5]/a')
		searchResults = []

		#Loop through all pages
		hasNextPage = True
		while(hasNextPage):
			#Grab all results and add to searchResult list
			searchResults.extend(driver.find_elements(By.CLASS_NAME, 'record-listing'))
			
			#Determine if another page exists
			buttonClasses = nextPageButtonContainer.get_attribute( "class" ).split(' ')
			hasNextPage = "disabled" not in buttonClasses
			
			if(hasNextPage):
				nextPageButton.click()

		#Loop through search results to verify search String appears in each result
		testPassed = True;	
		for result in searchResults:
			if searchString not in result.get_property('innerText'):
				testPassed = False

		#Print test results
		if testPassed:
			print('Pass: Search term found in all results')
		else:
			print('Fail: Search term did not appear in all results')
	else:
		print('Fail: no search results found')


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
	driver.dispose()
else:
	#Identify page objects for later use
	searchButton = driver.find_element(By.XPATH, '//*[@id="performSearch"]')
	clearButton = driver.find_element(By.XPATH, '//*[@id="clearSearch"]')
	programSearchBox = driver.find_element(By.XPATH, '//*[@id="budgetNumObj_value"]')
	resultsNumber = driver.find_element(By.XPATH, '//*[@id="navbarCollapse"]/ul/li[2]/a/strong')
	# budgetYearsDropDownButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[1]/am-multiselect/div/button')
	# budgetYearsDropDownItems = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[1]/am-multiselect/div/ul').get_property("children")
	# agenciesYearsDropDownButton = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[2]/am-multiselect/div/button')
	# agenciesYearsDropDownItems = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[2]/am-multiselect/div/ul').get_property("children")


	searchTest(searchString)
	searchCorrectnessTest(searchString)



	# #Reveal Drop down for budget 
	# budgetYearsDropDownButton.click()

	# #Print and click all buttons in drop down
	# for element in budgetYearsDropDownItems:
	# 	print(element.get_property("outerText"))
	# 	element.click()

	# #Reveal Drop down for agencies
	# agenciesYearsDropDownButton.click()

	# #Print and click all buttons in drop down
	# for element in agenciesYearsDropDownItems:
	# 	print(element.get_property("outerText"))
	# 	element.click()	