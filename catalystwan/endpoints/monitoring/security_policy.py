# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.models.monitoring.security_policy import SecurityPolicyDeviceList


class MonitoringSecurityPolicy(APIEndpoints):
    @get("/security/policy/devicelist", "data")
    def get_device_list(self) -> SecurityPolicyDeviceList:
        ...
