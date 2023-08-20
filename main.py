#from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from os import environ, pathsep

#C:\Program Files\Google\Chrome\Application\chrome.exe

environ["PATH"] += pathsep + 'C:/Program Files/Google/Chrome/Application'
browser = webdriver.Chrome()

url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_outfitter_potion_014.png&ItemID=211&ItemNamePattern=Dreugh+Wax&SortBy=LastSeen&Order=desc'

browser.get(url)
soup = BeautifulSoup(browser.page_source, "html.parser")

table = soup.find('table', class_ = 'trade-list-table max-width')


for elem in table.find_all('tbody'):
    rows = elem.find_all('tr')
    for row in rows:
        rowData = row.find('td', class_ = 'bold hidden-xs')
        print(row.text)



