# Webscraper for OutsidePride.com ground-seeds section
# Install BeautifulSoup and Selenium

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import regex as re
import time
import requests
import csv

# Configure webdriver for your browser and
# set path to the driver file on your computer.
# Get soup of page html.

driver = webdriver.Chrome('/Users/eliaslosego/Desktop/chromedriver')
driver.get('https://www.outsidepride.com/seed/ground-cover-seed/')
html = driver.page_source

pages = [str(i) for i in range(5)]

# Wait 20 seconds on new page and close pop-up dialog.

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.styles_closeButton__20ID4'))).click()

# Set base_URL for reformatting a_tags from page_soup
# Define unwanted_URLS to be removed from final URL_list

base_URL ='https://www.outsidepride.com'

URL_list = []

# Iterate through product pages
# and find a_tags in page soup that contain html links to the different
# ground cover seeds. Reformat using the base_URL, and append
# URL_list.
    
for page in pages:
    time.sleep(3)
    html = driver.page_source
    page_soup = soup(html, 'lxml')
    
    for a_tag in page_soup.find_all('a', href = True):
        new_URL = base_URL + a_tag['href']
        
        if '/seed/ground-cover-seed/'in new_URL:
            if '.html' in new_URL:
                
                if new_URL not in URL_list:
                    URL_list.append(new_URL)
                 
    driver.find_element_by_css_selector('a.next').click()
    
# Create .csv file in write and list headers on the spreadsheet.
    
filename = 'groundcover_seeds.csv'
f = open(filename, 'w') 

headers = "Name, Season, USDA Zone, Height, Bloom Season, Bloom Color, Environment, Soil Type, Foot Traffic, Deer Resistant, Temperature, Average Germination Time, Light Required, Depth, Sowing Rate, Moisture, Spacing\n"

f.write(headers)

# Iterate through all product pages added to URL_list and create variables
# for product names and information to be formatted and written to .csv file.
    
for URL in URL_list:
    driver.get(URL)
    html = driver.page_source
    big_soup = soup(html, 'lxml')

    for h2_tag in big_soup.find_all('h2', class_ = 'opc-h1'):
        name = h2_tag.text
    
    p_tags = big_soup.find_all('p', class_ = 'opc-small')
    
    for p_tag in p_tags:   
        
        if p_tag.find(string = ('Season')):
            season = p_tag.text.replace('Season: ', '')

        elif p_tag.find_all(string = re.compile('USDA Zones')):
            zone = p_tag.text.replace('USDA Zones: ', '')

        elif p_tag.find(string = re.compile('Height')):
            height = p_tag.text.replace('Height: ', '')

        elif p_tag.find(string = re.compile('Bloom Season')):
            bloom = p_tag.text.replace('Bloom Season: ', '')
            
        elif p_tag.find(string = re.compile('Bloom Color')):
            color = p_tag.text.replace('Bloom Color: ', '')
    
        elif p_tag.find(string = re.compile('Environment')):
            environment = p_tag.text.replace('Environment: ', '')
            
        elif p_tag.find(string = re.compile('Soil Type')):
            soil = p_tag.text.replace('Soil Type: ', '')
            
        elif p_tag.find(string = re.compile('Foot Traffic')):
            traffic = p_tag.text.replace('Foot Traffic: ', '')
            
        elif p_tag.find(string = re.compile('Deer Resistant')):
            resistance = p_tag.text.replace('Deer Resistant: ', '')
            
        elif p_tag.find(string = re.compile('Temperature')):
            temperature = p_tag.text.replace('Temperature: ', '')
        
        elif p_tag.find(string = re.compile('Average Germ Time')):
            germination = p_tag.text.replace('Average Germ Time: ', '')
            
        elif p_tag.find(string = re.compile('Light Required')):
            light = p_tag.text.replace('Light Required: ', '')
            
        elif p_tag.find(string = re.compile('Depth')):
            depth = p_tag.text.replace('Depth: ', '')
            
        elif p_tag.find(string = re.compile('Sowing Rate')):
            sowing = p_tag.text.replace('Sowing Rate: ', '')
            
        elif p_tag.find(string = re.compile('Moisture')):
            moisture = p_tag.text.replace('Moisture: ', '')
            
        elif p_tag.find(string = re.compile('Spacing')):
            spacing = p_tag.text.replace('Spacing: ', '')
                
        else:
            continue

# Write variables to .csv file and close.
    
    f.write(name.replace(',', ' |') + ',' + season.replace(',', ' |') + ',' + zone.replace(',', ' |') + ',' + height.replace(',', ' |') + ',' + bloom.replace(',', ' |') + ',' + color.replace(',', ' |') + ',' + environment.replace(',', ' |') + ',' + soil.replace(',', ' |') + ',' + traffic.replace(',', ' |') + ',' + resistance.replace(',', ' |') + ',' + temperature.replace(',', ' |') + ',' + germination.replace(',', ' |') + ',' + light.replace(',', ' |') + ',' + depth.replace(',', ' |') + ',' + sowing.replace(',', ' |') + ',' + moisture.replace(',', ' |') + ',' + spacing.replace(',', ' |') + '\n')
    
f.close()

# End of code.
    