# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.topology_group import (
    ActivateRequest,
    DeployResponse,
    Preview,
    TopologyGroup,
    TopologyGroupId,
)
from catalystwan.typed_list import DataSequence


class TopologyGroupEndpoints(APIEndpoints):
    @post("/v1/topology-group")
    @versions(">=20.12")
    def create(self, payload: TopologyGroup) -> TopologyGroupId:
        ...

    @put("/v1/topology-group/{group_id}")
    @versions(">=20.12")
    def edit(self, group_id: UUID, payload: TopologyGroup) -> TopologyGroupId:
        ...

    @get("/v1/topology-group/{group_id}")
    @versions(">=20.12")
    def get_by_id(self, group_id: UUID) -> TopologyGroup:
        ...

    @get("/v1/topology-group")
    @versions(">=20.12")
    def get_all(self) -> DataSequence[TopologyGroupId]:
        ...

    @delete("/v1/topology-group/{group_id}")
    @versions(">=20.12")
    def delete(self, group_id: UUID) -> None:
        ...

    @post("/v1/topology-group/{group_id}/device/{device_id}/preview")
    @versions(">=20.12")
    def preview(self, group_id: UUID, device_id: UUID, payload: ActivateRequest) -> Preview:
        ...

    @post("/v1/topology-group/{group_id}/device/deploy")
    @versions(">=20.12")
    def deploy(self, group_id: UUID, payload: ActivateRequest) -> DeployResponse:
        ...
