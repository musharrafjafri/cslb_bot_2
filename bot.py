import xlrd
from xlwt import Workbook
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select

print('                       BOT STARTED...')
city_low = []
lic_type = []
city = []
d_path = ''
with open('res_files_path.txt') as file:
    d_path = file.read()

workbook = xlrd.open_workbook('input_data/input_data.xlsx')
sheet = workbook.sheet_by_index(0)

for row in range(sheet.nrows):
    city_low.append(sheet.cell_value(row, 0))
    lic_type.append(sheet.cell_value(row, 1))

for citi in city_low:
    city.append(citi.upper())

print(city)

wrong_city = []
for num in range(len(city)):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('start-maximized')
    preferances = {"download.default_directory": d_path}
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

        des_city = city[num]
        cur_lic_type = lic_type[num]
        location = 'res_files/Contractor List.xlsx'
        workbook = xlrd.open_workbook(location)
        sheet = workbook.sheet_by_index(0)
        file_city = sheet.cell_value(8, 2)
        p_num = 0

        try:
            while des_city != file_city:
                location = f"res_files/Contractor List ({p_num + 1}).xlsx"
                workbook = xlrd.open_workbook(location)
                sheet = workbook.sheet_by_index(0)
                file_city = sheet.cell_value(8, 2)
                p_num += 1
        except:
            # print('City name is wrong.')
            pass

        lic = []
        for row in range(sheet.nrows):
            if row > 7:
                lic.append(sheet.cell_value(row, 5))

        print('length of license list: ', len(lic))
        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'LICENSE NUMBER')
        sheet1.write(0, 1, 'NAME')

        for i in range(len(lic)):
            print(f'{i+1} out of {len(lic)} - {des_city}')
            try:
                url = f'https://cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={int(lic[i])}'
                driver.get(url)
                # sleep(1)
                driver.find_element_by_name('ctl00$MainContent$PersonnelLink').click()
                # sleep(1)
                sheet1.write(i+1, 0, lic[i])
                sheet1.write(i+1, 1, driver.find_element_by_id('MainContent_dlAssociated_hlName_0').text)
            except:
                print('Except block...')
                sheet1.write(i+1, 0, lic[i])
                sheet1.write(i+1, 1, 'NOT FOUND')

        wb.save(f'output_data/{des_city}-{cur_lic_type}-Names.xls')
    except:
        driver.close()
        print(city[num], ' with ', lic_type[num], 'is wrong.')
        wrong_city.append(city[num])
        # wrong_lic_type.append(lic_type[num])

    with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
            for i in range(len(wrong_city)):
                w_in.write(f'{wrong_city[i]}, ')

    driver.close()
print('                       Files generated successfully...')