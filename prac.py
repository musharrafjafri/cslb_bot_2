import pandas as pd
import openpyxl
import xlrd


city = ['Hey', 'You']
lic_type = ['Whats', 'Up']

with open('wrong_input/wrong_inputs.txt', 'w') as w_in:
    for i in range(len(city)):
        w_in.write(f'{city[i]}, ')
