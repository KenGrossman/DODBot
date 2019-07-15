#Created by Kenny Grossman July, 2019
#This project is intended to be used for interview purposes only

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Add location of downloaded selenium chrome driver
#Drivers can be found at https://www.seleniumhq.org/download/
class pageModel:
	def setUp(self):
		print("here")
		driverFolderPath = '/Users/kennygrossman/Projects/Bots/Drivers/chromedriver'
		URL = 'https://apps.dtic.mil/dodinvestment/#/advancedSearch'
		webpageTimeout = 10
		self.searchString = '0603680F'
		
		self.driver = webdriver.Chrome(driverFolderPath)
		self.driver.get(URL)

		#Wait for page and content to load before proceeding
		try:
		    element = WebDriverWait(driver, webpageTimeout).until(
		        EC.presence_of_element_located((By.XPATH, '//*[@id="budgetNumObj_value"]'))
		    )
		except:
			print("Failed to load webpage")
			self.driver.Dispose()
		else:
			#Identify page objects for later use
			self.searchButton = driver.find_element(By.XPATH, '//*[@id="performSearch"]')
			self.clearButton = driver.find_element(By.XPATH, '//*[@id="clearSearch"]')
			self.programSearch = driver.find_element(By.XPATH, '//*[@id="budgetNumObj_value"]')
			self.budgetYearsDropDownItems = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/form/div[3]/div[1]/am-multiselect/div/ul/li')
			self.agenciesDropDownItems = driver.find_elements(By.XPATH, '')

			for element in budgetYearsDropDownItems:
				print(element.outerText)

	def searchTest(self, searchString):
		programElementNumberSearch = driver.find_elements(By.XPATH, '//button')

	def __init__(self):
		setUp()