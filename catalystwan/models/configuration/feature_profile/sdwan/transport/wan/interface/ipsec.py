# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.common import IkeCiphersuite, IkeGroup, IkeMode, IpsecCiphersuite
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, TunnelApplication

PerfectForwardSecrecy = Literal[
    "group-1",
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-24",
    "group-5",
    "none",
]


class InterfaceIpsecParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["wan/vpn/interface/ipsec"] = Field(default="wan/vpn/interface/ipsec", exclude=True, frozen=True)
    address: AddressWithMask = Field(validation_alias=AliasPath("data", "address"))
    application: Union[Variable, Global[TunnelApplication]] = Field(validation_alias=AliasPath("data", "application"))
    clear_dont_fragment: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "clearDontFragment")
    )
    if_description: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    dpd_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(10), validation_alias=AliasPath("data", "dpdInterval")
    )
    dpd_retries: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(3), validation_alias=AliasPath("data", "dpdRetries")
    )
    if_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "ifName"))
    ike_ciphersuite: Union[Variable, Global[IkeCiphersuite], Default[IkeCiphersuite]] = Field(
        default=as_default("aes256-cbc-sha1", IkeCiphersuite), validation_alias=AliasPath("data", "ikeCiphersuite")
    )
    ike_group: Union[Global[IkeGroup], Default[IkeGroup], Variable] = Field(
        default=as_default("16", IkeGroup), validation_alias=AliasPath("data", "ikeGroup")
    )
    ike_local_id: Union[Variable, Global[str], Default[None]] = Field(validation_alias=AliasPath("data", "ikeLocalId"))
    ike_rekey_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(14400), validation_alias=AliasPath("data", "ikeRekeyInterval")
    )
    ike_remote_id: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "ikeRemoteId")
    )
    ike_version: Union[Global[int], Default[int]] = Field(
        default=as_default(1), validation_alias=AliasPath("data", "ikeVersion")
    )
    ipsec_ciphersuite: Union[Variable, Global[IpsecCiphersuite], Default[IpsecCiphersuite]] = Field(
        default=as_default("aes256-gcm", IpsecCiphersuite), validation_alias=AliasPath("data", "ipsecCiphersuite")
    )
    ipsec_rekey_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(3600), validation_alias=AliasPath("data", "ipsecRekeyInterval")
    )
    ipsec_replay_window: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(512), validation_alias=AliasPath("data", "ipsecReplayWindow")
    )
    mtu: Union[Variable, Default[int], Global[int]] = Field(
        default=as_default(1500), validation_alias=AliasPath("data", "mtu")
    )
    perfect_forward_secrecy: Union[Variable, Default[PerfectForwardSecrecy], Global[PerfectForwardSecrecy]] = Field(
        default=as_default("group-16", PerfectForwardSecrecy),
        validation_alias=AliasPath("data", "perfectForwardSecrecy"),
    )
    pre_shared_secret: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "preSharedSecret"))
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True), validation_alias=AliasPath("data", "shutdown")
    )
    tcp_mss_adjust: Union[Variable, Global[int], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "tcpMssAdjust")
    )
    tunnel_destination: AddressWithMask = Field(validation_alias=AliasPath("data", "tunnelDestination"))
    tunnel_source: AddressWithMask = Field(validation_alias=AliasPath("data", "tunnelSource"))
    ike_mode: Optional[Union[Variable, Global[IkeMode], Default[Literal["main"]]]] = Field(
        default=None, validation_alias=AliasPath("data", "ikeMode")
    )
    tracker: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tracker")
    )
    tunnel_route_via: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelRouteVia")
    )
    tunnel_source_interface: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelSourceInterface")
    )
