from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time
import xlrd

book = xlrd.open_workbook("/Users/tl0002axtech/Downloads/keo-contact-list-2012.xls")
# print("The number of worksheets is {0}".format(book.nsheets))
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
def scrape_data(data_list):
    # On click, iframe appears containing agent details. Selenium needs to switch out to the iframe to detect its elements. 
    iframe = driver.find_element_by_xpath("//iframe[@name='Sample']")
    driver.switch_to.frame(iframe)

    # Scrape data through table rows and table elements
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "FtPublicRegisterDetail_RGridSP_ctl00__0"))
        )
    except:
        close = driver.find_element_by_id('BtnClose')
        close.click()
        driver.switch_to.default_content()
        return
    
    try:
        data_row = driver.find_element_by_id('FtPublicRegisterDetail_RGridSP_ctl00__0').find_elements_by_xpath('.//td')
    except:
        close = driver.find_element_by_id('BtnClose')
        close.click()
        driver.switch_to.default_content()
        return
    # print(data_row[1].text)

    sh = book.sheet_by_index(0)
    for rx in range(sh.nrows):
        if sh.row(rx)[0].value in data_row[1].text:
            print(sh.row(rx)[0])
            data_list.append(sh.row(rx)[0].value)
            break
    # close iframe and switch back to original window
    # close = driver.find_element_by_xpath("//input[@name='BtnClose']")
    close = driver.find_element_by_id('BtnClose')
    close.click()
    driver.switch_to.default_content()


driver = webdriver.Chrome('/Users/tl0002axtech/Downloads/chromedriver')

driver.get('https://www.cea.gov.sg/public-register?category=EstateAgent&page=90')

all_data = []

for page_num in range(91, 120):
    all_estate_agents = driver.find_elements_by_xpath('.//tr')
    
    for estate_index in range(3, len(all_estate_agents)-1):
        estate = all_estate_agents[estate_index].find_elements_by_xpath('.//td')[0].find_element_by_xpath('.//a')
        
        # select estate and search
        estate.click()

        scrape_data(all_data)

    # navigate to next page
    # driver.find_element_by_link_text(str(page_num)).click()
    driver.get('https://www.cea.gov.sg/public-register?category=EstateAgent&page={0}'.format(page_num))

json_data = {"data" : all_data}

with open('contact_4.json', 'w') as outfile:
    json.dump(json_data, outfile)