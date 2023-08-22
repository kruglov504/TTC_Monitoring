from ItemMonitoringProcess import ItemMonitoringProcess
import multiprocessing


itemList = []
# Ancestor Silk
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_cloth_base_harvestersilk.png&ItemID=3799&ItemNamePattern=Ancestor+Silk&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=20,
    minNumber=100,
    requestInterval=10))

# Rubedo Leather
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_daedric_skin.png&ItemID=2318&ItemNamePattern=Rubedo+Leather&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=10,
    minNumber=100,
    requestInterval=20))

# Dreug Wax
itemList.append(ItemMonitoringProcess(
    url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_outfitter_potion_014.png&ItemID=211&ItemNamePattern=Dreugh+Wax&SortBy=LastSeen&Order=desc',
    urlTimeout=10,
    maxPrice=15000,
    minNumber=1,
    requestInterval=30))


if __name__ == "__main__":

    proc = []
    for item in itemList:
        p = multiprocessing.Process(target=item.searchItem)
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

