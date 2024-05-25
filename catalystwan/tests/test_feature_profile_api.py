# Copyright 2023 Cisco Systems, Inc. and its affiliates
import unittest
from unittest.mock import Mock
from uuid import uuid4

from parameterized import parameterized  # type: ignore

from catalystwan.api.feature_profile_api import (
    ServiceFeatureProfileAPI,
    SystemFeatureProfileAPI,
    TransportFeatureProfileAPI,
)
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.system import SystemFeatureProfile
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.models.configuration.feature_profile.parcel import ParcelAssociationPayload, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing import (
    RoutingOspfParcel,
    RoutingOspfv3IPv4Parcel,
    RoutingOspfv3IPv6Parcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import AppqoeParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    InterfaceEthernetParcel as LanInterfaceEthernetParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import InterfaceGreParcel as LanInterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    InterfaceIpsecParcel as LanInterfaceIpsecParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import InterfaceSviParcel as LanInterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    LanVpnDhcpServerParcel,
    LanVpnParcel,
    SwitchportParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.eigrp import EigrpParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import MulticastParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import WirelessLanParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    AAAParcel,
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
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport import InterfaceGreParcel as WanInterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    InterfaceIpsecParcel as WanInterfaceIpsecParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    ManagementVpnParcel,
    T1E1ControllerParcel,
    TransportVpnParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import CellularProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    InterfaceCellularParcel,
)

system_endpoint_mapping = {
    AAAParcel: "aaa",
    BannerParcel: "banner",
    BasicParcel: "basic",
    BFDParcel: "bfd",
    GlobalParcel: "global",
    LoggingParcel: "logging",
    MRFParcel: "mrf",
    NtpParcel: "ntp",
    OMPParcel: "omp",
    SecurityParcel: "security",
    SNMPParcel: "snmp",
}


class TestSystemFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=SystemFeatureProfile)
        self.api = SystemFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(system_endpoint_mapping.items())
    def test_delete_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.delete_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.delete.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.get_by_id.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_get_all_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.get_parcels(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.get_all.assert_called_once_with(self.profile_uuid, expected_path)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_create_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create.assert_called_once_with(self.profile_uuid, expected_path, parcel)

    @parameterized.expand(system_endpoint_mapping.items())
    def test_update_method_with_valid_arguments(self, parcel, expected_path):
        # Act
        self.api.update_parcel(self.profile_uuid, parcel, self.parcel_uuid)

        # Assert
        self.mock_endpoint.update.assert_called_once_with(self.profile_uuid, expected_path, self.parcel_uuid, parcel)


service_endpoint_mapping = {
    LanVpnDhcpServerParcel: "dhcp-server",
    AppqoeParcel: "appqoe",
    LanVpnParcel: "lan/vpn",
    RoutingOspfParcel: "routing/ospf",
    RoutingOspfv3IPv4Parcel: "routing/ospfv3/ipv4",
    RoutingOspfv3IPv6Parcel: "routing/ospfv3/ipv6",
    RoutePolicyParcel: "route-policy",
    EigrpParcel: "routing/eigrp",
    Ipv6AclParcel: "ipv6-acl",
    Ipv4AclParcel: "ipv4-acl",
    SwitchportParcel: "switchport",
    MulticastParcel: "routing/multicast",
    WirelessLanParcel: "wirelesslan",
}

service_interface_parcels = [
    ("interface/gre", LanInterfaceGreParcel),
    ("interface/svi", LanInterfaceSviParcel),
    ("interface/ethernet", LanInterfaceEthernetParcel),
    ("interface/ipsec", LanInterfaceIpsecParcel),
]

service_vpn_sub_parcels = [
    (
        "routing/multicast",
        MulticastParcel(
            parcel_name="TestMulticastParcel",
            parcel_description="Test Multicast Parcel",
        ),
    )
]


class TestServiceFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.vpn_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=ServiceFeatureProfile)
        self.api = ServiceFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint

    @parameterized.expand(service_endpoint_mapping.items())
    def test_post_method_parcel(self, parcel, parcel_type):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_service_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)

    @parameterized.expand(service_interface_parcels)
    def test_post_method_interface_parcel(self, parcel_type, parcel):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_lan_vpn_sub_parcel.assert_called_once_with(
            self.profile_uuid, self.vpn_uuid, parcel_type, parcel
        )

    @parameterized.expand(service_vpn_sub_parcels)
    def test_post_method_create_then_assigin_subparcel(self, parcel_type, parcel):
        # Arrange
        self.mock_endpoint.create_service_parcel.return_value = ParcelCreationResponse(id=self.parcel_uuid)

        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_service_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)
        self.mock_endpoint.associate_parcel_with_vpn.assert_called_once_with(
            self.profile_uuid,
            self.vpn_uuid,
            parcel_type,
            ParcelAssociationPayload(parcel_id=self.parcel_uuid),
        )


transport_enpoint_mapping = {
    T1E1ControllerParcel: "t1-e1-controller",
    GpsParcel: "gps",
    CellularControllerParcel: "cellular-controller",
    CellularProfileParcel: "cellular-profile",
    ManagementVpnParcel: "management/vpn",
    TransportVpnParcel: "wan/vpn",
}

transport_interface_parcels = [
    ("interface/ipsec", WanInterfaceIpsecParcel),
    ("interface/dsl-ipoe", InterfaceDslIPoEParcel),
    (
        "interface/ethpppoe",
        InterfaceEthPPPoEParcel,
    ),
    (
        "interface/dsl-pppoe",
        InterfaceDslPPPoEParcel,
    ),
    (
        "interface/dsl-pppoa",
        InterfaceDslPPPoAParcel,
    ),
    ("interface/gre", WanInterfaceGreParcel),
    ("interface/cellular", InterfaceCellularParcel),
]


class TestTransportFeatureProfileAPI(unittest.TestCase):
    def setUp(self):
        self.profile_uuid = uuid4()
        self.vpn_uuid = uuid4()
        self.parcel_uuid = uuid4()
        self.mock_session = Mock()
        self.mock_endpoint = Mock(spec=TransportFeatureProfile)
        self.api = TransportFeatureProfileAPI(self.mock_session)
        self.api.endpoint = self.mock_endpoint
        parcel_mock = Mock()
        parcel_mock.payload._get_parcel_type.return_value = "wan/vpn"
        self.api._get_vpn_parcel = Mock(return_value=parcel_mock)

    @parameterized.expand(transport_enpoint_mapping.items())
    def test_post_method_parcel(self, parcel, parcel_type):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel)

        # Assert
        self.mock_endpoint.create_transport_parcel.assert_called_once_with(self.profile_uuid, parcel_type, parcel)

    @parameterized.expand(transport_interface_parcels)
    def test_post_method_interface_parcel(self, parcel_type, parcel):
        # Act
        self.api.create_parcel(self.profile_uuid, parcel, self.vpn_uuid)

        # Assert
        self.mock_endpoint.create_transport_vpn_sub_parcel.assert_called_once_with(
            self.profile_uuid, self.vpn_uuid, parcel_type, parcel
        )
