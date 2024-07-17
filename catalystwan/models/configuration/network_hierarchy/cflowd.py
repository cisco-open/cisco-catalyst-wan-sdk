# Copyright 2024 Cisco Systems, Inc. and its affiliates
import typing
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.configuration.feature_profile.common import arguments_as_optional_global

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
    parcel_name: Optional[str] = Field(default=None, description="This parcel does not have this field") # type: ignore
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

    @typing.no_type_check
    @arguments_as_optional_global
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
                address=address,
                udp_port=udp_port,
                vpn_id=vpn_id,
                export_spread=export_spread,
                bfd_metrics_export=bfd_metrics_export,
                export_interval=export_interval,
            )
        )

    @typing.no_type_check
    @arguments_as_optional_global
    def set_customized_ipv4_record_fields(
        self, collect_dscp_output: Optional[bool] = False, collect_tos: Optional[bool] = False
    ):
        self.customized_ipv4_record_fields = CustomizedIpv4RecordFields(
            collect_dscp_output=collect_dscp_output, collect_tos=collect_tos
        )

    @typing.no_type_check
    @arguments_as_optional_global
    def set_flow(
        self,
        active_timeout: Optional[int] = 600,
        inactive_timeout: Optional[int] = 60,
        refresh_time: Optional[int] = 600,
        sampling_interval: Optional[int] = 1,
    ):
        self.flow_active_timeout = active_timeout
        self.flow_inactive_timeout = inactive_timeout
        self.flow_refresh_time = refresh_time
        self.flow_sampling_interval = sampling_interval

    def set_protocol(self, protocol: Protocol):
        self.protocol = as_global(protocol, Protocol)
