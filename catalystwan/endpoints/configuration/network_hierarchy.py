# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from catalystwan.endpoints import APIEndpoints, get
from catalystwan.models.configuration.network_hierarchy import NodeInfo
from catalystwan.typed_list import DataSequence


class NetworkHierarchy(APIEndpoints):
    @get("/v1/network-hierarchy")
    def list_nodes(self) -> DataSequence[NodeInfo]:
        ...
