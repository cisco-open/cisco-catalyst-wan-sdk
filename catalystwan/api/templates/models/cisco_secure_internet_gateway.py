# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

DEFAULT_TRACKER_THRESHOLD = 300
DEFAULT_TRACKER_INTERVAL = 60
DEFAULT_TRACKER_MULTIPLIER = 3
DEFAULT_INTERFACE_MTU = 1400
DEFAULT_INTERFACE_DPD_INTERVAL = 10
DEFAULT_INTERFACE_DPD_RETRIES = 3
DEFAULT_INTERFACE_IKE_VERSION = 2
DEFAULT_INTERFACE_IKE_REKEY_INTERVAL = 14400
DEFAULT_INTERFACE_IPSEC_REKEY_INTERVAL = 3600
DEFAULT_INTERFACE_IPSEC_REPLAY_WINDOW = 512
DEFAULT_INTERFACE_PAIR_ACTIVE_INTERFACE_WEIGHT = 1
DEFAULT_INTERFACE_PAIR_BACKUP_INTERFACE_WEIGHT = 1
DEFAULT_SIG_VPN_ID = 0
DEFAULT_SERVICE_IDLE_TIME = 0
DEFAULT_SERVICE_REFRESH_TIME = 0


class Application(str, Enum):
    SIG = "sig"


class TunnelSet(str, Enum):
    SECURE_INTERNET_GATEWAY_UMBRELLA = "secure-internet-gateway-umbrella"
    SECURE_INTERNET_GATEWAY_ZSCALER = "secure-internet-gateway-zscaler"


class TunnelDcPreference(str, Enum):
    PRIMARY_DC = "primary-dc"
    SECONDARY_DC = "secondary-dc"


class IkeCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA2 = "aes256-cbc-sha2"
    AES128_CBC_SHA1 = "aes128-cbc-sha1"
    AES128_CBC_SHA2 = "aes128-cbc-sha2"


class IkeGroup(str, Enum):
    TWO = "2"
    FOURTEEN = "14"
    FIFTEEN = "15"
    SIXTEEN = "16"


class IpsecCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA384 = "aes256-cbc-sha384"
    AES256_CBC_SHA256 = "aes256-cbc-sha256"
    AES256_CBC_SHA512 = "aes256-cbc-sha512"
    AES256_GCM = "aes256-gcm"
    NULL_SHA1 = "null-sha1"
    NULL_SHA384 = "null-sha384"
    NULL_SHA256 = "null-sha256"
    NULL_SHA512 = "null-sha512"


class PerfectForwardSecrecy(str, Enum):
    GROUP_2 = "group-2"
    GROUP_14 = "group-14"
    GROUP_15 = "group-15"
    GROUP_16 = "group-16"
    NONE = "none"


class Interface(FeatureTemplateValidator):
    if_name: str = Field(
        ...,  # Ellipsis indicates a required field
        json_schema_extra={"vmanage_key": "if-name"},
        description="Name of the interface.",
    )
    auto: bool = Field(..., description="Flag to indicate if the interface should be automatically configured.")
    shutdown: bool = Field(..., description="Flag to indicate if the interface is administratively down (shutdown).")
    description: Optional[str] = Field(default=None, description="Description for the interface.")
    unnumbered: bool = Field(default=True, description="Flag to indicate if the interface should be unnumbered.")
    address: Optional[ipaddress.IPv4Interface] = Field(
        default=None, description="IPv4 address and subnet mask for the interface."
    )
    tunnel_source: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tunnel-source"},
        description="IPv4 address used as the source of the tunnel.",
    )
    tunnel_source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tunnel-source-interface"},
        description="Interface name used as the source of the tunnel.",
    )
    tunnel_route_via: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tunnel-route-via"},
        description="The route via which tunnel traffic should be sent.",
    )
    tunnel_destination: str = Field(
        ...,
        json_schema_extra={"vmanage_key": "tunnel-destination"},
        description="The destination address for the tunnel.",
    )
    application: Application = Field(
        default=Application.SIG, description="Application type for the Secure Internet Gateway."
    )
    tunnel_set: TunnelSet = Field(
        default=TunnelSet.SECURE_INTERNET_GATEWAY_UMBRELLA,
        json_schema_extra={"vmanage_key": "tunnel-set"},
        description="Tunnel set used for the Secure Internet Gateway.",
    )
    tunnel_dc_preference: TunnelDcPreference = Field(
        default=TunnelDcPreference.PRIMARY_DC,
        json_schema_extra={"vmanage_key": "tunnel-dc-preference"},
        description="Data center preference for the tunnel.",
    )
    tcp_mss_adjust: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tcp-mss-adjust"},
        description="TCP Maximum Segment Size (MSS) adjust value.",
    )
    mtu: int = Field(
        default=DEFAULT_INTERFACE_MTU, description="MTU (Maximum Transmission Unit) size for the interface."
    )
    dpd_interval: Optional[int] = Field(
        default=DEFAULT_INTERFACE_DPD_INTERVAL,
        json_schema_extra={"vmanage_key": "dpd-interval"},
        description="Dead Peer Detection (DPD) interval in seconds.",
    )
    dpd_retries: Optional[int] = Field(
        default=DEFAULT_INTERFACE_DPD_RETRIES,
        json_schema_extra={"vmanage_key": "dpd-retries"},
        description="Number of retries for Dead Peer Detection (DPD).",
    )
    ike_version: int = Field(
        default=DEFAULT_INTERFACE_IKE_VERSION,
        json_schema_extra={"vmanage_key": "ike-version"},
        description="Internet Key Exchange (IKE) protocol version.",
    )
    pre_shared_secret: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "pre-shared-secret"},
        description="Pre-shared secret key for IKE authentication.",
    )
    ike_rekey_interval: Optional[int] = Field(
        default=DEFAULT_INTERFACE_IKE_REKEY_INTERVAL,
        json_schema_extra={"vmanage_key": "ike-rekey-interval"},
        description="Interval for rekeying the IKE security association.",
    )
    ike_ciphersuite: Optional[IkeCiphersuite] = Field(
        default=IkeCiphersuite.AES256_CBC_SHA1,
        json_schema_extra={"vmanage_key": "ike-ciphersuite"},
        description="Ciphersuite for IKE security association establishment.",
    )
    ike_group: IkeGroup = Field(
        default=IkeGroup.FOURTEEN,
        json_schema_extra={"vmanage_key": "ike-group"},
        description="Diffie-Hellman group used for IKE key exchange.",
    )
    pre_shared_key_dynamic: bool = Field(
        default=True,
        json_schema_extra={"vmanage_key": "pre-shared-key-dynamic"},
        description="Flag indicating if the pre-shared key is dynamic.",
    )
    ike_local_id: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ike-local-id"},
        description="Local identifier for IKE authentication.",
    )
    ike_remote_id: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ike-remote-id"},
        description="Remote identifier for IKE authentication.",
    )
    ipsec_rekey_interval: Optional[int] = Field(
        default=DEFAULT_INTERFACE_IPSEC_REKEY_INTERVAL,
        json_schema_extra={"vmanage_key": "ipsec-rekey-interval"},
        description="Interval for rekeying the IPsec security association.",
    )
    ipsec_replay_window: Optional[int] = Field(
        default=DEFAULT_INTERFACE_IPSEC_REPLAY_WINDOW,
        json_schema_extra={"vmanage_key": "ipsec-replay-window"},
        description="Replay window size for IPsec security association.",
    )
    ipsec_ciphersuite: IpsecCiphersuite = Field(
        default=IpsecCiphersuite.AES256_GCM,
        json_schema_extra={"vmanage_key": "ipsec-ciphersuite"},
        description="Ciphersuite for IPsec security association establishment.",
    )
    perfect_forward_secrecy: PerfectForwardSecrecy = Field(
        default=PerfectForwardSecrecy.NONE,
        json_schema_extra={"vmanage_key": "perfect-forward-secrecy"},
        description="Perfect Forward Secrecy (PFS) setting for IPsec key exchange.",
    )
    tracker: Optional[bool] = Field(default=None, description="Flag indicating if interface tracking is enabled.")
    track_enable: Optional[bool] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "track-enable"},
        description="Flag indicating if tracking is enabled for the interface.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class SvcType(str, Enum):
    SIG = "sig"


class InterfacePair(FeatureTemplateValidator):
    active_interface: str = Field(
        ..., json_schema_extra={"vmanage_key": "active-interface"}, description="Name of the active interface."
    )
    active_interface_weight: int = Field(
        default=DEFAULT_INTERFACE_PAIR_ACTIVE_INTERFACE_WEIGHT,
        json_schema_extra={"vmanage_key": "active-interface-weight"},
        description="Weighting factor for the active interface, used in failover decisions.",
    )
    backup_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "backup-interface"},
        description="Name of the backup interface. Can be 'None' if no backup interface is defined.",
    )
    backup_interface_weight: int = Field(
        default=DEFAULT_INTERFACE_PAIR_BACKUP_INTERFACE_WEIGHT,
        json_schema_extra={"vmanage_key": "backup-interface-weight"},
        description="Weighting factor for the backup interface, used in failover decisions.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class DisplayTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class RefreshTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class Service(FeatureTemplateValidator):
    svc_type: SvcType = Field(
        default=SvcType.SIG, json_schema_extra={"vmanage_key": "svc-type"}, description="Type of service configured."
    )
    interface_pair: List[InterfacePair] = Field(
        ...,
        json_schema_extra={"data_path": ["ha-pairs"], "vmanage_key": "interface-pair"},
        description="List of high-availability interface pairs.",
    )
    auth_required: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "auth-required"},
        description="Flag indicating if authentication is required for the service.",
    )
    xff_forward_enabled: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "xff-forward-enabled"},
        description="Flag indicating if X-Forwarded-For HTTP header is enabled.",
    )
    ofw_enabled: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "ofw-enabled"},
        description="Flag indicating if on-premise firewall is enabled.",
    )
    ips_control: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "ips-control"},
        description="Flag indicating if Intrusion Prevention System (IPS) control is enabled.",
    )
    caution_enabled: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "caution-enabled"},
        description="Flag indicating if caution warnings are enabled.",
    )
    primary_data_center: Optional[str] = Field(
        default="Auto",
        json_schema_extra={"vmanage_key": "primary-data-center"},
        description="Primary data center for the service. 'Auto' for automatic selection.",
    )
    secondary_data_center: Optional[str] = Field(
        default="Auto",
        json_schema_extra={"vmanage_key": "secondary-data-center"},
        description="Secondary data center for the service. 'Auto' for automatic selection.",
    )
    ip: Optional[bool] = Field(
        default=None, description="Flag indicating if IP filtering or processing is enabled for the service."
    )
    idle_time: Optional[int] = Field(
        default=DEFAULT_SERVICE_IDLE_TIME,
        json_schema_extra={"vmanage_key": "idle-time"},
        description="Idle time before a session is considered inactive.",
    )

    display_time_unit: Optional[DisplayTimeUnit] = Field(
        default=DisplayTimeUnit.MINUTE,
        json_schema_extra={"vmanage_key": "display-time-unit"},
        description="Unit of time used for displaying time-related settings.",
    )
    ip_enforced_for_known_browsers: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "ip-enforced-for-known-browsers"},
        description="Flag indicating if IP is enforced for known browsers.",
    )
    refresh_time: Optional[int] = Field(
        default=DEFAULT_SERVICE_REFRESH_TIME,
        json_schema_extra={"vmanage_key": "refresh-time"},
        description="Time after which the service information is refreshed.",
    )
    refresh_time_unit: Optional[RefreshTimeUnit] = Field(
        default=RefreshTimeUnit.MINUTE,
        json_schema_extra={"vmanage_key": "refresh-time-unit"},
        description="Unit of time used for the refresh time setting.",
    )
    enabled: Optional[bool] = Field(default=None, description="Flag indicating if the service is enabled.")
    block_internet_until_accepted: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "block-internet-until-accepted"},
        description="Flag indicating if Internet access is blocked until the service is accepted.",
    )
    force_ssl_inspection: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "force-ssl-inspection"},
        description="Flag indicating if SSL inspection is forced.",
    )
    timeout: Optional[int] = Field(
        default=None, description="Timeout value for the service, after which the session is considered inactive."
    )
    data_center_primary: Optional[str] = Field(
        default="Auto",
        json_schema_extra={"vmanage_key": "data-center-primary"},
        description="Alias for the primary data center setting.",
    )
    data_center_secondary: Optional[str] = Field(
        default="Auto",
        json_schema_extra={"vmanage_key": "data-center-secondary"},
        description=(
            "Secondary data center for the service. 'Auto' for automatic selection "
            "or a specific identifier for a manual selection."
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class TrackerType(str, Enum):
    SIG = "SIG"


class Tracker(FeatureTemplateValidator):
    name: str = Field(..., description="Name of the tracker.")
    endpoint_api_url: str = Field(
        ...,
        json_schema_extra={"vmanage_key": "endpoint-api-url"},
        description="URL of the endpoint API used by the tracker for health checks.",
    )
    threshold: Optional[int] = Field(
        default=DEFAULT_TRACKER_THRESHOLD, description="Threshold value for the tracker to trigger an alert or action."
    )
    interval: Optional[int] = Field(
        default=DEFAULT_TRACKER_INTERVAL, description="Interval at which the tracker performs health checks."
    )
    multiplier: Optional[int] = Field(
        default=DEFAULT_TRACKER_MULTIPLIER,
        description="Multiplier value used by the tracker to escalate repeated failures.",
    )
    tracker_type: TrackerType = Field(
        ..., json_schema_extra={"vmanage_key": "tracker-type"}, description="Type of tracker used for monitoring."
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class CiscoSecureInternetGatewayModel(FeatureTemplate):
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco Secure Internet Gateway feature template configuration"

    vpn_id: int = Field(
        default=DEFAULT_SIG_VPN_ID,
        json_schema_extra={"vmanage_key": "vpn-id"},
        description="VPN ID associated with the Cisco Secure Internet Gateway service.",
    )
    interface: List[Interface] = Field(..., description="List of interface configurations associated with the service.")
    service: List[Service] = Field(
        ..., description="List of service configurations for the Cisco Secure Internet Gateway."
    )
    tracker_src_ip: Optional[ipaddress.IPv4Interface] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tracker-src-ip"},
        description="Source IP address used by the tracker for sending health check packets.",
    )
    tracker: Optional[List[Tracker]] = Field(
        default=None,
        description="List of trackers for monitoring the health of the Cisco Secure Internet Gateway service.",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_secure_internet_gateway"
