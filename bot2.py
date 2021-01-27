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

    prev_id = pd.read_html(driver.page_source)[0]['License #'][0]
    after_id = pd.read_html(driver.page_source)[0]['License #'][0]
    page_num_class = driver.find_element_by_class_name('GridPager').find_element_by_tag_name('td')
    td_texts_list = []
    for np_link in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('td'):
        td_texts_list.append(np_link.text)
    if td_texts_list.pop() == '>>':
        for a_tag in page_num_class.find_elements_by_tag_name('a'):
            if a_tag.text == '>>':
                a_tag.click()
                while prev_id == after_id:
                    sleep(1)
                    after_id = pd.read_html(driver.page_source)[0]['License #'][0]
                sleep(1)
                td_texts_list.clear()
                for np_link in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('td'):
                    td_texts_list.append(np_link.text)
                break
    else:
        for np_link in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('td'):
            td_texts_list.append(np_link.text)

    driver.find_element_by_class_name('GridPager').find_element_by_tag_name('tr').find_element_by_tag_name('td').click()
    while prev_id != after_id:
        sleep(1)
        after_id = pd.read_html(driver.page_source)[0]['License #'][0]

    max_page = td_texts_list.pop()
    lic_nums_list = []
    all_lic_nums = []
    for page_num in range(1, (int(max_page)+1)):
        print('loop no.', page_num)
        lic_nums_list.append(list(pd.read_html(driver.page_source)[0]['License #']))
        try:
            for a in driver.find_element_by_class_name('GridPager').find_elements_by_tag_name('a'):
                try:
                    if int(a.text) > page_num:
                        print('CP1')
                        a.click()
                        while prev_id == after_id:
                            sleep(1)
                            after_id = pd.read_html(driver.page_source)[0]['License #'][0]
                        break
                except:
                    if a.text == '...':
                        print('CP2')
                        next_page_link = a.get_attribute('href')
                        page_text = next_page_link[61:69]
                        print('CP3')
                        if str(page_num) in page_text:
                            a.click()
                            print('CP4')
                            while prev_id == after_id:
                                print('while cp')
                                sleep(1)
                                after_id = pd.read_html(driver.page_source)[0]['License #'][0]
                            break
            prev_id = after_id
        except:
            print('except block.')

    # for i in range(len(lic_nums_list)):
    #     print(lic_nums_list[i])
    #     for num in lic_nums_list[i]:
    #         try:
    #             if len(num) > 1:
    #                 all_lic_nums.append(int(num))
    #         except:
    #             pass
    # print(all_lic_nums)
    # print('Length: ', len(all_lic_nums))
print('                       BOT END...')