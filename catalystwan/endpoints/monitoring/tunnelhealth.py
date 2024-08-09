# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from typing import Optional

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.models.monitoring.tunnelhealth import (
    TunnelHealthHistoryItem,
    TunnelHealthOverview,
    TunnelHealthRequest,
)
from catalystwan.typed_list import DataSequence


class TunnelHealth(APIEndpoints):
    @get("/statistics/tunnelhealth/history")
    def get_tunnelhealth_history(
        self, params: Optional[TunnelHealthRequest] = None
    ) -> DataSequence[TunnelHealthHistoryItem]:
        ...

    @get("/statistics/tunnelhealth/overview/{type}")
    def get_tunnelhealth_overview(
        self, type: str, params: Optional[TunnelHealthRequest] = None
    ) -> TunnelHealthOverview:
        ...
