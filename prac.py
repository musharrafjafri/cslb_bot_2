import pandas as pd
import openpyxl
import xlrd

# list1 = [['a', 'b', 'c', 'd'], ['12', '23', '34', '45'], ['z', 'x', 'c', 'v']]
list1 = [['2324','654','345','231>>>'],['4367','23423','342','3766>>>'],['467','835','1354','456>>>']]
list2 = []
for i in range(len(list1)):
    for list in list1[i]:
        try:
            print(len(int(list)))
            list2.append(int(list))
        except:
            print('except block')
print(list2)
