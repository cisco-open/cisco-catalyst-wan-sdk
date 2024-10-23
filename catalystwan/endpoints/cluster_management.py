# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import JSON, APIEndpoints, get, post, put
from catalystwan.typed_list import DataSequence
from catalystwan.utils.persona import Persona

TenancyModes = Literal["SingleTenant", "MultiTenant"]


class TenancyMode(BaseModel):
    mode: TenancyModes
    deploymentmode: str
    domain: Optional[str] = None
    clusterid: Optional[str] = None


class VManageDetails(BaseModel):
    service: str
    enabled: bool
    status: str


class ConnectedDevice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    uuid: str
    device_id: str = Field(serialization_alias="deviceId", validation_alias="deviceId")


class VManageSetup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vmanage_id: Optional[str] = Field(default=None, serialization_alias="vmanageID", validation_alias="vmanageID")
    device_ip: str = Field(serialization_alias="deviceIP", validation_alias="deviceIP")
    username: str
    password: str
    gen_csr: Optional[bool] = Field(default=None, serialization_alias="genCSR", validation_alias="genCSR")
    persona: Persona
    services: Optional[Dict[str, Dict[str, bool]]] = Field(default=None)


class ClusterManagement(APIEndpoints):
    def add_or_update_user_credentials(self):
        # POST /clusterManagement/userCreds
        ...

    @post("/clusterManagement/setup")
    def add_vmanage(self, payload: VManageSetup) -> JSON:
        # POST /clusterManagement/setup
        ...

    def check_if_cluster_locked(self):
        # GET /clusterManagement/clusterLocked
        ...

    def configure_vmanage(self):
        # POST /clusterManagement/configure
        ...

    @put("/clusterManagement/setup")
    def edit_vmanage(self, payload: VManageSetup) -> JSON:
        # PUT /clusterManagement/setup
        ...

    def get_cluster_workflow_version(self):
        # GET /clusterManagement/clusterworkflow/version
        ...

    def get_configured_ip_list(self):
        # GET /clusterManagement/iplist/{vmanageID}
        ...

    @get("/clusterManagement/connectedDevices/{vmanageIP}", "data")
    def get_connected_devices(self, vmanageIP: str) -> DataSequence[ConnectedDevice]:
        ...

    def get_connected_devices_per_tenant(self):
        # GET /clusterManagement/{tenantId}/connectedDevices/{vmanageIP}
        ...

    @get("/clusterManagement/tenancy/mode", "data")
    def get_tenancy_mode(self) -> TenancyMode:
        ...

    def get_tenants_list(self):
        # GET /clusterManagement/tenantList
        ...

    @get("/clusterManagement/vManage/details/{vmanageIP}", "data")
    def get_vmanage_details(self, vmanageIP: str) -> DataSequence[VManageDetails]:
        ...

    def health_details(self):
        # GET /clusterManagement/health/details
        ...

    def health_status_info(self):
        # GET /clusterManagement/health/status
        ...

    def health_summary(self):
        # GET /clusterManagement/health/summary
        ...

    def is_cluster_ready(self):
        # GET /clusterManagement/isready
        ...

    def list_vmanages(self):
        # GET /clusterManagement/list
        ...

    def node_properties(self):
        # GET /clusterManagement/nodeProperties
        ...

    def perform_replication_and_rebalance_of_kafka_partitions(self):
        # PUT /clusterManagement/replicateAndRebalance
        ...

    def remove_vmanage(self):
        # POST /clusterManagement/remove
        ...

    def set_tenancy_mode(self):
        # POST /clusterManagement/tenancy/mode
        ...
