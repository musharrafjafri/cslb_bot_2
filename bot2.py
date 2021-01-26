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
        sleep(2)
        page_num_class = driver.find_element_by_class_name('GridPager')
        last_page_num = ''
        page_nums = []

        try:
            for np_link in page_num_class.find_elements_by_tag_name('a'):
                print('np_link text: ',np_link.text)
                for np_link_span in page_num_class.find_elements_by_tag_name('span'):
                    print('CP1')
                    if int(np_link.text) in range(1, 50) and int(np_link.text) > int(np_link_span.text):
                        print('CP2')
                        np_link.click()
                        print('CP3')
                        break
                        print('CP4')
                        # sleep(10)
                    # elif np_link.text == '...':
                print('CP_loop')    
                sleep(1)
                    # print('np_link spans: ', np_link_span.text)

                # if np_link.text == '>>':
                    # np_link.click()
                    # sleep(20)
                    # for num in page_num_class.find_elements_by_tag_name('span'):
                    #     last_page_num = num.text
                    # sleep(2)
                    # page_num_class.find_element_by_tag_name('td').find_element_by_tag_name('a').click()
                    # sleep(10)

            # print('last page number: ', last_page_num)
        except:
            print('except block')
            # for num in page_num_class.find_elements_by_tag_name('a'):
            #     page_nums.append(num.text)
            # last_page_num = page_nums.pop()
            # print('last page number: ', last_page_num)

        # for i in range(1, (int(last_page_num)+1)):
        #     print(i)
        # driver.close()
        # source = pd.read_html(driver.page_source)
        # table = source[0]
        # lic_col = table['License #'].drop([25, 26])
        # print(lic_col)
    except:
        driver.close()
        print(city[num], ' with ', lic_type[num], 'is wrong.')
        wrong_city.append(city[num])
        # wrong_lic_type.append(lic_type[num])

with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
    for i in range(len(wrong_city)):
        w_in.write(f'{wrong_city[i]}, ')