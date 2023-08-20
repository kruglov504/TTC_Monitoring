from bs4 import BeautifulSoup
from os import environ, pathsep
from selenium import webdriver
import time

# SET THIS
url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_cloth_base_harvestersilk.png&ItemID=3799&ItemNamePattern=Ancestor+Silk&SortBy=LastSeen&Order=desc'

MAX_PRICE = 20.0
MIN_NUMBER = 100
REQUEST_EACH = 90   # sec

#############################################################################################################


environ["PATH"] += pathsep + 'C:/Program Files/Google/Chrome/Application'
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
#browser = webdriver.Chrome()

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
        print('item name: ' + self.itemName +
              ' | location: ' + self.location +
              ' | price: ' + self.price +
              ' | amount: ' + self.amount +
              ' | lastSeen: ' + self.lastSeen)


def searchItem():
    browser.get(url)

    time.sleep(3)

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

    # quit browser
    #browser.quit()

    # loop over items and print if price ok
    for item in newItems:
        if item.itemOk():
            item.printMsg()


if __name__ == "__main__":
    while True:
        searchItem()
        time.sleep(REQUEST_EACH)

