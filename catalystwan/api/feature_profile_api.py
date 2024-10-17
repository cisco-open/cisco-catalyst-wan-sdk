# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Protocol, Type, Union, overload
from uuid import UUID

from pydantic import Json

from catalystwan.endpoints.configuration.feature_profile.sdwan.cli import CliFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.other import OtherFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.sig_security import SIGSecurity
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.topology import TopologyFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.uc_voice import UcVoiceFeatureProfile
from catalystwan.exceptions import CatalystwanException, ManagerHTTPError
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import (
    AnyApplicationPriorityParcel,
    PolicySettingsParcel,
    QosPolicyParcel,
    TrafficPolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.as_path import AsPathParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.mirror import MirrorParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.sla_class import SLAClassParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.aip import (
    AdvancedInspectionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.amp import (
    AdvancedMalwareProtectionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.intrusion_prevention import (
    IntrusionPreventionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption import (
    SslDecryptionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption_profile import (
    SslDecryptionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url import URLParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing import (
    AnyRoutingParcel,
    RoutingBgpParcel,
    RoutingOspfParcel,
    RoutingOspfv3IPv4Parcel,
    RoutingOspfv3IPv6Parcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyServiceParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.eigrp import EigrpParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import (
    InterfaceEthernetParcel as LanInterfaceEthernetParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import (
    InterfaceGreParcel as LanInterfaceGreParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import (
    InterfaceIpsecParcel as LanInterfaceIpsecParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.multilink import (
    InterfaceMultilinkParcel as LanInterfaceMultilinkParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import MulticastParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.switchport import SwitchportParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import WirelessLanParcel
from catalystwan.models.configuration.feature_profile.sdwan.sig_security.sig_security import SIGParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology import AnyTopologyParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import AnyTransportParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.management.ethernet import (
    InterfaceEthernetParcel as ManagementInterfaceEthernetParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.t1e1controller import T1E1ControllerParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import ManagementVpnParcel, TransportVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    InterfaceCellularParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    InterfaceEthernetParcel as WanInterfaceEthernetParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.gre import (
    InterfaceGreParcel as WanInterfaceGreParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ipsec import (
    InterfaceIpsecParcel as WanInterfaceIpsecParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.multilink import (
    InterfaceMultilinkParcel as WanInterfaceMultilinkParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import T1E1SerialParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import AnyUcVoiceParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.dsp_farm import DspFarmParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.media_profile import MediaProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.trunk_group import TrunkGroupParcel
from catalystwan.typed_list import DataSequence

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.api.parcel_api import SDRoutingFullConfigParcelAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.application_priority import (
    ApplicationPriorityFeatureProfile,
)
from catalystwan.endpoints.configuration.feature_profile.sdwan.dns_security import DnsSecurityFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.embedded_security import EmbeddedSecurityFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.policy_object import PolicyObjectFeatureProfile
from catalystwan.endpoints.configuration_feature_profile import SDRoutingConfigurationFeatureProfile
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
    GetReferenceCountFeatureProfilesPayload,
)
from catalystwan.models.configuration.feature_profile.parcel import (
    Parcel,
    ParcelAssociationPayload,
    ParcelCreationResponse,
)
from catalystwan.models.configuration.feature_profile.sdwan.cli import AnyCliParcel
from catalystwan.models.configuration.feature_profile.sdwan.dns_security import AnyDnsSecurityParcel, DnsParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import (
    AnyEmbeddedSecurityParcel,
    NgfirewallParcel,
    PolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AnyPolicyObjectParcel,
    ApplicationListParcel,
    AppProbeParcel,
    ColorParcel,
    DataPrefixParcel,
    ExpandedCommunityParcel,
    ExtendedCommunityParcel,
    FowardingClassParcel,
    FQDNDomainParcel,
    GeoLocationListParcel,
    IPSSignatureParcel,
    IPv6DataPrefixParcel,
    IPv6PrefixListParcel,
    LocalDomainParcel,
    PolicerParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    SecurityApplicationListParcel,
    SecurityDataPrefixParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    StandardCommunityParcel,
    TlocParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
    AnySystemParcel,
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NtpParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)


def removeprefix(s: str, prefix: str) -> str:
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


class SDRoutingFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.cli = SDRoutingCLIFeatureProfileAPI(session=session)


class SDWANFeatureProfilesAPI:
    def __init__(self, session: ManagerSession):
        self.application_priority = ApplicationPriorityFeatureProfileAPI(session=session)
        self.cli = CliFeatureProfileAPI(session=session)
        self.dns_security = DnsSecurityFeatureProfileAPI(session=session)
        self.embedded_security = EmbeddedSecurityFeatureProfileAPI(session=session)
        self.other = OtherFeatureProfileAPI(session=session)
        self.policy_object = PolicyObjectFeatureProfileAPI(session=session)
        self.service = ServiceFeatureProfileAPI(session=session)
        self.sig_security = SIGSecurityAPI(session=session)
        self.system = SystemFeatureProfileAPI(session=session)
        self.topology = TopologyFeatureProfileAPI(session=session)
        self.transport = TransportFeatureProfileAPI(session=session)
        self.uc_voice = UcVoiceFeatureProfileAPI(session=session)


class FeatureProfileAPI(Protocol):
    def init_parcels(self, fp_id: str) -> None:
        """
        Initialized parcel(s) associated with this feature profile
        """
        ...

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates feature profile
        """
        ...

    def delete(self, fp_id: str) -> None:
        """
        Deletes feature profile
        """
        ...


class SDRoutingCLIFeatureProfileAPI(FeatureProfileAPI):
    """
    SD-Routing CLI feature-profile APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SDRoutingConfigurationFeatureProfile(session)

    def init_parcels(self, fp_id: str) -> None:
        """
        Initialize CLI full-config parcel associated with this feature profile
        """
        self.full_config_parcel = SDRoutingFullConfigParcelAPI(session=self.session, fp_id=fp_id)

    def create(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Creates CLI feature profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)

        return self.endpoint.create_cli_feature_profile(payload=payload)

    def delete(self, fp_id: str) -> None:
        """
        Deletes CLI feature-profile
        """
        self.endpoint.delete_cli_feature_profile(cli_fp_id=fp_id)


class TransportFeatureProfileAPI:
    """
    SDWAN Feature Profile Transport APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = TransportFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Transport Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_transport_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Transport Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_transport_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Transport Feature Profile
        """
        self.endpoint.delete_transport_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete all Transport Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def create_parcel(
        self, profile_id: UUID, payload: AnyTransportParcel, vpn_uuid: Optional[UUID] = None
    ) -> ParcelCreationResponse:
        """
        Create Transport Parcel for selected profile_id based on payload type
        """
        if vpn_uuid is not None:
            vpn_parcel = self._get_vpn_parcel(profile_id, vpn_uuid).payload
            # All interface parcels start with prefix wan/vpn to diffrentiate between
            # transport and service parcels, but the actual endpoint does not require
            # the prefix, so we remove it here. Same applies to management.
            parcel_type = payload._get_parcel_type().replace("wan/vpn/", "").replace("management/vpn/", "")
            if vpn_parcel._get_parcel_type() == TransportVpnParcel._get_parcel_type():
                return self.endpoint.create_transport_vpn_sub_parcel(profile_id, vpn_uuid, parcel_type, payload)
            else:
                return self.endpoint.create_management_vpn_sub_parcel(profile_id, vpn_uuid, parcel_type, payload)
        return self.endpoint.create_transport_parcel(profile_id, payload._get_parcel_type(), payload)

    def _get_vpn_parcel(
        self, profile_id: UUID, vpn_uuid: UUID
    ) -> Union[Parcel[TransportVpnParcel], Parcel[ManagementVpnParcel]]:
        """Resolve the VPN parcel type based on the VPN UUID."""
        try:
            return self.endpoint.get_transport_parcel(profile_id, TransportVpnParcel._get_parcel_type(), vpn_uuid)
        except ManagerHTTPError:
            pass
        try:
            return self.endpoint.get_transport_parcel(profile_id, ManagementVpnParcel._get_parcel_type(), vpn_uuid)
        except ManagerHTTPError:
            raise CatalystwanException(f"VPN parcel wih uuid: {vpn_uuid} is not found")

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[CellularControllerParcel], parcel_id: UUID
    ) -> Parcel[CellularControllerParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[T1E1ControllerParcel], parcel_id: UUID
    ) -> Parcel[T1E1ControllerParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[TransportVpnParcel], parcel_id: UUID
    ) -> Parcel[TransportVpnParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[ManagementVpnParcel], parcel_id: UUID
    ) -> Parcel[ManagementVpnParcel]:
        ...

    @overload
    def get_parcel(self, profile_id: UUID, parcel_type: Type[Ipv4AclParcel], parcel_id: UUID) -> Parcel[Ipv4AclParcel]:
        ...

    @overload
    def get_parcel(self, profile_id: UUID, parcel_type: Type[Ipv6AclParcel], parcel_id: UUID) -> Parcel[Ipv6AclParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[RoutePolicyParcel], parcel_id: UUID
    ) -> Parcel[RoutePolicyParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[WanInterfaceMultilinkParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[WanInterfaceMultilinkParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[InterfaceEthPPPoEParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[InterfaceEthPPPoEParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[InterfaceDslPPPoEParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[InterfaceDslPPPoEParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[InterfaceDslPPPoAParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[InterfaceDslPPPoAParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[InterfaceDslIPoEParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[InterfaceDslIPoEParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[WanInterfaceGreParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[WanInterfaceGreParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[WanInterfaceEthernetParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[WanInterfaceEthernetParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[ManagementInterfaceEthernetParcel], parcel_id: UUID, vpn_uuid: UUID
    ) -> Parcel[ManagementInterfaceEthernetParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[RoutingBgpParcel], parcel_id: UUID
    ) -> Parcel[RoutingBgpParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[RoutingOspfParcel], parcel_id: UUID
    ) -> Parcel[RoutingOspfParcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[RoutingOspfv3IPv6Parcel], parcel_id: UUID
    ) -> Parcel[RoutingOspfv3IPv6Parcel]:
        ...

    @overload
    def get_parcel(
        self, profile_id: UUID, parcel_type: Type[RoutingOspfv3IPv4Parcel], parcel_id: UUID
    ) -> Parcel[RoutingOspfv3IPv4Parcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[InterfaceCellularParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[InterfaceCellularParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[T1E1SerialParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[T1E1SerialParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[WanInterfaceIpsecParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[WanInterfaceIpsecParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[Union[AnyTransportParcel, AnyRoutingParcel]],
        parcel_id: UUID,
        vpn_uuid: Optional[UUID] = None,
    ) -> Parcel:
        """
        Get one Transport Parcel given profile id, parcel type and parcel id
        """
        if vpn_uuid is not None:
            vpn_parcel = self._get_vpn_parcel(profile_id, vpn_uuid).payload
            parcel_type_str = parcel_type._get_parcel_type()
            parcel_type_str = removeprefix(parcel_type_str, "wan/vpn/")
            parcel_type_str = removeprefix(parcel_type_str, "management/vpn/")
            if vpn_parcel._get_parcel_type() == TransportVpnParcel._get_parcel_type():
                return self.endpoint.get_transport_vpn_sub_parcel(profile_id, vpn_uuid, parcel_type_str, parcel_id)
            else:
                return self.endpoint.get_management_vpn_sub_parcel(profile_id, vpn_uuid, parcel_type_str, parcel_id)
        return self.endpoint.get_transport_parcel(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def update_parcel(
        self, profile_id: UUID, payload: AnyTransportParcel, parcel_id: UUID, vpn_uuid: Optional[UUID] = None
    ) -> ParcelCreationResponse:
        """
        Update Transport Parcel for selected profile_id based on payload type
        """
        if vpn_uuid is not None:
            vpn_parcel = self._get_vpn_parcel(profile_id, vpn_uuid).payload
            parcel_type = payload._get_parcel_type()
            parcel_type = removeprefix(parcel_type, "wan/vpn/")
            parcel_type = removeprefix(parcel_type, "management/vpn/")
            if vpn_parcel._get_parcel_type() == TransportVpnParcel._get_parcel_type():
                return self.endpoint.update_transport_vpn_sub_parcel(
                    profile_id, vpn_uuid, parcel_type, parcel_id, payload
                )
            else:
                return self.endpoint.update_management_vpn_sub_parcel(
                    profile_id, vpn_uuid, parcel_type, parcel_id, payload
                )
        return self.endpoint.update_transport_parcel(profile_id, payload._get_parcel_type(), parcel_id, payload)


class OtherFeatureProfileAPI:
    """
    SDWAN Feature Profile System APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = OtherFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Other Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_other_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Other Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_other_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Other Feature Profile
        """
        self.endpoint.delete_sdwan_other_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete all Other Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def get(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyOtherParcel],  # UCSE, 1000-eyes, cybervision
        parcel_id: Union[UUID, None] = None,
    ) -> DataSequence[Parcel[Any]]:
        """
        Get all Other Parcels for selected profile_id and selected type or get one Other Parcel given parcel id
        """

        if not parcel_id:
            return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyOtherParcel) -> ParcelCreationResponse:
        """
        Create Other Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnyOtherParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update Other Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyOtherParcel], parcel_id: UUID) -> None:
        """
        Delete Other Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class ServiceFeatureProfileAPI:
    """
    SDWAN Feature Profile Service APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = ServiceFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Service Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_service_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Service Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_service_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Service Feature Profile
        """
        self.endpoint.delete_sdwan_service_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete all Service Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def create_parcel(
        self, profile_id: UUID, payload: AnyServiceParcel, vpn_uuid: Optional[UUID] = None
    ) -> ParcelCreationResponse:
        """
        Create Service Parcel for selected profile_id based on payload type
        """
        if vpn_uuid is not None:
            if isinstance(payload, MulticastParcel):
                response = self.endpoint.create_service_parcel(profile_id, payload._get_parcel_type(), payload)
                return self.endpoint.associate_parcel_with_vpn(
                    profile_id, vpn_uuid, payload._get_parcel_type(), ParcelAssociationPayload(parcel_id=response.id)
                )
            else:
                parcel_type = payload._get_parcel_type().replace("lan/vpn/", "")
                return self.endpoint.create_lan_vpn_sub_parcel(profile_id, vpn_uuid, parcel_type, payload)
        return self.endpoint.create_service_parcel(profile_id, payload._get_parcel_type(), payload)

    def delete_parcel(
        self,
        profile_uuid: UUID,
        parcel_type: Type[AnyServiceParcel],
        parcel_uuid: UUID,
        vpn_uuid: Optional[UUID] = None,
    ) -> None:
        """
        Delete Service Parcel for selected profile_uuid based on payload type
        """
        if vpn_uuid is not None:
            return self.endpoint.delete_lan_vpn_sub_parcel(
                profile_uuid, vpn_uuid, removeprefix(parcel_type._get_parcel_type(), "lan/vpn/"), parcel_uuid
            )
        return self.endpoint.delete_service_parcel(profile_uuid, parcel_type._get_parcel_type(), parcel_uuid)

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutePolicyParcel],
    ) -> DataSequence[Parcel[RoutePolicyParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[Ipv4AclParcel],
    ) -> DataSequence[Parcel[Ipv4AclParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[Ipv6AclParcel],
    ) -> DataSequence[Parcel[Ipv6AclParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[LanVpnParcel],
    ) -> DataSequence[Parcel[LanVpnParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[MulticastParcel],
    ) -> DataSequence[Parcel[MulticastParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[EigrpParcel],
    ) -> DataSequence[Parcel[EigrpParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SwitchportParcel],
    ) -> DataSequence[Parcel[SwitchportParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[WirelessLanParcel],
    ) -> DataSequence[Parcel[WirelessLanParcel]]:
        ...

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyServiceParcel],
    ) -> DataSequence:
        """
        Get all Service Parcels given profile id and parcel type
        """
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutePolicyParcel],
        parcel_id: UUID,
    ) -> Parcel[RoutePolicyParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[Ipv4AclParcel],
        parcel_id: UUID,
    ) -> Parcel[Ipv4AclParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[Ipv6AclParcel],
        parcel_id: UUID,
    ) -> Parcel[Ipv6AclParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LanVpnParcel],
        parcel_id: UUID,
    ) -> Parcel[LanVpnParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MulticastParcel],
        parcel_id: UUID,
    ) -> Parcel[MulticastParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[EigrpParcel],
        parcel_id: UUID,
    ) -> Parcel[EigrpParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SwitchportParcel],
        parcel_id: UUID,
    ) -> Parcel[SwitchportParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[WirelessLanParcel],
        parcel_id: UUID,
    ) -> Parcel[WirelessLanParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LanInterfaceEthernetParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[LanInterfaceEthernetParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LanInterfaceGreParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[LanInterfaceGreParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LanInterfaceIpsecParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[LanInterfaceIpsecParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[InterfaceSviParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[InterfaceSviParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LanInterfaceMultilinkParcel],
        parcel_id: UUID,
        vpn_uuid: UUID,
    ) -> Parcel[LanInterfaceMultilinkParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutingBgpParcel],
        parcel_id: UUID,
    ) -> Parcel[RoutingBgpParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutingOspfv3IPv6Parcel],
        parcel_id: UUID,
    ) -> Parcel[RoutingOspfv3IPv6Parcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutingOspfParcel],
        parcel_id: UUID,
    ) -> Parcel[RoutingOspfParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[RoutingOspfv3IPv4Parcel],
        parcel_id: UUID,
    ) -> Parcel[RoutingOspfv3IPv4Parcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyServiceParcel],
        parcel_id: UUID,
        vpn_uuid: Optional[UUID] = None,
    ) -> Parcel:
        """
        Get one Service Parcel given profile id, parcel type and parcel id
        """
        if vpn_uuid is not None:
            return self.endpoint.get_lan_vpn_sub_parcel(
                profile_id, vpn_uuid, removeprefix(parcel_type._get_parcel_type(), "lan/vpn/"), parcel_id
            )
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def update_parcel(
        self,
        profile_id: UUID,
        payload: AnyServiceParcel,
        parcel_id: UUID,
        vpn_uuid: Optional[UUID] = None,
    ) -> ParcelCreationResponse:
        """
        Update Service Parcel for selected profile_id based on payload type
        """
        if vpn_uuid is not None:
            return self.endpoint.update_lan_vpn_sub_parcel(
                profile_id, vpn_uuid, removeprefix(payload._get_parcel_type(), "lan/vpn/"), parcel_id, payload
            )
        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)


class SystemFeatureProfileAPI:
    """
    SDWAN Feature Profile System APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SystemFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all System Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_sdwan_system_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create System Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sdwan_system_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete System Feature Profile
        """
        self.endpoint.delete_sdwan_system_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete all System Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def get_schema(
        self,
        profile_id: UUID,
        parcel_type: Type[AnySystemParcel],
    ) -> Json:
        """
        Get all System Parcels for selected profile_id and selected type or get one Policy Object given parcel id
        """

        return self.endpoint.get_schema(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
    ) -> DataSequence[Parcel[AAAParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
    ) -> DataSequence[Parcel[BannerParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
    ) -> DataSequence[Parcel[BasicParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
    ) -> DataSequence[Parcel[BFDParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
    ) -> DataSequence[Parcel[GlobalParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
    ) -> DataSequence[Parcel[LoggingParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
    ) -> DataSequence[Parcel[MRFParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[NtpParcel],
    ) -> DataSequence[Parcel[NtpParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
    ) -> DataSequence[Parcel[OMPParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
    ) -> DataSequence[Parcel[SecurityParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
    ) -> DataSequence[Parcel[SNMPParcel]]:
        ...

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AnySystemParcel],
    ) -> DataSequence:
        """
        Get all System Parcels given profile id and parcel type
        """
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
        parcel_id: UUID,
    ) -> Parcel[AAAParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
        parcel_id: UUID,
    ) -> Parcel[BannerParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
        parcel_id: UUID,
    ) -> Parcel[BasicParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
        parcel_id: UUID,
    ) -> Parcel[BFDParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
        parcel_id: UUID,
    ) -> Parcel[GlobalParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
        parcel_id: UUID,
    ) -> Parcel[LoggingParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
        parcel_id: UUID,
    ) -> Parcel[MRFParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[NtpParcel],
        parcel_id: UUID,
    ) -> Parcel[NtpParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
        parcel_id: UUID,
    ) -> Parcel[OMPParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
        parcel_id: UUID,
    ) -> Parcel[SecurityParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
        parcel_id: UUID,
    ) -> Parcel[SNMPParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnySystemParcel],
        parcel_id: UUID,
    ) -> Parcel:
        """
        Get one System Parcel given profile id, parcel type and parcel id
        """
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnySystemParcel) -> ParcelCreationResponse:
        """
        Create System Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnySystemParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update System Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AAAParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BFDParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[LoggingParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BannerParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[BasicParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[GlobalParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[NtpParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MRFParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[OMPParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SecurityParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    @overload
    def delete_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[SNMPParcel],
        parcel_id: UUID,
    ) -> None:
        ...

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnySystemParcel], parcel_id: UUID) -> None:
        """
        Delete System Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class PolicyObjectFeatureProfileAPI:
    """
    SDWAN Feature Profile Policy Object APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = PolicyObjectFeatureProfile(session)

    def get_profiles(self) -> DataSequence[FeatureProfileInfo]:
        return self.endpoint.get_profiles()

    def create_profile(self, profile: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        return self.endpoint.create_profile(profile)

    def delete_profile(self, profile_id: UUID) -> None:
        return self.endpoint.delete_profile(profile_id=profile_id)

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[AdvancedInspectionProfileParcel]
    ) -> DataSequence[Parcel[AdvancedInspectionProfileParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[AdvancedMalwareProtectionParcel]
    ) -> DataSequence[Parcel[AdvancedMalwareProtectionParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ApplicationListParcel]
    ) -> DataSequence[Parcel[ApplicationListParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel]) -> DataSequence[Parcel[AppProbeParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AsPathParcel]) -> DataSequence[Parcel[AsPathParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel]) -> DataSequence[Parcel[ColorParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel]) -> DataSequence[Parcel[DataPrefixParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel]
    ) -> DataSequence[Parcel[ExpandedCommunityParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[FowardingClassParcel]
    ) -> DataSequence[Parcel[FowardingClassParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel]) -> DataSequence[Parcel[FQDNDomainParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel]
    ) -> DataSequence[Parcel[GeoLocationListParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IntrusionPreventionParcel]
    ) -> DataSequence[Parcel[IntrusionPreventionParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel]) -> DataSequence[Parcel[IPSSignatureParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel]
    ) -> DataSequence[Parcel[IPv6DataPrefixParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel]
    ) -> DataSequence[Parcel[IPv6PrefixListParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel]) -> DataSequence[Parcel[LocalDomainParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[MirrorParcel]) -> DataSequence[Parcel[MirrorParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicerParcel]) -> DataSequence[Parcel[PolicerParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel]
    ) -> DataSequence[Parcel[PreferredColorGroupParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel]) -> DataSequence[Parcel[PrefixListParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ProtocolListParcel]) -> DataSequence[Parcel[ProtocolListParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel]
    ) -> DataSequence[Parcel[SecurityApplicationListParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel]
    ) -> DataSequence[Parcel[SecurityDataPrefixParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SecurityPortParcel]) -> DataSequence[Parcel[SecurityPortParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel]
    ) -> DataSequence[Parcel[SecurityZoneListParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SLAClassParcel]) -> DataSequence[Parcel[SLAClassParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SslDecryptionParcel]
    ) -> DataSequence[Parcel[SslDecryptionParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SslDecryptionProfileParcel]
    ) -> DataSequence[Parcel[SslDecryptionProfileParcel]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel]
    ) -> DataSequence[Parcel[StandardCommunityParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel]) -> DataSequence[Parcel[TlocParcel]]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLParcel]) -> DataSequence[Parcel[TlocParcel]]:
        ...

    # get by id

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[AdvancedInspectionProfileParcel], parcel_id: UUID
    ) -> Parcel[AdvancedInspectionProfileParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[AdvancedMalwareProtectionParcel], parcel_id: UUID
    ) -> Parcel[AdvancedMalwareProtectionParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ApplicationListParcel], parcel_id: UUID
    ) -> Parcel[ApplicationListParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AppProbeParcel], parcel_id: UUID) -> Parcel[AppProbeParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[AsPathParcel], parcel_id: UUID) -> Parcel[AsPathParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[ColorParcel], parcel_id: UUID) -> Parcel[ColorParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[DataPrefixParcel], parcel_id: UUID) -> Parcel[DataPrefixParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ExpandedCommunityParcel], parcel_id: UUID
    ) -> Parcel[ExpandedCommunityParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ExtendedCommunityParcel], parcel_id: UUID
    ) -> DataSequence[Parcel[Any]]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[FowardingClassParcel], parcel_id: UUID
    ) -> Parcel[FowardingClassParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[FQDNDomainParcel], parcel_id: UUID) -> Parcel[FQDNDomainParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[GeoLocationListParcel], parcel_id: UUID
    ) -> Parcel[GeoLocationListParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IntrusionPreventionParcel], parcel_id: UUID
    ) -> Parcel[IntrusionPreventionParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPSSignatureParcel], parcel_id: UUID
    ) -> Parcel[IPSSignatureParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6DataPrefixParcel], parcel_id: UUID
    ) -> Parcel[IPv6DataPrefixParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[IPv6PrefixListParcel], parcel_id: UUID
    ) -> Parcel[IPv6PrefixListParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[LocalDomainParcel], parcel_id: UUID) -> Parcel[LocalDomainParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[MirrorParcel], parcel_id: UUID) -> Parcel[MirrorParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PolicerParcel], parcel_id: UUID) -> Parcel[PolicerParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[PreferredColorGroupParcel], parcel_id: UUID
    ) -> Parcel[PreferredColorGroupParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[PrefixListParcel], parcel_id: UUID) -> Parcel[PrefixListParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[ProtocolListParcel], parcel_id: UUID
    ) -> Parcel[ProtocolListParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityApplicationListParcel], parcel_id: UUID
    ) -> Parcel[SecurityApplicationListParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityDataPrefixParcel], parcel_id: UUID
    ) -> Parcel[SecurityDataPrefixParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityPortParcel], parcel_id: UUID
    ) -> Parcel[SecurityPortParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SecurityZoneListParcel], parcel_id: UUID
    ) -> Parcel[SecurityZoneListParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[SLAClassParcel], parcel_id: UUID) -> Parcel[SLAClassParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SslDecryptionParcel], parcel_id: UUID
    ) -> Parcel[SslDecryptionParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[SslDecryptionProfileParcel], parcel_id: UUID
    ) -> Parcel[SslDecryptionProfileParcel]:
        ...

    @overload
    def get(
        self, profile_id: UUID, parcel_type: Type[StandardCommunityParcel], parcel_id: UUID
    ) -> Parcel[StandardCommunityParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[TlocParcel], parcel_id: UUID) -> Parcel[TlocParcel]:
        ...

    @overload
    def get(self, profile_id: UUID, parcel_type: Type[URLParcel], parcel_id: UUID) -> Parcel[TlocParcel]:
        ...

    def get(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyPolicyObjectParcel],
        parcel_id: Union[UUID, None] = None,
    ) -> Any:
        """
        Get all Policy Objects for selected profile_id and selected type or get one Policy Object given parcel id
        """

        policy_object_list_type = parcel_type._get_parcel_type()
        if parcel_id is None:
            return self.endpoint.get_all(profile_id=profile_id, policy_object_list_type=policy_object_list_type)
        return self.endpoint.get_by_id(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=parcel_id
        )

    def create_parcel(self, profile_id: UUID, payload: AnyPolicyObjectParcel) -> ParcelCreationResponse:
        """
        Create Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = payload._get_parcel_type()
        return self.endpoint.create(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, payload=payload
        )

    def update(self, profile_id: UUID, payload: AnyPolicyObjectParcel, list_object_id: UUID):
        """
        Update Policy Object for selected profile_id based on payload type
        """

        policy_type = payload._get_parcel_type()
        return self.endpoint.update(
            profile_id=profile_id, policy_object_list_type=policy_type, list_object_id=list_object_id, payload=payload
        )

    def delete(self, profile_id: UUID, parcel_type: Type[AnyPolicyObjectParcel], list_object_id: UUID) -> None:
        """
        Delete Policy Object for selected profile_id based on payload type
        """

        policy_object_list_type = parcel_type._get_parcel_type()
        return self.endpoint.delete(
            profile_id=profile_id, policy_object_list_type=policy_object_list_type, list_object_id=list_object_id
        )


class EmbeddedSecurityFeatureProfileAPI:
    """
    SDWAN Feature Profile Embedded Security APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = EmbeddedSecurityFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Embedded Security Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_embedded_security_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Embedded Security Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_embedded_security_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Embedded Security Feature Profile
        """
        self.endpoint.delete_embedded_security_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete Embedded Security Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[NgfirewallParcel],
    ) -> DataSequence[Parcel[NgfirewallParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[PolicyParcel],
    ) -> DataSequence[Parcel[PolicyParcel]]:
        ...

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyEmbeddedSecurityParcel],
    ) -> DataSequence:
        """
        Get all Embedded Security Parcels given profile id and parcel type
        """
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[NgfirewallParcel],
        parcel_id: UUID,
    ) -> Parcel[NgfirewallParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[PolicyParcel],
        parcel_id: UUID,
    ) -> Parcel[PolicyParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyEmbeddedSecurityParcel],
        parcel_id: UUID,
    ) -> Parcel:
        """
        Get one Embedded Security Parcel given profile id, parcel type and parcel id
        """
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyEmbeddedSecurityParcel) -> ParcelCreationResponse:
        """
        Create Embedded Security Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(
        self, profile_id: UUID, payload: AnyEmbeddedSecurityParcel, parcel_id: UUID
    ) -> ParcelCreationResponse:
        """
        Update Embedded Security Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyEmbeddedSecurityParcel], parcel_id: UUID) -> None:
        """
        Delete Embedded Security Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class CliFeatureProfileAPI:
    """
    SDWAN Feature Profile CLI APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = CliFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all CLI Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_profiles(payload)

    def create_profile(self, name: str, description: str = "") -> FeatureProfileCreationResponse:
        """
        Create CLI Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete CLI Feature Profile
        """
        self.endpoint.delete_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete all CLI Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def get_parcel_by_id(
        self,
        profile_id: UUID,
        parcel_id: UUID,
        parcel_type: str = "config",
    ) -> Parcel[AnyCliParcel]:
        """
        Get all CLI Parcels for selected profile_id and selected type or get one CLI Parcel given parcel id
        """
        return self.endpoint.get_by_id(profile_id, parcel_type, parcel_id)

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: str = "config",
    ) -> DataSequence[Parcel[AnyCliParcel]]:
        """
        Get all CLI Parcels for selected profile_id and selected type or get one CLI Parcel given parcel id
        """
        return self.endpoint.get_all(profile_id, parcel_type)

    def create_parcel(self, profile_id: UUID, config: AnyCliParcel) -> ParcelCreationResponse:
        """
        Create CLI Parcel for selected profile_id
        """
        return self.endpoint.create(profile_id, config._get_parcel_type(), config)

    def update_parcel(self, profile_id: UUID, config: AnyCliParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update CLI Parcel for selected profile_id
        """
        return self.endpoint.update(profile_id, config._get_parcel_type(), parcel_id, config)

    def delete_parcel(self, profile_id: UUID, parcel_id: UUID) -> None:
        """
        Delete CLI Parcel for selected profile_id
        """
        return self.endpoint.delete(profile_id, parcel_id)


class DnsSecurityFeatureProfileAPI:
    """
    SDWAN Feature Profile DNS Security APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = DnsSecurityFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all DNS Security Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_dns_security_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create DNS Security Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_dns_security_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete DNS Security Feature Profile
        """
        self.endpoint.delete_dns_security_feature_profile(profile_id)

    def delete_all_profiles(self) -> None:
        """
        Delete DNS Security Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[DnsParcel],
    ) -> DataSequence[Parcel[DnsParcel]]:
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[DnsParcel],
        parcel_id: UUID,
    ) -> Parcel[DnsParcel]:
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyDnsSecurityParcel) -> ParcelCreationResponse:
        """
        Create DNS Security Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnyDnsSecurityParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update DNS Security Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyDnsSecurityParcel], parcel_id: UUID) -> None:
        """
        Delete DNS Security Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class SIGSecurityAPI:
    """
    SDWAN Feature Profile Service APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = SIGSecurity(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None, reference_count: Optional[bool] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all SIG Security Feature Profiles
        """
        payload = GetReferenceCountFeatureProfilesPayload(limit=limit, offset=offset, reference_count=reference_count)

        return self.endpoint.get_sig_security_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create SIG Security Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_sig_security_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete SIG Security Feature Profile
        """
        self.endpoint.delete_sig_security_feature_profile(str(profile_id))

    def delete_all_profiles(self) -> None:
        """
        Delete all SIG Security Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def create_parcel(self, profile_uuid: UUID, payload: SIGParcel) -> ParcelCreationResponse:
        """
        Create SIG Security Parcel for selected profile_id
        """
        return self.endpoint.create_sig_security_parcel(str(profile_uuid), payload)

    def delete_parcel(self, profile_uuid: UUID, parcel_uuid: UUID) -> None:
        """
        Delete Service Parcel for selected profile_uuid based on payload type
        """
        return self.endpoint.delete_sig_security_parcel(str(profile_uuid), str(parcel_uuid))


class ApplicationPriorityFeatureProfileAPI:
    """
    SDWAN Feature Profile Application Priority APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = ApplicationPriorityFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Application Priority Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_application_priority_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Application Priority Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_application_priority_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Application Priority Feature Profile
        """
        self.endpoint.delete_application_priority_feature_profile(str(profile_id))

    def delete_all_profiles(self) -> None:
        """
        Delete all Application Priority Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[QosPolicyParcel],
    ) -> DataSequence[Parcel[QosPolicyParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[PolicySettingsParcel],
    ) -> DataSequence[Parcel[PolicySettingsParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[TrafficPolicyParcel],
    ) -> DataSequence[Parcel[TrafficPolicyParcel]]:
        ...

    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyApplicationPriorityParcel],
    ) -> DataSequence:
        """
        Get all Application Priority Parcels given profile id and parcel type
        """
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[PolicySettingsParcel],
        parcel_id: UUID,
    ) -> Parcel[PolicySettingsParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[TrafficPolicyParcel],
        parcel_id: UUID,
    ) -> Parcel[TrafficPolicyParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[QosPolicyParcel],
        parcel_id: UUID,
    ) -> Parcel[QosPolicyParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyApplicationPriorityParcel],
        parcel_id: UUID,
    ) -> Parcel:
        """
        Get one Application Priority Parcel given profile id, parcel type and parcel id
        """
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyApplicationPriorityParcel) -> ParcelCreationResponse:
        """
        Create Application Priority Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(
        self, profile_id: UUID, payload: AnyApplicationPriorityParcel, parcel_id: UUID
    ) -> ParcelCreationResponse:
        """
        Update Application Priority Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyApplicationPriorityParcel], parcel_id: UUID) -> None:
        """
        Delete Application Priority Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)


class TopologyFeatureProfileAPI:
    """
    SDWAN Feature Profile Topology APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = TopologyFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all Topology Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit, offset=offset)
        return self.endpoint.get_topology_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create Topology Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_topology_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete Topology Feature Profile
        """
        self.endpoint.delete_topology_feature_profile(str(profile_id))

    def delete_all_profiles(self) -> None:
        """
        Delete all Topology Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    def create_parcel(self, profile_id: UUID, parcel: AnyTopologyParcel) -> ParcelCreationResponse:
        """
        Create Topology Parcel for selected profile_id based on payload type
        """
        return self.endpoint.create_any_parcel(profile_id, parcel._get_parcel_type(), parcel)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyTopologyParcel], parcel_id: UUID) -> None:
        """
        Delete Topology Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete_any_parcel(
            profile_id=profile_id, parcel_type=parcel_type._get_parcel_type(), parcel_id=parcel_id
        )

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[HubSpokeParcel],
        parcel_id: UUID,
    ) -> Parcel[HubSpokeParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MeshParcel],
        parcel_id: UUID,
    ) -> Parcel[MeshParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[CustomControlParcel],
        parcel_id: UUID,
    ) -> Parcel[CustomControlParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyTopologyParcel],
        parcel_id: UUID,
    ) -> Parcel:
        """
        Get one Topology Parcel given profile id, parcel type and parcel id
        """
        return self.endpoint.get_any_parcel_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)


class UcVoiceFeatureProfileAPI:
    """
    SDWAN Feature Profile UC Voice APIs
    """

    def __init__(self, session: ManagerSession):
        self.session = session
        self.endpoint = UcVoiceFeatureProfile(session)

    def get_profiles(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> DataSequence[FeatureProfileInfo]:
        """
        Get all UC Voice Feature Profiles
        """
        payload = GetFeatureProfilesParams(limit=limit if limit else None, offset=offset if offset else None)

        return self.endpoint.get_uc_voice_feature_profiles(payload)

    def create_profile(self, name: str, description: str) -> FeatureProfileCreationResponse:
        """
        Create UC Voice Feature Profile
        """
        payload = FeatureProfileCreationPayload(name=name, description=description)
        return self.endpoint.create_uc_voice_feature_profile(payload)

    def delete_profile(self, profile_id: UUID) -> None:
        """
        Delete UC Voice Feature Profile
        """
        self.endpoint.delete_uc_voice_feature_profile(str(profile_id))

    def delete_all_profiles(self) -> None:
        """
        Delete all UC Voice Feature Profiles
        """
        profiles = self.get_profiles()
        for profile in profiles:
            self.delete_profile(profile.profile_id)

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[DspFarmParcel],
    ) -> DataSequence[Parcel[DspFarmParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[MediaProfileParcel],
    ) -> DataSequence[Parcel[MediaProfileParcel]]:
        ...

    @overload
    def get_parcels(
        self,
        profile_id: UUID,
        parcel_type: Type[TrunkGroupParcel],
    ) -> DataSequence[Parcel[TrunkGroupParcel]]:
        ...

    def get_parcels(self, profile_id: UUID, parcel_type: Type[AnyUcVoiceParcel]) -> DataSequence[Parcel]:
        """
        Get all UC Voice Parcels given profile id and parcel type
        """
        return self.endpoint.get_all(profile_id, parcel_type._get_parcel_type())

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[DspFarmParcel],
        parcel_id: UUID,
    ) -> Parcel[DspFarmParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[MediaProfileParcel],
        parcel_id: UUID,
    ) -> Parcel[MediaProfileParcel]:
        ...

    @overload
    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[TrunkGroupParcel],
        parcel_id: UUID,
    ) -> Parcel[TrunkGroupParcel]:
        ...

    def get_parcel(
        self,
        profile_id: UUID,
        parcel_type: Type[AnyUcVoiceParcel],
        parcel_id: UUID,
    ) -> Parcel:
        """
        Get one UC Voice Parcel given profile id, parcel type and parcel id
        """
        return self.endpoint.get_by_id(profile_id, parcel_type._get_parcel_type(), parcel_id)

    def create_parcel(self, profile_id: UUID, payload: AnyUcVoiceParcel) -> ParcelCreationResponse:
        """
        Create UC Voice Parcel for selected profile_id based on payload type
        """

        return self.endpoint.create(profile_id, payload._get_parcel_type(), payload)

    def update_parcel(self, profile_id: UUID, payload: AnyUcVoiceParcel, parcel_id: UUID) -> ParcelCreationResponse:
        """
        Update UC Voice Parcel for selected profile_id based on payload type
        """

        return self.endpoint.update(profile_id, payload._get_parcel_type(), parcel_id, payload)

    def delete_parcel(self, profile_id: UUID, parcel_type: Type[AnyUcVoiceParcel], parcel_id: UUID) -> None:
        """
        Delete UC Voice Parcel for selected profile_id based on payload type
        """
        return self.endpoint.delete(profile_id, parcel_type._get_parcel_type(), parcel_id)
