from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
import getpass
import tkinter as tk
import re
import time



#scrolling down and waiting 1 second


def page_scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(0.5)


    
driver = webdriver.Chrome("*****")
driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

username = driver.find_element_by_id("****")
username.send_keys("****")
password = driver.find_element_by_id("*****")
password.send_keys("****")
log_in_button = driver.find_element_by_xpath("//*[@id='app__container']/main/div/form/div[3]/button")
log_in_button.click()


search_link="*****"
no_of_pages=1

contact_link=search_link

driver.get(search_link)



#Selenium hands the page source to Beautiful Soup

driver.get(contact_link)
soup =BeautifulSoup(driver.page_source, 'lxml')
result_main = soup.findAll('div',class_="display-flex mt2")

page_scroll()
            
try:
    name_data = soup.find('li',attrs={'class':'inline t-24 t-black t-normal break-words'}).contents
except:
    name_data=[]
    name_data.append(NoInfo("N/A").text)

try:
    location_data= soup.find('li',attrs={'class':'t-16 t-black t-normal inline-block'}).contents
except:
    location_data=[]
    location_data.append(NoInfo("N/A"))

try:
    company_data = soup.find('span', {'class': 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view'})
except:
    company_data=[]
    company_data.append(NoInfo("N/A"))

try:
    current_position = soup.find('div', {'class': 'display-flex flex-column full-width'})
except:
    current_position=[]
    current_position.append(NoInfo("N/A"))

    
contact_current_company = (company_data.text).replace('\n', '')
contact_location=location_data[0].replace('\n', '')
contact_name= name_data[0].replace('\n', '')

contact_info=[contact_name, contact_location, contact_current_company, current_position]
print(contact_info)

print("DONE!")

