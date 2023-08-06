from .APIResponse import APIResponse
class BaseSkin(APIResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skinId1 = kwargs.get("skin_id1", 0) if kwargs is not None else 0
        self.skinId2 = kwargs.get("skin_id2", 0) if kwargs is not None else 0
        self.skinName = kwargs.get("skin_name", None) if kwargs is not None else None
        self.skinNameEnglish = kwargs.get("skin_name_english", None) if kwargs is not None else None
        self.obtainability = kwargs.get("rarity", kwargs.get("obtainability", None)) if kwargs is not None else None
    def __eq__(self, other):
        return self.skinID1 == other.skinID1 and self.skinID2 == other.skinID2
