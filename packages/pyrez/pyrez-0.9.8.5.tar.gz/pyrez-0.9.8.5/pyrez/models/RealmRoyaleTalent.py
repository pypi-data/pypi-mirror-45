from .APIResponse import APIResponse
class RealmRoyaleTalent(APIResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categoryName = kwargs.get("category_name", None) if kwargs is not None else None
        self.itemId = kwargs.get("item_id", 0) if kwargs is not None else 0
        self.lootTableItemId = kwargs.get("loot_table_item_id", 0) if kwargs is not None else 0
        self.talentDescription = kwargs.get("talent_description", None) if kwargs is not None else None
        self.talentName = kwargs.get("talent_name", None) if kwargs is not None else None
