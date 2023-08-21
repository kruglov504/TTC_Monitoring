

#import threading
from ItemMonitoringProcess import ItemMonitoringProcess
import multiprocessing
import time



if __name__ == "__main__":
    itemList = []
    itemList.append(ItemMonitoringProcess(
        url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_cloth_base_harvestersilk.png&ItemID=3799&ItemNamePattern=Ancestor+Silk&SortBy=LastSeen&Order=desc',
        urlTimeout=3,
        maxPrice=70,
        minNumber=100,
        requestInterval=10))

    itemList.append(ItemMonitoringProcess(
        url='https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?IconName=crafting_daedric_skin.png&ItemID=2318&ItemNamePattern=Rubedo+Leather&SortBy=LastSeen&Order=desc',
        urlTimeout=3,
        maxPrice=40,
        minNumber=100,
        requestInterval=10))

    futures = []
    with multiprocessing.Pool() as pool:
        for item in itemList:
            futures.append(pool.apply_async(item.searchItem))

        for future in futures:
            try:
                future.get()
            except Exception as e:
                print("    Error = %s : %s" % (type(e), e))


