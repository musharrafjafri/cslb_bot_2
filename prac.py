import pandas as pd
import openpyxl
import xlrd

city = 'ESCONDIDO'
location = 'input_data/Contractor List.xlsx'
workbook = xlrd.open_workbook(location)
sheet = workbook.sheet_by_index(0)
file_city = sheet.cell_value(8, 2)

num = 0
lic = ['2323', '23245']

print(f'https://cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={int(lic[1])}')

# while city != file_city:
#     location = f"input_data/Contractor List ({num + 1}).xlsx"
#     workbook = xlrd.open_workbook(location)
#     sheet = workbook.sheet_by_index(0)
#     file_city = sheet.cell_value(8, 2)
#     num += 1
# lic = []
# for row in range(sheet.nrows):
#     if row > 7:
#         lic.append(sheet.cell_value(row, 5))
# for item in range(1, (len(lic)+1)):
#     print(item)
