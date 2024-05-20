# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.models.monitoring.server_info import ServerInfoResponse


class ServerInfo(APIEndpoints):
    @get("/server/info")
    def get_server_info(self) -> ServerInfoResponse:
        ...
