from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from datetime import datetime

URL = 'https://www.turismocity.com.ar'

s = Service('C:/Users/Guille/Documents/chromedriver/chromedriver.exe')
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
driver = webdriver.Chrome(service=s, options=options)
driver.get(URL)
sleep(1)

# Cities (IATA codes)
city_from = 'BUE'
city_destination ='LON'

#inbound
div_dest = driver.find_element(By.XPATH, '//div[contains(@class,"e2e-inbound-input")]')
div_dest.click()
input_destination = driver.find_element(By.XPATH, '//input[contains(@class,"select2-focused")]')
input_destination.send_keys(city_destination)
sleep(1)
click_destination = driver.find_element(By.XPATH, '//*[@id="flights-tab-container"]/form/div[2]/div/div[3]/div/div/span/span/span[2]/ul/li/div[2]/div[2]')
click_destination.click()
sleep(1)

#Outbound
div_from = driver.find_element(By.XPATH, '//div[contains(@class,"e2e-outbound-input")]')
div_from.click()
input_from = driver.find_element(By.XPATH, '//input[contains(@class,"select2-focused")]')
input_from.send_keys(city_from)
sleep(1)
driver.find_element(By.XPATH, '//*[@id="flights-tab-container"]/form/div[2]/div/div[2]/div/div/span/span/span[2]/ul/li[1]/div[2]/div[2]').click()

# Selecting the 'haven't decided a date yet' checkbox
checkbox = driver.find_element(By.XPATH, '//div[contains(@class,"tc-checkbox")]')
checkbox.click()

# Search button
search_btn = driver.find_element(By.XPATH, '//input[contains(@class, "btn btn-block btn-large btn-lg tc-btn-main tc-btn-flight-main TCSearchButton")]')
search_btn.click()
sleep(5)

# Creating empty lists and using BeautifulSoup to extract data
from_dates=[]
return_dates=[]
prices=[]
links=[]

soup=BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'class': 'tc-price-table'})
for row in table.tbody.find_all('tr', limit=10):
        columns = row.find_all('td')
        origin = columns[0].div.text
        ret = columns[1].div.text
        price = columns[6].div.text
        link = columns[7].div.a['href']

        from_dates.append(origin)
        return_dates.append(ret)
        prices.append(price)
        links.append(URL + link)

driver.close()

# Creating a new data frame and saving to a csv file (todays date in the name for future automation) 
now = datetime.now().strftime('%d_%m_%Y')
my_dict = {'from': from_dates, 'to': return_dates, 'price': prices, 'link': links}
df = pd.DataFrame(my_dict)
df.to_csv(f'flights_{now}.csv')