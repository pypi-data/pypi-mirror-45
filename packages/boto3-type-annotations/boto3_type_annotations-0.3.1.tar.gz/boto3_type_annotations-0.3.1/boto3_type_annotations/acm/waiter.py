from typing import Dict
from botocore.waiter import Waiter


class CertificateValidated(Waiter):
    def wait(self, CertificateArn: str, WaiterConfig: Dict = None):
        pass
