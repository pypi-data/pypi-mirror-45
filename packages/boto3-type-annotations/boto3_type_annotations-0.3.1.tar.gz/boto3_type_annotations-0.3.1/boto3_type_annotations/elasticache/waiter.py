from typing import Dict
from botocore.waiter import Waiter


class CacheClusterAvailable(Waiter):
    def wait(self, CacheClusterId: str = None, MaxRecords: int = None, Marker: str = None, ShowCacheNodeInfo: bool = None, ShowCacheClustersNotInReplicationGroups: bool = None, WaiterConfig: Dict = None):
        pass


class CacheClusterDeleted(Waiter):
    def wait(self, CacheClusterId: str = None, MaxRecords: int = None, Marker: str = None, ShowCacheNodeInfo: bool = None, ShowCacheClustersNotInReplicationGroups: bool = None, WaiterConfig: Dict = None):
        pass


class ReplicationGroupAvailable(Waiter):
    def wait(self, ReplicationGroupId: str = None, MaxRecords: int = None, Marker: str = None, WaiterConfig: Dict = None):
        pass


class ReplicationGroupDeleted(Waiter):
    def wait(self, ReplicationGroupId: str = None, MaxRecords: int = None, Marker: str = None, WaiterConfig: Dict = None):
        pass
