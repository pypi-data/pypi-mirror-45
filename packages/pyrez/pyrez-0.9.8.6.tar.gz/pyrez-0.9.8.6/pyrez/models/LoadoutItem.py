class LoadoutItem:
    def __init__(self, **kwargs):
        self.itemId = kwargs.get("ItemId", 0) if kwargs else 0
        self.itemName = kwargs.get("ItemName", None) if kwargs else None
        self.points = kwargs.get("Points", 0) if kwargs else 0
    def __str__(self):
        return "{}({})".format(self.itemName, self.points)
