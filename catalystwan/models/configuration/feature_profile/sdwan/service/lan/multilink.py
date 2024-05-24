from ipaddress import IPv4Address, IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import (
    MultilinkAuthenticationType,
    MultilinkControllerTxExList,
    MultilinkControllerType,
    MultilinkMethod,
    MultilinkNimList,
    RefIdItem,
)


class InterfaceMultilinkParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["lan/vpn/interface/multilink"] = Field(
        default="lan/vpn/interface/multilink", frozen=True, exclude=True
    )

    group_number: Union[Global[int], Variable] = Field(validation_alias=AliasPath("data", "groupNumber"))
    if_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "ifName"))
    method: Union[Global[MultilinkMethod], Default[None]] = Field(validation_alias=AliasPath("data", "method"))
    address_ipv4: Optional[Union[Global[IPv4Address], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv4")
    )
    address_ipv6: Optional[Union[Global[IPv6Interface], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv6")
    )
    authentication_type: Optional[
        Union[Default[MultilinkAuthenticationType], Global[MultilinkAuthenticationType], Variable]
    ] = Field(default=None, validation_alias=AliasPath("data", "authenticationType"))
    bandwidth_upstream: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthUpstream")
    )
    clear_dont_fragment_sdwan_tunnel: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "clearDontFragmentSdwanTunnel")
    )
    control_connections: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "controlConnections")
    )
    controller_tx_ex_list: Optional[List[MultilinkControllerTxExList]] = Field(
        default=None, validation_alias=AliasPath("data", "controllerTxExList")
    )
    controller_type: Global[MultilinkControllerType] = Field(
        default=Global[MultilinkControllerType](value="T1/E1"), validation_alias=AliasPath("data", "controllerType")
    )
    delay_value: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "delayValue")
    )
    disable: Union[Default[bool], Global[bool], Variable] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "disable")
    )
    hostname: Optional[Union[Global[str], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "hostname")
    )
    interleave: Union[Default[bool], Global[bool], Variable] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "interleave")
    )
    ip_directed_broadcast: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "ipDirectedBroadcast")
    )
    ipv4_acl_egress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv4AclEgress"))
    ipv4_acl_ingress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv4AclIngress"))
    ipv6_acl_egress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv6AclEgress"))
    ipv6_acl_ingress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv6AclIngress"))
    mask_ipv4: Optional[Union[Global[SubnetMask], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "maskIpv4")
    )
    mtu: Union[Global[int], Default[int], Variable] = Field(
        default=Default[int](value=1500), validation_alias=AliasPath("data", "mtu")
    )
    nim_list: Optional[List[MultilinkNimList]] = Field(default=None, validation_alias=AliasPath("data", "nimList"))
    password: Optional[Union[Global[str], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "password")
    )
    ppp_auth_password: Optional[Union[Global[str], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "pppAuthPassword")
    )
    shaping_rate: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "shapingRate")
    )
    shutdown: Union[Default[bool], Global[bool], Variable] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "shutdown")
    )
    tcp_mss_adjust: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "tcpMssAdjust")
    )
    tloc_extension: Optional[Union[Global[str], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "tlocExtension")
    )
    username_string: Optional[Union[Global[str], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "usernameString")
    )
