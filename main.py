from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import datetime
import os

os.system('color')  # to make colored console output

# SET THIS
url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_cloth_base_harvestersilk.png&ItemID=3799&ItemNamePattern=Ancestor+Silk&SortBy=LastSeen&Order=desc'
URL_TIMEOUT = 3

MAX_PRICE = 70.0
MIN_NUMBER = 100
REQUEST_EACH = 90   # sec

#############################################################################################################

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument("--start-maximized")
browser = webdriver.Firefox(options=options)

# Class to saveData
class ItemInfo:
    def __init__(self, itemName, location, price, amount, lastSeen):
        self.itemName = itemName
        self.location = location
        self.price = price
        self.amount = amount
        self.lastSeen = lastSeen
        self.priceOk = float(self.price.replace(',', '')) <= MAX_PRICE
        self.amountOk = float(self.amount.replace(',', '')) >= MIN_NUMBER

    def itemOk(self):
        return self.priceOk and self.amountOk

    def printMsg(self):
        print("\033[92m", "item name: ", self.itemName +
              " | location: " + self.location +
              " | price: " + self.price +
              " | amount: " + self.amount +
              " | lastSeen: " + self.lastSeen, "\033[0m")


def searchItem():
    browser.get(url)
    try:
        element_present = EC.presence_of_element_located((By.ID, 'search-result-view'))
        WebDriverWait(browser, URL_TIMEOUT).until(element_present)
    except TimeoutException:
        print("\033[0;31m", "Timed out waiting for page to load", "\033[0m")

    soup = BeautifulSoup(browser.page_source, "html.parser")

    table = soup.find('table', class_ = 'trade-list-table max-width')

    # last prices
    newItems = []

    for elem in table.find_all('tbody'):
        rows = elem.find_all('tr', class_ = 'cursor-pointer')
        for row in rows:
            newItems.append(ItemInfo(itemName = 'itemName',
                                     location = 'location',
                                     price = row.find('td', class_='gold-amount bold').find(attrs={'data-bind' : 'localizedNumber: UnitPrice'}).text,
                                     amount = row.find('td', class_='gold-amount bold').find(attrs={'data-bind' : 'localizedNumber: Amount'}).text,
                                     lastSeen = row.find('td', class_='bold hidden-xs').text))


    # loop over items and print if price ok
    print(datetime.datetime.now())
    for item in newItems:
        if item.itemOk():
            item.printMsg()


if __name__ == "__main__":
    while True:
        try:
            searchItem()
        except WebDriverException:
            print('Exception in searchItem()')
        time.sleep(REQUEST_EACH)

