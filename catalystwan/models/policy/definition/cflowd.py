# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import VpnId
from catalystwan.models.policy.policy_definition import (
    Optimized,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)

IpProtocol = Literal["ipv4", "ipv6", "both"]
TransportProtocol = Literal["transport_udp", "transport_tcp"]
ExportState = Literal["enable"]


class Collector(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vpn: VpnId
    address: str
    port: int = Field(ge=1024, le=65536)
    transport: TransportProtocol
    source_interface: str = Field(
        default=None, validation_alias="sourceInterface", serialization_alias="sourceInterface"
    )
    export_spread: Optional[ExportState] = Field(
        default=None, validation_alias="exportSpread", serialization_alias="exportSpread"
    )
    bfd_metrics_export: Optional[ExportState] = Field(
        default=None, validation_alias="bfd-metrics-export", serialization_alias="bfd-metrics-export"
    )
    export_interval: Optional[int] = Field(
        default=None, validation_alias="export-interval", serialization_alias="export-interval", ge=0, le=86400
    )

    def enable_bfd_metrics_exporting(self, export_interval: int):
        self.bfd_metrics_export = "enable"
        self.export_interval = export_interval


class CustomizedIpv4RecordFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    collect_tos: bool = Field(default=False, validation_alias="collectTos", serialization_alias="collectTos")
    collect_dscp_output: bool = Field(
        default=False, validation_alias="collectDscpOutput", serialization_alias="collectDscpOutput"
    )


class CflowdDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    collectors: List[Collector] = []
    protocol: IpProtocol = "ipv4"

    flow_active_timeout: Optional[int] = Field(
        default=None, validation_alias="flowActiveTimeout", serialization_alias="flowActiveTimeout", ge=30, le=3600
    )

    flow_inactive_timeout: Optional[int] = Field(
        default=None, validation_alias="flowInactiveTimeout", serialization_alias="flowInactiveTimeout", ge=1, le=3600
    )

    template_refresh: Optional[int] = Field(
        default=None, validation_alias="templateRefresh", serialization_alias="templateRefresh", ge=60, le=86400
    )

    flow_sampling_interval: Optional[int] = Field(
        default=None,
        validation_alias="flowSamplingInterval",
        serialization_alias="flowSamplingInterval",
        ge=1,
        le=65536,
    )

    customized_ipv4_record_fields: CustomizedIpv4RecordFields = Field(
        default=CustomizedIpv4RecordFields(),
        validation_alias="customizedIpv4RecordFields",
        serialization_alias="customizedIpv4RecordFields",
    )


class CflowdPolicy(PolicyDefinitionBase):
    type: Literal["cflowd"] = "cflowd"
    optimized: Optional[Optimized] = None
    definition: CflowdDefinition


class CflowdPolicyEditPayload(CflowdPolicy, PolicyDefinitionId):
    pass


class CflowdPolicyGetResponse(CflowdPolicy, PolicyDefinitionGetResponse):
    pass
