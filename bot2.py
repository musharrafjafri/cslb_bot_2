import os
from csv import reader
import time
import requests
import pandas as pd
import xlrd
from time import sleep
from selenium import webdriver
from _collections import defaultdict
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

city = []
lic_type = []

workbook = xlrd.open_workbook('input_data/input_data.xlsx')
sheet = workbook.sheet_by_index(0)

for row in range(sheet.nrows):
    city.append(sheet.cell_value(row, 0))
    lic_type.append(sheet.cell_value(row, 1))


wrong_city = []
# wrong_lic_type = []

for num in range(len(city)):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('start-maximized')
    preferances = {"download.default_directory": r"C:\Users\smmj1\OneDrive\Python Projects\cslb_bot-1\output_data"}
    options.add_experimental_option("prefs", preferances)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx")
    sleep(1)


    try:
        driver.find_element_by_name('ctl00$MainContent$txtCity').send_keys(city[num])
        selection = Select(driver.find_element_by_name('ctl00$MainContent$ddlLicenseType'))
        selection.select_by_visible_text(lic_type[num])
        driver.find_element_by_name('ctl00$MainContent$btnZipCodeSearch').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="MainContent_gvZipCodeSearch"]/tbody/tr[27]/td/table/tbody/tr/td[12]/a').click()
        sleep(3)
        page_num_class = driver.find_element_by_class_name('GridPager')
        page_nums = []
        last_page_num = ''
        for num in page_num_class.find_elements_by_tag_name('span'):
            page_nums.append(num.text)
        last_page_num = page_nums.pop()
        print(last_page_num)
        for i in range(1, (int(last_page_num)+1)):
            print(i)
        
        # source = pd.read_html(driver.page_source)
        # table = source[0]
        # lic_col = table['License #'].drop([25, 26])
        # print(lic_col)

    except:
        driver.close()
        print(city[num], ' with ', lic_type[num], 'is wrong.')
        wrong_city.append(city[num])
        # wrong_lic_type.append(lic_type[num])
    break
with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
    for i in range(len(wrong_city)):
        w_in.write(f'{wrong_city[i]}, ')