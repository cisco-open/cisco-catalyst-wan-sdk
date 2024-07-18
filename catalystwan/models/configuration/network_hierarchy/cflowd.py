# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global, as_optional_global

Protocol = Literal[
    "both",
    "ipv4",
    "ipv6",
]


class CustomizedIpv4RecordFields(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    collect_dscp_output: Optional[Global[bool]] = Field(
        default=Global[bool](value=False), validation_alias="collectDscpOutput", serialization_alias="collectDscpOutput"
    )
    collect_tos: Optional[Global[bool]] = Field(
        default=Global[bool](value=False), validation_alias="collectTos", serialization_alias="collectTos"
    )


class Collectors(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    address: Optional[Global[str]] = Field(default=None)
    bfd_metrics_export: Optional[Global[bool]] = Field(
        default=Global[bool](value=False), validation_alias="bfdMetricsExport", serialization_alias="bfdMetricsExport"
    )
    export_interval: Optional[Global[int]] = Field(
        default=Global[int](value=600), validation_alias="exportInterval", serialization_alias="exportInterval"
    )
    export_spread: Optional[Global[bool]] = Field(
        default=Global[bool](value=False), validation_alias="exportSpread", serialization_alias="exportSpread"
    )
    udp_port: Optional[Global[int]] = Field(
        default=Global[int](value=4739), validation_alias="udpPort", serialization_alias="udpPort"
    )
    vpn_id: Optional[Global[int]] = Field(default=None, validation_alias="vpnId", serialization_alias="vpnId")


class CflowdParcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    type_: Literal["cflowd"] = Field(default="cflowd", exclude=True)
    parcel_name: str = Field(
        default="Cflowd",
        exclude=True,
        description="This field is not defined for this model",
        serialization_alias="name",
        validation_alias="name",
    )
    collect_tloc_loopback: Optional[Global[bool]] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "collectTlocLoopback")
    )
    collectors: Optional[List[Collectors]] = Field(
        default=None, description="Collectors list", validation_alias=AliasPath("data", "collectors")
    )
    customized_ipv4_record_fields: Optional[CustomizedIpv4RecordFields] = Field(
        default=None,
        validation_alias=AliasPath("data", "customizedIpv4RecordFields"),
        description="Custom IPV4 flow record fields",
    )
    flow_active_timeout: Optional[Global[int]] = Field(
        default=Global[int](value=600), validation_alias=AliasPath("data", "flowActiveTimeout")
    )
    flow_inactive_timeout: Optional[Global[int]] = Field(
        default=Global[int](value=60), validation_alias=AliasPath("data", "flowInactiveTimeout")
    )
    flow_refresh_time: Optional[Global[int]] = Field(
        default=Global[int](value=600), validation_alias=AliasPath("data", "flowRefreshTime")
    )
    flow_sampling_interval: Optional[Global[int]] = Field(
        default=Global[int](value=1), validation_alias=AliasPath("data", "flowSamplingInterval")
    )
    protocol: Optional[Global[Protocol]] = Field(default=None, validation_alias=AliasPath("data", "protocol"))

    def add_collector(
        self,
        address: Optional[str] = None,
        bfd_metrics_export: Optional[bool] = False,
        export_interval: Optional[int] = 600,
        export_spread: Optional[bool] = False,
        udp_port: Optional[int] = 4739,
        vpn_id: Optional[int] = None,
    ):
        if self.collectors is None:
            self.collectors = []
        self.collectors.append(
            Collectors(
                address=as_optional_global(address),
                udp_port=as_optional_global(udp_port),
                vpn_id=as_optional_global(vpn_id),
                export_spread=as_optional_global(export_spread),
                bfd_metrics_export=as_optional_global(bfd_metrics_export),
                export_interval=as_optional_global(export_interval),
            )
        )

    def set_customized_ipv4_record_fields(
        self, collect_dscp_output: Optional[bool] = False, collect_tos: Optional[bool] = False
    ):
        self.customized_ipv4_record_fields = CustomizedIpv4RecordFields(
            collect_dscp_output=as_optional_global(collect_dscp_output), collect_tos=as_optional_global(collect_tos)
        )

    def set_flow(
        self,
        active_timeout: Optional[int] = 600,
        inactive_timeout: Optional[int] = 60,
        refresh_time: Optional[int] = 600,
        sampling_interval: Optional[int] = 1,
    ):
        self.flow_active_timeout = as_optional_global(active_timeout)
        self.flow_inactive_timeout = as_optional_global(inactive_timeout)
        self.flow_refresh_time = as_optional_global(refresh_time)
        self.flow_sampling_interval = as_optional_global(sampling_interval)

    def set_protocol(self, protocol: Protocol):
        self.protocol = as_global(protocol, Protocol)
