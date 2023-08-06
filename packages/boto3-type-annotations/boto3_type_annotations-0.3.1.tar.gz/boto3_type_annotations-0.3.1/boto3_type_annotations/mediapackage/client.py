from typing import Optional
from botocore.client import BaseClient
from typing import Dict
from typing import Union
from botocore.paginate import Paginator
from botocore.waiter import Waiter
from typing import List


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None):
        pass

    def create_channel(self, Id: str, Description: str = None, Tags: Dict = None) -> Dict:
        pass

    def create_origin_endpoint(self, ChannelId: str, Id: str, CmafPackage: Dict = None, DashPackage: Dict = None, Description: str = None, HlsPackage: Dict = None, ManifestName: str = None, MssPackage: Dict = None, StartoverWindowSeconds: int = None, Tags: Dict = None, TimeDelaySeconds: int = None, Whitelist: List = None) -> Dict:
        pass

    def delete_channel(self, Id: str) -> Dict:
        pass

    def delete_origin_endpoint(self, Id: str) -> Dict:
        pass

    def describe_channel(self, Id: str) -> Dict:
        pass

    def describe_origin_endpoint(self, Id: str) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None):
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def list_channels(self, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def list_origin_endpoints(self, ChannelId: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def list_tags_for_resource(self, ResourceArn: str) -> Dict:
        pass

    def rotate_channel_credentials(self, Id: str) -> Dict:
        pass

    def rotate_ingest_endpoint_credentials(self, Id: str, IngestEndpointId: str) -> Dict:
        pass

    def tag_resource(self, ResourceArn: str, Tags: Dict):
        pass

    def untag_resource(self, ResourceArn: str, TagKeys: List):
        pass

    def update_channel(self, Id: str, Description: str = None) -> Dict:
        pass

    def update_origin_endpoint(self, Id: str, CmafPackage: Dict = None, DashPackage: Dict = None, Description: str = None, HlsPackage: Dict = None, ManifestName: str = None, MssPackage: Dict = None, StartoverWindowSeconds: int = None, TimeDelaySeconds: int = None, Whitelist: List = None) -> Dict:
        pass
