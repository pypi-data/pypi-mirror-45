from typing import Optional
from botocore.client import BaseClient
from typing import Dict
from typing import Union
from botocore.paginate import Paginator
from datetime import datetime
from botocore.waiter import Waiter


class Client(BaseClient):
    def can_paginate(self, operation_name: str = None):
        pass

    def generate_data_set(self, dataSetType: str, dataSetPublicationDate: datetime, roleNameArn: str, destinationS3BucketName: str, snsTopicArn: str, destinationS3Prefix: str = None, customerDefinedValues: Dict = None) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None):
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def start_support_data_export(self, dataSetType: str, fromDate: datetime, roleNameArn: str, destinationS3BucketName: str, snsTopicArn: str, destinationS3Prefix: str = None, customerDefinedValues: Dict = None) -> Dict:
        pass
