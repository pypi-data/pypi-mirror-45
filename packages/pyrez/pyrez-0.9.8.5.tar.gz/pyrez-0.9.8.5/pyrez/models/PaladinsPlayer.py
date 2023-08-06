from .BasePSPlayer import BasePSPlayer
from .Ranked import Ranked
from pyrez.enumerations import Tier
class PaladinsPlayer(BasePSPlayer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platform = kwargs.get("Platform", None) if kwargs is not None else None
        self.rankedController = Ranked(**kwargs.get("RankedController", None)) if kwargs is not None else None
        self.rankedKeyboard = Ranked(**kwargs.get("RankedKBM", None)) if kwargs is not None else None
        self.playerRankController = Tier(kwargs.get("Tier_RankedController", 0)) if kwargs is not None else None
        self.playerRankKeyboard = Tier(kwargs.get("Tier_RankedKBM", 0)) if kwargs is not None else None
