from typing import Dict
from typing import List
from botocore.waiter import Waiter


class FleetStarted(Waiter):
    def wait(self, Names: List = None, NextToken: str = None, WaiterConfig: Dict = None):
        pass


class FleetStopped(Waiter):
    def wait(self, Names: List = None, NextToken: str = None, WaiterConfig: Dict = None):
        pass
