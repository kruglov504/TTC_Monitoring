
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import datetime
from ItemInfo import ItemInfo
import re   # to search strings
import os   # for console output colors
os.system('color')  # to make colored console output

class ItemMonitoringProcess:
    def __init__(self, url, urlTimeout, maxPrice, minNumber, requestInterval):
        self.url = url
        self.urlTimeout = urlTimeout
        self.maxPrice = maxPrice
        self.minNumber = minNumber
        self.requestInterval = requestInterval

    def searchItem(self):
        while True:
            # print search item and timestamp
            searchItemName = re.search('ItemNamePattern=(.*)&SortBy', self.url)
            if searchItemName is not None:
                print(searchItemName.group(1) + ': ', datetime.datetime.now())

            try:
                # Set up browser
                options = webdriver.FirefoxOptions()
                options.add_argument('--headless')
                options.add_argument("--start-maximized")
                self.driver = webdriver.Firefox(options=options)
                self.driver.get(self.url)
                try:
                    element_present = EC.presence_of_element_located((By.ID, 'search-result-view'))
                    WebDriverWait(self.driver, self.urlTimeout).until(element_present)
                except TimeoutException:
                    print("\033[0;31m", "Timed out waiting for page to load", "\033[0m")

                time.sleep(3)

                soup = BeautifulSoup(self.driver.page_source, "html.parser")

                self.driver.quit()

                table = soup.find('table', class_='trade-list-table max-width')

                # last prices
                newItems = []

                for elem in table.find_all('tbody'):
                    rows = elem.find_all('tr', class_='cursor-pointer')
                    for row in rows:
                        try:
                            newItems.append(ItemInfo(itemName=row.find('td').find('div').text,
                                                     location=row.find('a', class_='trade-list-clickable bold').text,
                                                     guild=row.find('div', attrs={'data-bind': 'text: GuildName'}).text,
                                                     price=row.find('td', class_='gold-amount bold').find(
                                                         attrs={'data-bind': 'localizedNumber: UnitPrice'}).text,
                                                     amount=row.find('td', class_='gold-amount bold').find(
                                                         attrs={'data-bind': 'localizedNumber: Amount'}).text,
                                                     lastSeen=row.find('td', class_='bold hidden-xs').text,
                                                     maxPrice=self.maxPrice,
                                                     minNumber=self.minNumber))
                        except AttributeError:
                            print('searchItem() -> No data')

                # loop over items and print if price ok
                for item in newItems:
                    if item.itemOk():
                        item.printMsg()

                time.sleep(self.requestInterval)

            except WebDriverException:
                print('Exception in searchItem()')




