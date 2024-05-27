# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, versions
from catalystwan.models.configuration.topology_group import TopologyGroup, TopologyGroupId
from catalystwan.typed_list import DataSequence


class TopologyGroupEndpoints(APIEndpoints):
    @post("/v1/topology-group")
    @versions(">=20.12")
    def create_topology_group(self, payload: TopologyGroup) -> TopologyGroupId:
        ...

    @get("/v1/topology-group")
    @versions(">=20.12")
    def get_all(self) -> DataSequence[TopologyGroupId]:
        ...

    @delete("/v1/topology-group/{group_id}")
    @versions(">=20.12")
    def delete(self, group_id: UUID) -> None:
        ...
