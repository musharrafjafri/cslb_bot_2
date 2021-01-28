from time import sleep  # sleep/wait is use to apply wait to load all the attributes in browser.
from selenium import webdriver  # It is out main library to make automation through python language.
from selenium.webdriver.support.select import Select

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument('start-maximized')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # to open chrome in maximaze mode.
driver.get("https://cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx")  # Giving url to open in chrome browser.

for item in driver.find_element_by_name('ctl00$MainContent$ddlLicenseType').find_elements_by_tag_name('option'):
    print(item.text)


# selection = Select(driver.find_element_by_name('ctl00$MainContent$ddlLicenseType'))  # Getting all options of license type from list.
#   # Selecting our desired license type from option's list
# driver.find_element_by_name('ctl00$MainContent$btnZipCodeSearch').click()  # Click on selected license type.
# sleep(1)  # wait 1 second to load page.
# driver.find_element_by_name('ctl00$MainContent$ibExportToExcell').click()  # Click on button to go to result.
# sleep(5)  # wait 5 second to wait page until file download.
