from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time

def scrape_data(data_list):
    # Scrape data through table rows and table elements
    data_rows = driver.find_elements_by_xpath('//tr')

    for row_index in range(2, len(data_rows)):
        data_dict = {}
        data_row = data_rows[row_index].find_elements_by_xpath('.//td')

        for data_index in range(len(data_row)):
            data_dict["{0}".format(data_index)] = data_row[data_index].text

        data_list.append(data_dict)


driver = webdriver.Chrome('/Users/tl0002axtech/Downloads/chromedriver')

driver.get('https://www.ura.gov.sg/realEstateIIWeb/transaction/search.action')

all_estates = driver.find_elements_by_class_name("addToProject")
all_data = []

for estate_index in range(len(all_estates)//4 * 3 +2, len(all_estates)):
    # select estate and search
    time.sleep(2)
    estate = driver.find_element_by_id("addToProject_{0}".format(estate_index))
    print(estate.text)
    estate.click()

    searchButton = driver.find_element_by_id("searchForm_0")
    searchButton.click()

    # sometimes when searching for estate, site will return "missing parameters" instead of the sales transaction table. Might have to repeat the process until the table appears / try refreshing the page.
    time.sleep(2)
    driver.refresh()

    # Scrape data from table
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))
    scrape_data(all_data)
    driver.back()

json_data = {"data" : all_data}

with open('private_property_3.json', 'w') as outfile:
    json.dump(json_data, outfile)