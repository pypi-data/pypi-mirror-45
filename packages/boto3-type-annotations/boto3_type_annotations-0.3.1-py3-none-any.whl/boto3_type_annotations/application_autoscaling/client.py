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

    def delete_scaling_policy(self, PolicyName: str, ServiceNamespace: str, ResourceId: str, ScalableDimension: str) -> Dict:
        pass

    def delete_scheduled_action(self, ServiceNamespace: str, ScheduledActionName: str, ResourceId: str, ScalableDimension: str) -> Dict:
        pass

    def deregister_scalable_target(self, ServiceNamespace: str, ResourceId: str, ScalableDimension: str) -> Dict:
        pass

    def describe_scalable_targets(self, ServiceNamespace: str, ResourceIds: List = None, ScalableDimension: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def describe_scaling_activities(self, ServiceNamespace: str, ResourceId: str = None, ScalableDimension: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def describe_scaling_policies(self, ServiceNamespace: str, PolicyNames: List = None, ResourceId: str = None, ScalableDimension: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def describe_scheduled_actions(self, ServiceNamespace: str, ScheduledActionNames: List = None, ResourceId: str = None, ScalableDimension: str = None, MaxResults: int = None, NextToken: str = None) -> Dict:
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None, HttpMethod: str = None):
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        pass

    def put_scaling_policy(self, PolicyName: str, ServiceNamespace: str, ResourceId: str, ScalableDimension: str, PolicyType: str = None, StepScalingPolicyConfiguration: Dict = None, TargetTrackingScalingPolicyConfiguration: Dict = None) -> Dict:
        pass

    def put_scheduled_action(self, ServiceNamespace: str, ScheduledActionName: str, ResourceId: str, ScalableDimension: str, Schedule: str = None, StartTime: datetime = None, EndTime: datetime = None, ScalableTargetAction: Dict = None) -> Dict:
        pass

    def register_scalable_target(self, ServiceNamespace: str, ResourceId: str, ScalableDimension: str, MinCapacity: int = None, MaxCapacity: int = None, RoleARN: str = None) -> Dict:
        pass
