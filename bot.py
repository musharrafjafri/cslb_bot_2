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
    except:
        driver.close()
        print(city[num], ' with ', lic_type[num], 'is wrong.')
        wrong_city.append(city[num])
        # wrong_lic_type.append(lic_type[num])

    with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
        for i in range(len(wrong_city)):
            w_in.write(f'{wrong_city[i]}, ')

    # try:
    prev_id = pd.read_html(driver.page_source)[0]['License #'][0]
    after_id = pd.read_html(driver.page_source)[0]['License #'][0]
    page_num_class = driver.find_element_by_class_name('GridPager').find_element_by_tag_name('td')
    td_texts_list = []
    for np_link in page_num_class.find_elements_by_tag_name('td'):
        td_texts_list.append(np_link.text)
    if td_texts_list.pop() == '>>':
        for a_tag in page_num_class.find_elements_by_tag_name('a'):
            if a_tag.text == '>>':
                a_tag.click()
                while prev_id == after_id:
                    sleep(1)
                    after_id = pd.read_html(driver.page_source)[0]['License #'][0]
                sleep(1)
                for np_link in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('td'):
                    td_texts_list.clear()
                    td_texts_list.append(np_link.text)
                break
    else:
        pass
    print(td_texts_list.pop())
        # for np_link_span in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('span'):
        #     if int(np_link.text) in range(1, 50) and int(np_link.text) > int(np_link_span.text):
        #         print('np_link:', np_link.text)
        #         np_link.click()
        #         while prev_id == after_id:
        #             sleep(1)
        #             after_id = pd.read_html(driver.page_source)[0]['License #'][0]
        #         print('prev_id: ', prev_id)
        #         print('after_id: ', after_id)
        #         print('page changes.')
        #         # print('np_link:', np_link.text)
        #         break
    # except:

    #     print('except block.')


    # driver.close()
print('                       BOT END...')