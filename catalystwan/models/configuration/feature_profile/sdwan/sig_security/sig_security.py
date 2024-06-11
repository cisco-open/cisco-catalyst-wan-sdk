from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.common import IkeCiphersuite

SigProvider = Literal["Umbrella", "Zscaler", "Generic"]
Application = Literal["sig"]
TunnelSet = Literal[
    "secure-internet-gateway-umbrella", "secure-internet-gateway-zscaler", "secure-internet-gateway-other"
]
TunnelDcPreference = Literal["primary-dc", "secondary-dc"]
IkeGroup = Literal["2", "5", "14", "15", "16", "19", "20", "21"]
IpsecReplayWindow = Literal[64, 128, 256, 512, 1024]
IpsecCiphersuite = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha384", "aes256-cbc-sha256", "aes256-cbc-sha512", "aes256-gcm"
]
PerfectForwardSecrecy = Literal[
    "group-2", "group-5", "group-14", "group-15", "group-16", "group-19", "group-20", "group-21", "none"
]
TrackerType = Literal["SIG"]
TimeUnit = Literal["MINUTE", "HOUR", "DAY"]


class InterfaceMetadataSharing(BaseModel):
    src_vpn: Union[Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="srcVpn",
        validation_alias="srcVpn",
        description="Share Source VPN",
    )


class Interface(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    if_name: Global[str] = Field(
        serialization_alias="ifName", validation_alias="ifName", description="Interface name: IPsec when present"
    )
    auto: Optional[Global[bool]] = Field(default=None, description="Auto Tunnel Mode")
    shutdown: Union[Global[bool], Default[bool]] = Field(default=as_default(False), description="Administrative state")
    description: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, description="Interface description"
    )
    unnumbered: Optional[Global[bool]] = Field(default=None, description="Unnumbered interface")
    address: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, description="Assign IPv4 address"
    )
    tunnel_source: Optional[Union[Global[str], Variable]] = Field(
        default=None,
        serialization_alias="tunnelSource",
        validation_alias="tunnelSource",
        description="Tunnel source IP Address",
    )
    tunnel_source_interface: Union[Global[str], Variable] = Field(
        serialization_alias="tunnelSourceInterface",
        validation_alias="tunnelSourceInterface",
        description="<1..32 characters> Interface name: ge0/<0-..> or ge0/<0-..>.vlanid",
    )
    tunnel_route_via: Optional[Union[Global[str], Variable]] = Field(
        default=None,
        serialization_alias="tunnelRouteVia",
        validation_alias="tunnelRouteVia",
        description="<1..32 characters> Interface name: ge0/<0-..> or ge0/<0-..>.vlanid",
    )
    tunnel_destination: Optional[Union[Global[str], Variable]] = Field(
        default=None,
        serialization_alias="tunnelDestination",
        validation_alias="tunnelDestination",
        description="Tunnel destination IP address",
    )
    application: Optional[Union[Global[Application], Default[Application]]] = Field(
        default=None, description="Enable Application Tunnel Type"
    )
    tunnel_set: Optional[Union[Global[TunnelSet], Default[TunnelSet]]] = Field(
        default=None, serialization_alias="tunnelSet", validation_alias="tunnelSet", description="SIG Tunnel Provider"
    )
    tunnel_dc_preference: Optional[Union[Global[TunnelDcPreference], Default[TunnelDcPreference]]] = Field(
        default=None,
        serialization_alias="tunnelDcPreference",
        validation_alias="tunnelDcPreference",
        description="SIG Tunnel Data Center",
    )
    tcp_mss_adjust: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="tcpMssAdjust",
        validation_alias="tcpMssAdjust",
        description="TCP MSS on SYN packets, in bytes",
    )
    mtu: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(1400), description="Interface MTU <576..2000>, in bytes"
    )
    dpd_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="dpdInterval",
        validation_alias="dpdInterval",
        description="IKE keepalive interval (seconds)",
    )
    dpd_retries: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="dpdRetries",
        validation_alias="dpdRetries",
        description="IKE keepalive retries",
    )
    ike_version: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, serialization_alias="ikeVersion", validation_alias="ikeVersion", description="IKE Version <1..2>"
    )
    pre_shared_secret: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="preSharedSecret",
        validation_alias="preSharedSecret",
        description="Use preshared key to authenticate IKE peer",
    )
    ike_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="ikeRekeyInterval",
        validation_alias="ikeRekeyInterval",
        description="IKE rekey interval <300..1209600> seconds",
    )
    ike_ciphersuite: Optional[Union[Global[IkeCiphersuite], Variable, Default[IkeCiphersuite]]] = Field(
        default=None,
        serialization_alias="ikeCiphersuite",
        validation_alias="ikeCiphersuite",
        description="IKE identity the IKE preshared secret belongs to",
    )
    ike_group: Optional[Union[Global[IkeGroup], Variable, Default[IkeGroup]]] = Field(
        default=None,
        serialization_alias="ikeGroup",
        validation_alias="ikeGroup",
        description="IKE Diffie Hellman Groups",
    )
    pre_shared_key_dynamic: Optional[Global[bool]] = Field(
        default=None,
        serialization_alias="preSharedKeyDynamic",
        validation_alias="preSharedKeyDynamic",
        description="Use preshared key to authenticate IKE peer",
    )
    ike_local_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="ikeLocalId",
        validation_alias="ikeLocalId",
        description="IKE ID for the local endpoint. Input IPv4 address, domain name, or email address",
    )
    ike_remote_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="ikeRemoteId",
        validation_alias="ikeRemoteId",
        description="IKE ID for the remote endpoint. Input IPv4 address, domain name, or email address",
    )
    ipsec_rekey_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="ipsecRekeyInterval",
        validation_alias="ipsecRekeyInterval",
        description="IPsec rekey interval <300..1209600> seconds",
    )
    ipsec_replay_window: Optional[Union[Global[IpsecReplayWindow], Variable, Default[IpsecReplayWindow]]] = Field(
        default=None,
        serialization_alias="ipsecReplayWindow",
        validation_alias="ipsecReplayWindow",
        description="Replay window size 32..8192 (must be a power of 2)",
    )
    ipsec_ciphersuite: Optional[Union[Global[IpsecCiphersuite], Variable, Default[IpsecCiphersuite]]] = Field(
        default=None,
        serialization_alias="ipsecCiphersuite",
        validation_alias="ipsecCiphersuite",
        description="IPsec(ESP) encryption and integrity protocol",
    )
    perfect_forward_secrecy: Optional[
        Union[Global[PerfectForwardSecrecy], Variable, Default[PerfectForwardSecrecy]]
    ] = Field(
        default=None,
        serialization_alias="perfectForwardSecrecy",
        validation_alias="perfectForwardSecrecy",
        description="IPsec perfect forward secrecy settings",
    )
    tracker: Optional[Union[Global[str], Default[None]]] = Field(
        default=None, description="Enable tracker for this interface"
    )
    track_enable: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="trackEnable",
        validation_alias="trackEnable",
        description="Enable/disable SIG tracking",
    )
    tunnel_public_ip: Optional[Union[Global[str], Variable, Default[str]]] = Field(
        default=None,
        serialization_alias="tunnelPublicIp",
        validation_alias="tunnelPublicIp",
        description="Public IP required to setup GRE tunnel to Zscaler",
    )


class InterfacePair(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    active_interface: Global[str] = Field(
        serialization_alias="activeInterface",
        validation_alias="activeInterface",
        description="Active Tunnel Interface for SIG",
    )
    active_interface_weight: Union[Global[int], Default[int]] = Field(
        default=as_default(1),
        serialization_alias="activeInterfaceWeight",
        validation_alias="activeInterfaceWeight",
        description="Active Tunnel Interface Weight",
    )
    backup_interface: Global[str] = Field(
        serialization_alias="backupInterface",
        validation_alias="backupInterface",
        description="Backup Tunnel Interface for SIG",
    )
    backup_interface_weight: Union[Global[int], Default[int]] = Field(
        default=as_default(1),
        serialization_alias="backupInterfaceWeight",
        validation_alias="backupInterfaceWeight",
        description="Backup Tunnel Interface Weight",
    )


class Service(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    interface_pair: List[InterfacePair] = Field(
        serialization_alias="interfacePair",
        validation_alias="interfacePair",
        description="Interface Pair for active and backup",
    )
    auth_required: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="authRequired",
        validation_alias="authRequired",
        description="Enforce Authentication",
    )
    xff_forward_enabled: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="xffForwardEnabled",
        validation_alias="xffForwardEnabled",
        description="XFF forwarding enabled",
    )
    ofw_enabled: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, serialization_alias="ofwEnabled", validation_alias="ofwEnabled", description="Firewall enabled"
    )
    ips_control: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, serialization_alias="ipsControl", validation_alias="ipsControl", description="Enable IPS Control"
    )
    caution_enabled: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="cautionEnabled",
        validation_alias="cautionEnabled",
        description="Enable Caution",
    )
    primary_data_center: Optional[Union[Global[str], Default[str], Variable]] = Field(
        default=None,
        serialization_alias="primaryDataCenter",
        validation_alias="primaryDataCenter",
        description="Custom Primary Datacenter",
    )
    secondary_data_center: Optional[Union[Global[str], Default[str], Variable]] = Field(
        default=None,
        serialization_alias="secondaryDataCenter",
        validation_alias="secondaryDataCenter",
        description="Custom Secondary Datacenter",
    )
    ip: Optional[Union[Global[bool], Default[bool]]] = Field(default=None, description="Enable Surrogate IP")
    idle_time: Optional[Union[Global[int], Default[int]]] = Field(
        default=None,
        serialization_alias="idleTime",
        validation_alias="idleTime",
        description="Idle time to disassociation",
    )
    display_time_unit: Optional[Union[Global[TimeUnit], Default[TimeUnit]]] = Field(
        default=None,
        serialization_alias="displayTimeUnit",
        validation_alias="displayTimeUnit",
        description="Display time unit",
    )
    ip_enforced_for_known_browsers: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="ipEnforcedForKnownBrowsers",
        validation_alias="ipEnforcedForKnownBrowsers",
        description="Enforce Surrogate IP for known browsers",
    )
    refresh_time: Optional[Union[Global[int], Default[int]]] = Field(
        default=None,
        serialization_alias="refreshTime",
        validation_alias="refreshTime",
        description="Refresh time for re-validation of surrogacy in minutes",
    )
    refresh_time_unit: Optional[Union[Global[TimeUnit], Default[TimeUnit]]] = Field(
        default=None,
        serialization_alias="refreshTimeUnit",
        validation_alias="refreshTimeUnit",
        description="Refresh Time unit",
    )
    enabled: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, description="Enable Acceptable User Policy"
    )
    block_internet_until_accepted: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="blockInternetUntilAccepted",
        validation_alias="blockInternetUntilAccepted",
        description="For first-time Acceptable User Policy behavior, block Internet access",
    )
    force_ssl_inspection: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="forceSslInspection",
        validation_alias="forceSslInspection",
        description="For first-time Acceptable User Policy behavior, force SSL inspection",
    )
    timeout: Optional[Union[Global[int], Default[int]]] = Field(
        default=None, description="Custom Acceptable User Policy frequency in days"
    )
    location_name: Optional[Union[Default[str], Variable]] = Field(
        default=None,
        serialization_alias="locationName",
        validation_alias="locationName",
        description="Zscaler location name (optional)",
    )
    data_center_primary: Optional[Union[Global[str], Default[str], Variable]] = Field(
        default=None,
        serialization_alias="dataCenterPrimary",
        validation_alias="dataCenterPrimary",
        description="Umbrella Primary Datacenter",
    )
    data_center_secondary: Optional[Union[Global[str], Default[str], Variable]] = Field(
        default=None,
        serialization_alias="dataCenterSecondary",
        validation_alias="dataCenterSecondary",
        description="Umbrella Secondary Datacenter",
    )


class Tracker(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    name: Global[str] = Field(description="Tracker name")
    endpoint_api_url: Union[Global[str], Variable] = Field(
        serialization_alias="endpointApiUrl", validation_alias="endpointApiUrl", description="API url of endpoint"
    )
    threshold: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(300), description="Probe Timeout threshold <100..1000> milliseconds"
    )
    interval: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(60), description="Probe interval <10..600> seconds"
    )
    multiplier: Union[Global[int], Variable, Default[int]] = Field(
        default=as_default(3), description="Probe failure multiplier <1..10> failed attempts"
    )
    tracker_type: Union[Global[TrackerType], Default[TrackerType]] = Field(
        default=as_default("SIG", TrackerType),
        serialization_alias="trackerType",
        validation_alias="trackerType",
        description="tracker type",
    )


class SIGParcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    type_: Literal["sig"] = Field(default="sig", exclude=True)

    sig_provider: Union[Global[SigProvider], Default[SigProvider]] = Field(
        default=as_default("Umbrella", SigProvider),
        validation_alias=AliasPath("data", "sigProvider"),
        description="SIG Provider",
    )
    interface_metadata_sharing: Optional[InterfaceMetadataSharing] = Field(
        default=None, validation_alias=AliasPath("data", "interfaceMetadataSharing")
    )
    interface: List[Interface] = Field(
        validation_alias=AliasPath("data", "interface"), description="Interface name: IPsec when present"
    )
    service: Service = Field(validation_alias=AliasPath("data", "service"))
    tracker_src_ip: Union[Global[IPv4Address], Variable, None] = Field(
        default=None, validation_alias=AliasPath("data", "trackerSrcIp"), description="Source IP address for Tracker"
    )
    tracker: List[Tracker] = Field(validation_alias=AliasPath("data", "tracker"))
