# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Network
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, ValidationError, model_validator
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, as_global
from catalystwan.models.configuration.feature_profile.common import RefIdItem, RefIdList

DefaultAction = Literal["pass", "drop"]
BaseAction = Literal["pass", "inspect", "drop"]
SequenceType = Literal["ngfirewall"]
AipActionType = Literal["advancedInspectionProfile"]
SequenceActionType = Literal["log", "connectionEvents"]
GeoLocation = Literal[
    "AF",
    "AN",
    "AS",
    "EU",
    "NA",
    "OC",
    "SA",
    "AFG",
    "ALB",
    "ATA",
    "DZA",
    "ASM",
    "AND",
    "AGO",
    "ATG",
    "AZE",
    "ARG",
    "AUS",
    "AUT",
    "BHS",
    "BHR",
    "BGD",
    "ARM",
    "BRB",
    "BEL",
    "BMU",
    "BTN",
    "BOL",
    "BIH",
    "BWA",
    "BVT",
    "BRA",
    "BLZ",
    "IOT",
    "SLB",
    "VGB",
    "BRN",
    "BGR",
    "MMR",
    "BDI",
    "BLR",
    "KHM",
    "CMR",
    "CAN",
    "CPV",
    "CYM",
    "CAF",
    "LKA",
    "TCD",
    "CHL",
    "CHN",
    "TWN",
    "CXR",
    "CCK",
    "COL",
    "COM",
    "MYT",
    "COG",
    "COD",
    "COK",
    "CRI",
    "HRV",
    "CUB",
    "CYP",
    "CZE",
    "BEN",
    "DNK",
    "DMA",
    "DOM",
    "ECU",
    "SLV",
    "GNQ",
    "ETH",
    "ERI",
    "EST",
    "FRO",
    "FLK",
    "SGS",
    "FJI",
    "FIN",
    "ALA",
    "FRA",
    "GUF",
    "PYF",
    "ATF",
    "DJI",
    "GAB",
    "GEO",
    "GMB",
    "PSE",
    "DEU",
    "GHA",
    "GIB",
    "KIR",
    "GRC",
    "GRL",
    "GRD",
    "GLP",
    "GUM",
    "GTM",
    "GIN",
    "GUY",
    "HTI",
    "HMD",
    "VAT",
    "HND",
    "HKG",
    "HUN",
    "ISL",
    "IND",
    "IDN",
    "IRN",
    "IRQ",
    "IRL",
    "ISR",
    "ITA",
    "CIV",
    "JAM",
    "JPN",
    "KAZ",
    "JOR",
    "KEN",
    "PRK",
    "KOR",
    "KWT",
    "KGZ",
    "LAO",
    "LBN",
    "LSO",
    "LVA",
    "LBR",
    "LBY",
    "LIE",
    "LTU",
    "LUX",
    "MAC",
    "MDG",
    "MWI",
    "MYS",
    "MDV",
    "MLI",
    "MLT",
    "MTQ",
    "MRT",
    "MUS",
    "MEX",
    "MCO",
    "MNG",
    "MDA",
    "MNE",
    "MSR",
    "MAR",
    "MOZ",
    "OMN",
    "NAM",
    "NRU",
    "NPL",
    "NLD",
    "ANT",
    "CUW",
    "ABW",
    "SXM",
    "BES",
    "NCL",
    "VUT",
    "NZL",
    "NIC",
    "NER",
    "NGA",
    "NIU",
    "NFK",
    "NOR",
    "MNP",
    "UMI",
    "FSM",
    "MHL",
    "PLW",
    "PAK",
    "PAN",
    "PNG",
    "PRY",
    "PER",
    "PHL",
    "PCN",
    "POL",
    "PRT",
    "GNB",
    "TLS",
    "PRI",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "BLM",
    "SHN",
    "KNA",
    "AIA",
    "LCA",
    "MAF",
    "SPM",
    "VCT",
    "SMR",
    "STP",
    "SAU",
    "SEN",
    "SRB",
    "SYC",
    "SLE",
    "SGP",
    "SVK",
    "VNM",
    "SVN",
    "SOM",
    "ZAF",
    "ZWE",
    "ESP",
    "SSD",
    "ESH",
    "SDN",
    "SUR",
    "SJM",
    "SWZ",
    "SWE",
    "CHE",
    "SYR",
    "TJK",
    "THA",
    "TGO",
    "TKL",
    "TON",
    "TTO",
    "ARE",
    "TUN",
    "TUR",
    "TKM",
    "TCA",
    "TUV",
    "UGA",
    "UKR",
    "MKD",
    "EGY",
    "GBR",
    "GGY",
    "JEY",
    "IMN",
    "TZA",
    "USA",
    "VIR",
    "BFA",
    "URY",
    "UZB",
    "VEN",
    "WLF",
    "WSM",
    "YEM",
    "ZMB",
]
ProtocolName = Literal[
    "snmp",
    "icmp",
    "tcp",
    "udp",
    "echo",
    "telnet",
    "wins",
    "n2h2server",
    "nntp",
    "pptp",
    "rtsp",
    "bootpc",
    "gdoi",
    "tacacs",
    "gopher",
    "icabrowser",
    "skinny",
    "sunrpc",
    "biff",
    "router",
    "ircs",
    "orasrv",
    "ms-cluster-net",
    "kermit",
    "isakmp",
    "sshell",
    "realsecure",
    "ircu",
    "appleqtc",
    "pwdgen",
    "rdb-dbs-disp",
    "creativepartnr",
    "finger",
    "ftps",
    "giop",
    "rsvd",
    "hp-alarm-mgr",
    "uucp",
    "kerberos",
    "imap",
    "time",
    "bootps",
    "tftp",
    "oracle",
    "snmptrap",
    "http",
    "qmtp",
    "radius",
    "oracle-em-vp",
    "tarantella",
    "pcanywheredata",
    "ldap",
    "mgcp",
    "sqlsrv",
    "hsrp",
    "cisco-net-mgmt",
    "smtp",
    "pcanywherestat",
    "exec",
    "send",
    "stun",
    "syslog",
    "ms-sql-m",
    "citrix",
    "creativeserver",
    "cifs",
    "cisco-sys",
    "cisco-tna",
    "ms-dotnetster",
    "gtpv1",
    "gtpv0",
    "imap3",
    "fcip-port",
    "netbios-dgm",
    "sip-tls",
    "pop3s",
    "cisco-fna",
    "802-11-iapp",
    "oem-agent",
    "cisco-tdp",
    "tr-rsrb",
    "r-winsock",
    "sql-net",
    "syslog-conn",
    "tacacs-ds",
    "h225ras",
    "ace-svr",
    "dhcp-failover",
    "igmpv3lite",
    "irc-serv",
    "entrust-svcs",
    "dbcontrol_agent",
    "cisco-svcs",
    "ipsec-msft",
    "microsoft-ds",
    "ms-sna",
    "rsvp_tunnel",
    "rsvp-encap",
    "hp-collector",
    "netbios-ns",
    "msexch-routing",
    "h323",
    "l2tp",
    "ldap-admin",
    "pop3",
    "h323callsigalt",
    "ms-sql",
    "iscsi-target",
    "webster",
    "lotusnote",
    "ipx",
    "entrust-svc-hand",
    "citriximaclient",
    "rtc-pm-port",
    "ftp",
    "aol",
    "xdmcp",
    "oraclenames",
    "login",
    "iscsi",
    "ttc",
    "imaps",
    "socks",
    "ssh",
    "dnsix",
    "daytime",
    "sip",
    "discard",
    "ntp",
    "ldaps",
    "https",
    "vdolive",
    "ica",
    "net8-cman",
    "cuseeme",
    "netstat",
    "sms",
    "streamworks",
    "rtelnet",
    "who",
    "kazaa",
    "ssp",
    "dbase",
    "timed",
    "cddbp",
    "telnets",
    "ymsgr",
    "ident",
    "bgp",
    "ddns-v3",
    "vqp",
    "irc",
    "ipass",
    "x11",
    "dns",
    "lotusmtap",
    "mysql",
    "nfs",
    "msnmsgr",
    "netshow",
    "sqlserv",
    "hp-managed-node",
    "ncp",
    "shell",
    "realmedia",
    "msrpc",
    "clp",
]


class Ipv4Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ipv4_value: Union[Global[List[IPv4Network]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )

    @classmethod
    def create_with_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(ipv4_value=as_global(ip_networks))

    @classmethod
    def create_with_variable(cls, variable_name: str) -> Self:
        return cls(ipv4_value=Variable(value=variable_name))


class FqdnMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    fqdn_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="fqdnValue", serialization_alias="fqdnValue"
    )

    @classmethod
    def from_domain_names(cls, domain_names: List[str]) -> Self:
        return cls(fqdn_value=as_global(domain_names))


class PortMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(port_value=as_global(ports))


class SourceDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_data_prefix_list: RefIdList = Field(
        validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )

    @classmethod
    def create(cls, source_data_prefix_list: List[UUID]) -> Self:
        return cls(source_data_prefix_list=RefIdList.from_uuids(uuids=source_data_prefix_list))


class DestinationDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_data_prefix_list: RefIdList = Field(
        validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_data_prefix_list=RefIdList.from_uuids(uuids=uuids))


class DestinationFqdnList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_fqdn_list: RefIdList = Field(
        validation_alias="destinationFqdnList", serialization_alias="destinationFqdnList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_fqdn_list=RefIdList.from_uuids(uuids=uuids))


class SourceGeoLocationList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_geo_location_list: RefIdList = Field(
        validation_alias="sourceGeoLocationList", serialization_alias="sourceGeoLocationList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_geo_location_list=RefIdList.from_uuids(uuids=uuids))


class DestinationGeoLocationList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_geo_location_list: RefIdList = Field(
        validation_alias="destinationGeoLocationList", serialization_alias="destinationGeoLocationList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_geo_location_list=RefIdList.from_uuids(uuids=uuids))


class SourcePortList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_port_list: RefIdList = Field(validation_alias="sourcePortList", serialization_alias="sourcePortList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_port_list=RefIdList.from_uuids(uuids=uuids))


class DestinationPortList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_port_list: RefIdList = Field(
        validation_alias="destinationPortList", serialization_alias="destinationPortList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_port_list=RefIdList.from_uuids(uuids))


class SourceScalableGroupTagList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_scalable_group_tag_list: RefIdList = Field(
        validation_alias="sourceScalableGroupTagList", serialization_alias="sourceScalableGroupTagList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_scalable_group_tag_list=RefIdList.from_uuids(uuids))


class DestinationScalableGroupTagList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_scalable_group_tag_list: RefIdList = Field(
        validation_alias="destinationScalableGroupTagList", serialization_alias="destinationScalableGroupTagList"
    )

    @classmethod  # from_uuids
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_scalable_group_tag_list=RefIdList.from_uuids(uuids))


class SourceIdentityList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_list: RefIdList = Field(
        validation_alias="sourceIdentityList", serialization_alias="sourceIdentityList"
    )


class ProtocolNameList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol_name_list: RefIdList = Field(validation_alias="protocolNameList", serialization_alias="protocolNameList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(protocol_name_list=RefIdList.from_uuids(uuids))


class AppList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_list: RefIdList = Field(validation_alias="appList", serialization_alias="appList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(app_list=RefIdList.from_uuids(uuids))


class AppListFlat(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_list_flat: RefIdList = Field(validation_alias="appListFlat", serialization_alias="appListFlat")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(app_list_flat=RefIdList.from_uuids(uuids))


class RuleSetList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    rule_set_list: RefIdList = Field(validation_alias="ruleSetList", serialization_alias="ruleSetList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(rule_set_list=RefIdList.from_uuids(uuids))


class SourceSecurityGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_security_group: RefIdList = Field(
        validation_alias="sourceSecurityGroup", serialization_alias="sourceSecurityGroup"
    )


class DestinationSecurityGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_security_group: RefIdList = Field(
        validation_alias="destinationSecurityGroup", serialization_alias="destinationSecurityGroup"
    )


class SourceIp(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_ip: Ipv4Match = Field(validation_alias="sourceIp", serialization_alias="sourceIp")

    @classmethod
    def from_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(source_ip=Ipv4Match.create_with_ip_networks(ip_networks))

    @classmethod
    def from_variable(cls, variable_name: str) -> Self:
        return cls(source_ip=Ipv4Match.create_with_variable(variable_name))


class DestinationIp(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_ip: Ipv4Match = Field(validation_alias="destinationIp", serialization_alias="destinationIp")

    @classmethod
    def from_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(destination_ip=Ipv4Match.create_with_ip_networks(ip_networks))

    @classmethod
    def from_variable(cls, variable_name: str) -> Self:
        return cls(destination_ip=Ipv4Match.create_with_variable(variable_name))


class DestinationFqdn(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_fqdn: FqdnMatch = Field(validation_alias="destinationFqdn", serialization_alias="destinationFqdn")

    @classmethod
    def from_domain_names(cls, domain_names: List[str]) -> Self:
        return cls(destination_fqdn=FqdnMatch.from_domain_names(domain_names))


class SourcePort(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_port: PortMatch = Field(validation_alias="sourcePort", serialization_alias="sourcePort")

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(source_port=PortMatch.from_str_list(ports))


class DestinationPort(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_port: PortMatch = Field(validation_alias="destinationPort", serialization_alias="destinationPort")

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(destination_port=PortMatch.from_str_list(ports))


class SourceGeoLocation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_geo_loacation: Union[Global[List[GeoLocation]], Variable] = Field(
        validation_alias="sourceGeoLocation", serialization_alias="sourceGeoLocation"
    )

    @classmethod
    def from_geo_locations_list(cls, locations: List[GeoLocation]) -> Self:
        return cls(source_geo_loacation=Global[List[GeoLocation]](value=locations))


class DestinationGeoLocation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_geo_loacation: Union[Global[List[GeoLocation]], Variable] = Field(
        validation_alias="destinationGeoLocation", serialization_alias="destinationGeoLocation"
    )

    @classmethod
    def from_geo_locations_list(cls, locations: List[GeoLocation]) -> Self:
        return cls(destination_geo_loacation=Global[List[GeoLocation]](value=locations))


class SourceIdentityUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_user: Global[List[str]] = Field(
        validation_alias="sourceIdentityUser", serialization_alias="sourceIdentityUser"
    )


class SourceIdentityUserGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_user_group: Global[List[str]] = Field(
        validation_alias="sourceIdentityUserGroup", serialization_alias="sourceIdentityUserGroup"
    )


class App(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app: Global[List[str]]


class AppFamily(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_family: Global[List[str]] = Field(validation_alias="appFamily", serialization_alias="appFamily")


class Protocol(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol: Global[List[str]]

    @classmethod
    def from_protocol_id_list(cls, ids: List[str]) -> Self:
        return cls(protocol=as_global(ids))


class ProtocolNameMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol_name: Global[List[ProtocolName]] = Field(
        validation_alias="protocolName", serialization_alias="protocolName"
    )

    @classmethod
    def from_protocol_name_list(cls, protocols: List[ProtocolName]) -> Self:
        return cls(protocol_name=Global[List[ProtocolName]](value=protocols))


MatchEntry = Union[
    SourceDataPrefixList,
    DestinationDataPrefixList,
    DestinationFqdnList,
    SourceGeoLocationList,
    DestinationGeoLocationList,
    SourcePortList,
    DestinationPortList,
    SourceScalableGroupTagList,
    DestinationScalableGroupTagList,
    SourceIdentityList,
    ProtocolNameList,
    AppList,
    AppListFlat,
    RuleSetList,
    SourceSecurityGroup,
    DestinationSecurityGroup,
    SourceIp,
    DestinationIp,
    DestinationFqdn,
    SourcePort,
    DestinationPort,
    SourceGeoLocation,
    DestinationGeoLocation,
    SourceIdentityUser,
    SourceIdentityUserGroup,
    App,
    AppFamily,
    Protocol,
    ProtocolNameMatch,
]


class AipAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type: Global[AipActionType] = Field(
        default=Global[AipActionType](value="advancedInspectionProfile"),
        validation_alias="type",
        serialization_alias="type",
    )
    parameter: RefIdItem

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(parameter=RefIdItem.from_uuid(uuid))


class LogAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type: Optional[Global[SequenceActionType]] = Field(default=None)
    parameter: Global[str] = Field(default=Global[str](value="true"))

    @classmethod
    def from_sequence_action(cls, action_type: SequenceActionType) -> Self:
        return cls(type=as_global(action_type, SequenceActionType))


class Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    entries: List[MatchEntry]

    @classmethod
    def create(cls, entries: Optional[List[MatchEntry]] = None) -> Self:
        return cls(entries=entries if entries else [])


class NgFirewallSequence(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    sequence_id: Global[str] = Field(validation_alias="sequenceId", serialization_alias="sequenceId")
    sequence_name: Global[str] = Field(validation_alias="sequenceName", serialization_alias="sequenceName")
    base_action: Global[BaseAction] = Field(
        default=Global[BaseAction](value="drop"), validation_alias="baseAction", serialization_alias="baseAction"
    )
    sequence_type: Global[SequenceType] = Field(
        default=Global[SequenceType](value="ngfirewall"),
        validation_alias="sequenceType",
        serialization_alias="sequenceType",
    )
    match: Match
    actions: List[Union[LogAction, AipAction]] = Field(
        default=[], validation_alias="actions", min_length=0, max_length=2, serialization_alias="actions"
    )
    disable_sequence: Global[bool] = Field(
        default=Global[bool](value=False),
        validation_alias="disableSequence",
        serialization_alias="disableSequence",
    )

    def add_log_action(self) -> None:
        self.actions.append(LogAction())

    def add_aip_action(self, aip_uuid: UUID) -> None:
        self.actions.append(AipAction.from_uuid(aip_uuid))

    @model_validator(mode="after")
    def validate_model(self):
        if len(self.actions) > len(set(map(type, self.actions))):
            raise ValidationError(
                f"NGFirewall sequence cannot contain actions with the same type. Sequence actions: {self.actions}"
            )

        return self

    @classmethod
    def create(
        cls,
        sequence_id: int,
        sequence_name: str,
        base_action: BaseAction,
        disable_sequence: bool = False,
        match: Optional[Match] = None,
        actions: Optional[List[Union[LogAction, AipAction]]] = None,
    ) -> Self:
        return cls(
            sequence_id=as_global(str(sequence_id)),
            sequence_name=as_global(sequence_name),
            base_action=as_global(base_action, BaseAction),
            match=match if match else Match.create(),
            actions=actions if actions else [],
            disable_sequence=as_global(disable_sequence),
        )


class NgfirewallParcel(_ParcelBase):
    type_: Literal["unified/ngfirewall"] = Field(default="unified/ngfirewall", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    default_action_type: Global[DefaultAction] = Field(validation_alias=AliasPath("data", "defaultActionType"))
    sequences: List[NgFirewallSequence] = Field(validation_alias=AliasPath("data", "sequences"))
    contains_tls: Optional[bool] = Field(
        default=False, validation_alias="containsTls", serialization_alias="containsTls"
    )
    contains_utd: Optional[bool] = Field(
        default=False, validation_alias="containsUtd", serialization_alias="containsUtd"
    )
    optimized: Optional[bool] = Field(default=True)

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        default_action_type: DefaultAction,
        sequences: List[NgFirewallSequence],
        contains_tls: bool = False,
        contains_utd: bool = False,
    ) -> Self:
        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            default_action_type=as_global(default_action_type, DefaultAction),
            sequences=sequences,
            contains_utd=contains_utd,
            contains_tls=contains_tls,
        )
