#Created by Kenny Grossman July, 2019
#This project is intended to be used for interview purposes only

from selenium import webdriver

if __name__ == "__main__":
	#Add location of downloaded selenium browser drivers
	#Drivers can be found at https://www.seleniumhq.org/download/
	driverFolderPath = ''
	URL = 'https://apps.dtic.mil/dodinvestment/#/advancedSearch'
	searchString = '0603680F'

	#Setup drivers
	drivers = {
		"chrome"	: webdriver.Chrome(driverFolderPath),
		"firefox"	: webdriver.Firefox(driverFolderPath),
		"ie"		: webdriver.Ie(driverFolderPath),
	}

	#Test with all available browser drivers
	for driver in drivers:
		#Add try catch to ensure drivers are found before proceeding
		try:
			driver.get(URL)

		except:
			#Fail all remaining test and move on