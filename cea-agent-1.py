from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time
import xlrd

# print("The number of worksheets is {0}".format(book.nsheets))
# book = xlrd.open_workbook("/Users/tl0002axtech/Downloads/Dennis_Wee_Realty.xls")
# sh = book.sheet_by_index(0)
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=2)))

# initialize chrome driver
driver = webdriver.Chrome('/Users/tl0002axtech/Downloads/chromedriver92')
book = xlrd.open_workbook("/Users/tl0002axtech/Downloads/savills_upload.xls")
sh = book.sheet_by_index(0)
all_data = []

# Loop through xls file and to get agent details
for e in range(sh.nrows):
# for e in range(10):
    try:
        number = int(sh.cell_value(rowx=e+1, colx=2))
    except:
        print('no number')
        continue
    
    # get agent details url using phone number as param
    driver.get('https://www.cea.gov.sg/aceas/public-register/sales/1?page=1&pageSize=10&sortAscFlag=true&sort=name&contactNumber={0}'.format(number))

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "has-mobile-cards"))
        )
    except:
        print('no data')
        continue    
            
    table = driver.find_element_by_class_name("has-mobile-cards")
    table_array = table.find_elements_by_xpath("//table/tbody/tr/td")
    agent_details = {}
    for data in table_array:
        if(data.get_attribute("data-label") and data.get_attribute("data-label") != "Action"):
            text = data.find_element_by_class_name("cell-text").text
            print(text)
            agent_details[data.get_attribute("data-label")] = text
    agent_details["Mobile"] = number
    all_data.append(agent_details)

json_data = {"data" : all_data}

with open('savills_upload.json', 'w') as outfile:
    json.dump(json_data, outfile)      
            



