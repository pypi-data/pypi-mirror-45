# Usage 1
```py
from pyrez.api import PaladinsAPI

paladinsAPI = PaladinsAPI(devId=1004, authKey="23DF3C7E9BD14D84BF892AD206B6755C")
matches = paladinsAPI.getMatchIdsByQueue(486, "20190329", "10,30")

for match in matches:
	print(match)
```

# Usage 2
```py
from pyrez.api import PaladinsAPI

paladinsAPI = PaladinsAPI(devId=1004, authKey="23DF3C7E9BD14D84BF892AD206B6755C")
matches = paladinsAPI.getMatchIdsByQueue(486, "20190329", 10.30)

for match in matches:
	print(match)
```

# Usage 3
```py
from pyrez.api import PaladinsAPI
from pyrez.enumerations import PaladinsQueue

paladinsAPI = PaladinsAPI(devId=1004, authKey="23DF3C7E9BD14D84BF892AD206B6755C")
matches = paladinsAPI.getMatchIdsByQueue(PaladinsQueue.Live_Competitive_Keyboard, "20190329", "10,30")

for match in matches:
	print(match)
```

# Usage 4
```py
from pyrez.api import PaladinsAPI
from pyrez.enumerations import PaladinsQueue
from datetime import datetime

paladinsAPI = PaladinsAPI(devId=1004, authKey="23DF3C7E9BD14D84BF892AD206B6755C")
matches = paladinsAPI.getMatchIdsByQueue(PaladinsQueue.Live_Competitive_Keyboard, datetime.date(year=2019, month=3, day=29), "10,30")

for match in matches:
	print(match)
```
