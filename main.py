from ItemMonitoringProcess import ItemMonitoringProcess
import multiprocessing
import datetime

REQUEST_INTERVAL = 10

itemList = []
# Ancestor Silk
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_cloth_base_harvestersilk.png&ItemID=3799&ItemNamePattern=Ancestor+Silk&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=20,
    minNumber=100,
    requestInterval=REQUEST_INTERVAL))

# Rubedo Leather
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_daedric_skin.png&ItemID=2318&ItemNamePattern=Rubedo+Leather&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=10,
    minNumber=100,
    requestInterval=REQUEST_INTERVAL))

# Dreug Wax
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_outfitter_potion_014.png&ItemID=211&ItemNamePattern=Dreugh+Wax&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=15000,
    minNumber=1,
    requestInterval=REQUEST_INTERVAL))


if __name__ == "__main__":
    while True:
        print(datetime.datetime.now())  # output time stamp
        futures = []
        with multiprocessing.Pool() as pool:
            for item in itemList:
                futures.append(pool.apply_async(item.searchItem))

            for future in futures:
                try:
                    future.get()
                except Exception as e:
                    pass
                    #print("    Error = %s : %s" % (type(e), e))


