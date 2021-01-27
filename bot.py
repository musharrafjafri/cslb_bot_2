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
print('                       BOT STARTED...')
city = []
lic_type = []

workbook = xlrd.open_workbook('input_data/input_data.xlsx')
sheet = workbook.sheet_by_index(0)

for row in range(sheet.nrows):
    city.append(sheet.cell_value(row, 0))
    lic_type.append(sheet.cell_value(row, 1))


wrong_city = []
for num in range(len(city)):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('start-maximized')
    preferances = {"download.default_directory": r"C:\Users\smmj1\OneDrive\Python Projects\cslb_bot-2\input_data"}
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
        driver.find_element_by_name('ctl00$MainContent$ibExportToExcell').click()
        sleep(5)
        driver.close()
    except:
        driver.close()
        print(city[num], ' with ', lic_type[num], 'is wrong.')
        wrong_city.append(city[num])
        # wrong_lic_type.append(lic_type[num])

    with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
        for i in range(len(wrong_city)):
            w_in.write(f'{wrong_city[i]}, ')

    des_city = city[num]
    location = 'input_data/Contractor List.xlsx'
    workbook = xlrd.open_workbook(location)
    sheet = workbook.sheet_by_index(0)
    file_city = sheet.cell_value(8, 2)
    p_num = 0
    lic = []
    try:
        while des_city != file_city:
            location = f"input_data/Contractor List ({p_num + 1}).xlsx"
            workbook = xlrd.open_workbook(location)
            sheet = workbook.sheet_by_index(0)
            file_city = sheet.cell_value(8, 2)
            p_num += 1
            print('While no.', p_num)
    except:
        print('City name is wrong.')

    for row in range(sheet.nrows):
        if row > 7:
            lic.append(sheet.cell_value(row, 5))

    print('length of license list: ', len(lic))
    for i in range(len(lic)):
        print(int(lic[i]))
        driver.get(f'https://cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={int(lic[i])}')
        sleep(1)
        driver.find_element_by_name('ctl00$MainContent$PersonnelLink').click()
        sleep(1)
        print(driver.find_element_by_id('MainContent_dlAssociated_hlName_0').text)
print('                       BOT END...')