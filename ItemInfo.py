

class ItemInfo:
    def __init__(self, itemName, location, guild, price, amount, lastSeen, maxPrice, minNumber):
        self.itemName = itemName
        self.location = location
        self.guild = guild
        self.price = price
        self.amount = amount
        self.lastSeen = lastSeen
        self.priceOk = float(self.price.replace(',', '')) <= maxPrice
        self.amountOk = float(self.amount.replace(',', '')) >= minNumber

    def itemOk(self):
        return self.priceOk and self.amountOk

    def printMsg(self):
        print("\033[92m", "item name: ", self.itemName +
              " | location: " + self.location +
              " | guild: " + self.guild +
              " | price: " + self.price +
              " | amount: " + self.amount +
              " | lastSeen: " + self.lastSeen, "\033[0m")

