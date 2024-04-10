# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions, view
from catalystwan.models.tenant import Tenant
from catalystwan.typed_list import DataSequence
from catalystwan.utils.session_type import ProviderAsTenantView, ProviderView


class TenantDeleteRequest(BaseModel):
    password: str


class TenantBulkDeleteRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    password: str
    tenant_id_list: List[str] = Field(serialization_alias="tenantIdList", validation_alias="tenantIdList")


class TenantTaskId(BaseModel):
    id: str


class CertificatesStatus(BaseModel):
    invalid: int
    warning: int
    revoked: int


class ControlStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    control_up: int = Field(serialization_alias="controlUp", validation_alias="controlUp")
    partial: int
    control_down: int = Field(serialization_alias="controlDown", validation_alias="controlDown")


class SiteHealth(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    full_connectivity: int = Field(serialization_alias="fullConnectivity", validation_alias="fullConnectivity")
    partial_connectivity: int = Field(serialization_alias="partialConnectivity", validation_alias="partialConnectivity")
    no_connectivity: int = Field(serialization_alias="noConnectivity", validation_alias="noConnectivity")


class vEdgeHealth(BaseModel):
    normal: int
    warning: int
    error: int


class vSmartStatus(BaseModel):
    up: int
    down: int


class TenantStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tenant_id: str = Field(serialization_alias="tenantId", validation_alias="tenantId")
    tenant_name: str = Field(serialization_alias="tenantName", validation_alias="tenantName")
    control_status: ControlStatus = Field(serialization_alias="controlStatus", validation_alias="controlStatus")
    site_health: SiteHealth = Field(serialization_alias="siteHealth", validation_alias="siteHealth")
    vedge_health: vEdgeHealth = Field(serialization_alias="vEdgeHealth", validation_alias="vEdgeHealth")
    vsmart_status: vSmartStatus = Field(serialization_alias="vSmartStatus", validation_alias="vSmartStatus")


class TenantUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tenant_id: str = Field(serialization_alias="tenantId", validation_alias="tenantId")
    subdomain: str = Field(serialization_alias="subDomain", validation_alias="subDomain")
    desc: str
    wan_edge_forecast: Optional[int] = Field(serialization_alias="wanEdgeForecast", validation_alias="wanEdgeForecast")
    edge_connector_enable: Optional[bool] = Field(
        serialization_alias="edgeConnectorEnable", validation_alias="edgeConnectorEnable"
    )
    edge_connector_system_ip: Optional[str] = Field(
        default=None, serialization_alias="edgeConnectorSystemIp", validation_alias="edgeConnectorSystemIp"
    )
    edge_connector_tunnel_interface_name: Optional[str] = Field(
        default=None,
        serialization_alias="edgeConnectorTunnelInterfaceName",
        validation_alias="edgeConnectorTunnelInterfaceName",
    )

    @classmethod
    def from_tenant(cls, tenant: Tenant) -> "TenantUpdateRequest":
        """Creates payload for tenant update from existing tenant data obtained by GET

        Args:
            tenant (Tenant): Tenant to be updated

        Raises:
            TypeError: When provided tenant is missing ID

        Returns:
            TenantUpdateRequest: Tenant attributes suitable for PUT request
        """
        if not tenant.tenant_id:
            raise TypeError("tenantId required for update request")
        return TenantUpdateRequest(
            tenant_id=tenant.tenant_id,
            desc=tenant.desc,
            subdomain=tenant.subdomain,
            wan_edge_forecast=tenant.wan_edge_forecast,
            edge_connector_enable=tenant.edge_connector_enable,
            edge_connector_system_ip=tenant.edge_connector_system_ip,
            edge_connector_tunnel_interface_name=tenant.edge_connector_tunnel_interface_name,
        )


class vSmartPlacementUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    src_vsmart_uuid: str = Field(serialization_alias="srcvSmartUuid", validation_alias="srcvSmartUuid")
    dest_vsmart_uuid: str = Field(serialization_alias="destvSmartUuid", validation_alias="destvSmartUuid")


class vSmartTenantCapacity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vsmart_uuid: str = Field(serialization_alias="vSmartUuid", validation_alias="vSmartUuid")
    total_tenant_capacity: int = Field(
        serialization_alias="totalTenantCapacity", validation_alias="totalTenantCapacity"
    )
    current_tenant_count: int = Field(serialization_alias="currentTenantCount", validation_alias="currentTenantCount")


class vSmartTenantMap(BaseModel):
    data: Dict[str, List[Tenant]]


class vSessionId(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vsessionid: str = Field(serialization_alias="VSessionId", validation_alias="VSessionId")


class TenantManagement(APIEndpoints):
    @view({ProviderView})
    @post("/tenant")
    def create_tenant(self, payload: Tenant) -> Tenant:
        ...

    @view({ProviderView})
    @post("/tenant/async")
    def create_tenant_async(self, payload: Tenant) -> TenantTaskId:
        ...

    @versions(">=20.4")
    @view({ProviderView})
    @post("/tenant/bulk/async")
    def create_tenant_async_bulk(self, payload: List[Tenant]) -> TenantTaskId:
        ...

    @view({ProviderView})
    @delete("/tenant/{tenant_id}/delete")
    def delete_tenant(self, tenant_id: str, payload: TenantDeleteRequest) -> None:
        ...

    @versions(">=20.4")
    @view({ProviderView})
    @delete("/tenant/bulk/async")
    def delete_tenant_async_bulk(self, payload: TenantBulkDeleteRequest) -> TenantTaskId:
        ...

    def force_status_collection(self):
        # POST /tenantstatus/force
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenantstatus", "data")
    def get_all_tenant_statuses(self) -> DataSequence[TenantStatus]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant", "data")
    def get_all_tenants(self) -> DataSequence[Tenant]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant/{tenant_id}")
    def get_tenant(self, tenant_id: str) -> Tenant:
        ...

    @view({ProviderView})
    @get("/tenant/vsmart/capacity", "data")
    def get_tenant_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant/vsmart")
    def get_tenant_vsmart_mapping(self) -> vSmartTenantMap:
        ...

    def switch_tenant(self):
        # POST /tenant/{tenantId}/switch
        ...

    def tenant_vsmart_mt_migrate(self):
        # POST /tenant/vsmart-mt/migrate
        ...

    @view({ProviderView})
    @put("/tenant/{tenant_id}")
    def update_tenant(self, tenant_id: str, payload: TenantUpdateRequest) -> Tenant:
        ...

    @view({ProviderView})
    @put("/tenant/{tenant_id}/vsmart")
    def update_tenant_vsmart_placement(self, tenant_id: str, payload: vSmartPlacementUpdateRequest) -> None:
        ...

    @view({ProviderView})
    @post("/tenant/{tenant_id}/vsessionid")
    def vsession_id(self, tenant_id: str) -> vSessionId:
        ...
