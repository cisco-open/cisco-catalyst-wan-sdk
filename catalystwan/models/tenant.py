# Copyright 2023 Cisco Systems, Inc. and its affiliates

from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress


class MTEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    uuid: str
    configured_hostname: Optional[str] = Field(
        serialization_alias="configuredHostname", validation_alias="configuredHostname"
    )
    configured_system_ip: Optional[IPvAnyAddress] = Field(
        serialization_alias="configuredSystemIP", validation_alias="configuredSystemIP"
    )
    management_system_ip: Optional[IPvAnyAddress] = Field(
        serialization_alias="managementSystemIP", validation_alias="managementSystemIP"
    )
    device_model: Optional[str] = Field(serialization_alias="deviceModel", validation_alias="deviceModel")
    device_type: Optional[str] = Field(serialization_alias="deviceType", validation_alias="deviceType")


class TenantVPNMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tenant_vpn: int = Field(serialization_alias="tenantVPN", validation_alias="tenantVPN")
    device_vpn: int = Field(serialization_alias="deviceVPN", validation_alias="deviceVPN")


class Tenant(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    desc: str
    org_name: str = Field(serialization_alias="orgName", validation_alias="orgName")
    subdomain: str = Field(serialization_alias="subDomain", validation_alias="subDomain")
    flake_id: Optional[int] = Field(default=None, serialization_alias="flakeId", validation_alias="flakeId")
    vbond_address: Optional[str] = Field(
        default=None, serialization_alias="vBondAddress", validation_alias="vBondAddress"
    )
    edge_connector_system_ip: Optional[str] = Field(
        default=None, serialization_alias="edgeConnectorSystemIp", validation_alias="edgeConnectorSystemIp"
    )
    edge_connector_enable: Optional[bool] = Field(
        default=None, serialization_alias="edgeConnectorEnable", validation_alias="edgeConnectorEnable"
    )
    vsmarts: Optional[List[str]] = Field(default=None, serialization_alias="vSmarts", validation_alias="vSmarts")
    wan_edge_forecast: Optional[int] = Field(
        default=None, serialization_alias="wanEdgeForecast", validation_alias="wanEdgeForecast"
    )
    saml_sp_info: Optional[str] = Field(default=None, serialization_alias="samlSpInfo", validation_alias="samlSpInfo")
    idp_map: Union[Dict, str, None] = Field(default=None, serialization_alias="idpMap", validation_alias="idpMap")
    config_db_cluster_service_name: Optional[str] = Field(
        default=None, serialization_alias="configDBClusterServiceName", validation_alias="configDBClusterServiceName"
    )
    old_idp_map: Union[Dict, str, None] = Field(
        default=None, serialization_alias="oldIdpMap", validation_alias="oldIdpMap"
    )
    created_at: Optional[datetime] = Field(default=None, serialization_alias="createdAt", validation_alias="createdAt")
    rid: Optional[int] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")
    edge_connector_tunnel_interface_name: Optional[str] = Field(
        default=None,
        serialization_alias="edgeConnectorTunnelInterfaceName",
        validation_alias="edgeConnectorTunnelInterfaceName",
    )
    tenant_id: Optional[str] = Field(default=None, serialization_alias="tenantId", validation_alias="tenantId")
    sp_metadata: Optional[str] = Field(default=None, serialization_alias="spMetadata", validation_alias="spMetadata")
    state: Optional[str] = None
    wan_edge_present: Optional[int] = Field(
        default=None, serialization_alias="wanEdgePresent", validation_alias="wanEdgePresent"
    )
    mt_edge: Optional[List[MTEdge]] = Field(default=None, serialization_alias="mtEdge", validation_alias="mtEdge")
    mt_edge_count: Optional[int] = Field(
        default=None, serialization_alias="mtEdgeCount", validation_alias="mtEdgeCount"
    )
    tenant_vpn_map: Optional[List[TenantVPNMap]] = Field(
        default=None, serialization_alias="tenantVPNmap", validation_alias="tenantVPNmap"
    )
    tenant_provider_vpn_count: Optional[int] = Field(
        default=None, serialization_alias="tenantProviderVPNCount", validation_alias="tenantProviderVPNCount"
    )


class TenantExport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    desc: str
    org_name: str = Field(serialization_alias="orgName", validation_alias="orgName")
    subdomain: str = Field(serialization_alias="subDomain", validation_alias="subDomain")
    wan_edge_forecast: Optional[int] = Field(
        default=None, serialization_alias="wanEdgeForecast", validation_alias="wanEdgeForecast"
    )
    is_destination_overlay_mt: Optional[bool] = Field(
        default=None,
        serialization_alias="isDestinationOverlayMT",
        validation_alias="isDestinationOverlayMT",
        description="required starting from 20.13",
    )
    migration_key: Optional[str] = Field(
        default=None,
        serialization_alias="migrationKey",
        validation_alias="migrationKey",
        pattern=r"^[a-zA-Z0-9]{8,32}$",
        description="required starting from 20.13",
    )
