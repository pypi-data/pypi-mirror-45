from .APIResponse import APIResponse
class LinkedAccount(APIResponse):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accountId = kwargs.get("accountId", None) if kwargs else None
        self.copied = kwargs.get("copied", False) if kwargs else False
        self.gamerTag = kwargs.get("gamerTag", None) if kwargs else None
        self.portalId = kwargs.get("platform", None) if kwargs else None
