# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from catalystwan.endpoints import APIEndpoints, get, post, put, delete
from catalystwan.models.url_monitoring import UrlMonitoringConfig, UrlMonitoringInfo, DeleteUrlMonitorRequest
from catalystwan.typed_list import DataSequence


class UrlMonitoring(APIEndpoints):
    @get("/url/monitor")
    def get_url_monitor(self) -> DataSequence[UrlMonitoringInfo]:
        ...

    @post("/url/monitor")
    def add_url_monitor(self, payload: UrlMonitoringConfig) -> None:
        ...

    @put("/url/monitor")
    def update_url_monitor(self, payload: UrlMonitoringConfig) -> None:
        ...

    @delete("/url/monitor")
    def delete_url_monitor(self, params: DeleteUrlMonitorRequest) -> None:
        ...
