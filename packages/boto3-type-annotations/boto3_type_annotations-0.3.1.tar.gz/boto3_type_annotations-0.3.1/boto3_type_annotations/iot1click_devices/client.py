from typing import Optional
from botocore.client import BaseClient
from typing import Dict
from typing import Union
from botocore.paginate import Paginator
from datetime import datetime
from botocore.waiter import Waiter
from typing import List


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None):
        pass

    def claim_devices_by_claim_code(self, ClaimCode: str) -> Dict:
        pass

    def describe_device(self, DeviceId: str) -> Dict:
        pass

    def finalize_device_claim(self, DeviceId: str, Tags: Dict = None) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None):
        pass

    def get_device_methods(self, DeviceId: str) -> Dict:
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def initiate_device_claim(self, DeviceId: str) -> Dict:
        pass

    def invoke_device_method(self, DeviceId: str, DeviceMethod: Dict = None, DeviceMethodParameters: str = None) -> Dict:
        pass

    def list_device_events(self, DeviceId: str, FromTimeStamp: datetime, ToTimeStamp: datetime, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def list_devices(self, DeviceType: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def list_tags_for_resource(self, ResourceArn: str) -> Dict:
        pass

    def tag_resource(self, ResourceArn: str, Tags: Dict):
        pass

    def unclaim_device(self, DeviceId: str) -> Dict:
        pass

    def untag_resource(self, ResourceArn: str, TagKeys: List):
        pass

    def update_device_state(self, DeviceId: str, Enabled: bool = None) -> Dict:
        pass
