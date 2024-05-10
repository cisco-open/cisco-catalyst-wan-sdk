from typing import List

import pytest
from pydantic import ValidationError

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.dns_security import DnsParcel, TargetVpns


class TestDnsSecurityParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.dns_security
        self.profile_id = self.api.create_profile("TestDnsSecurityProfile", "Description").id

    def test_create_cli_config_parcel(self):
        dns_parcel = DnsParcel(
            name="dns_parcel",
            match_all_vpn=Global[bool](value=True),
            dns_crypt=Global[bool](value=False),
            local_domain_bypass_enabled=Global[bool](value=False),
            umbrella_default=Global[bool](value=False),
            child_org_id=Global[str](value="1235"),
            dns_server_ip=Global[str](value="192.168.11.11"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, dns_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, DnsParcel, parcel_id).payload

        assert parcel.parcel_name == "dns_parcel"
        assert parcel.dns_server_ip == Global[str](value="192.168.11.11")

    def test_update_cli_config_parcel(self):
        dns_parcel = DnsParcel(
            name="dns_parcel",
            match_all_vpn=Global[bool](value=True),
            dns_crypt=Global[bool](value=False),
            local_domain_bypass_enabled=Global[bool](value=False),
            umbrella_default=Global[bool](value=False),
            child_org_id=Global[str](value="1235"),
            dns_server_ip=Global[str](value="192.168.11.11"),
        )
        parcel_id = self.api.create_parcel(self.profile_id, dns_parcel).id
        parcel = self.api.get_parcel(self.profile_id, DnsParcel, parcel_id).payload
        parcel.dns_server_ip = Global[str](value="172.16.2.2")
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, DnsParcel, parcel_id).payload

        # Assert
        assert parcel.dns_server_ip == Global[str](value="172.16.2.2")

    def test_delete_cli_config_parcel(self):
        dns_parcel = DnsParcel(
            name="dns_parcel",
            match_all_vpn=Global[bool](value=True),
            dns_crypt=Global[bool](value=False),
            local_domain_bypass_enabled=Global[bool](value=False),
            umbrella_default=Global[bool](value=False),
            child_org_id=Global[str](value="1235"),
            dns_server_ip=Global[str](value="192.168.11.11"),
        )
        parcel_id = self.api.create_parcel(self.profile_id, dns_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, DnsParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, DnsParcel, parcel_id).payload

    def test_target_vpns_constraints(self):
        with pytest.raises(ValidationError):
            DnsParcel(
                name="dns_parcel",
                match_all_vpn=Global[bool](value=False),
                dns_crypt=Global[bool](value=False),
                local_domain_bypass_enabled=Global[bool](value=False),
                umbrella_default=Global[bool](value=False),
                child_org_id=Global[str](value="1235"),
                dns_server_ip=Global[str](value="192.168.11.11"),
            )
        with pytest.raises(ValidationError):
            DnsParcel(
                name="dns_parcel",
                match_all_vpn=Global[bool](value=True),
                dns_crypt=Global[bool](value=False),
                local_domain_bypass_enabled=Global[bool](value=False),
                umbrella_default=Global[bool](value=False),
                child_org_id=Global[str](value="1235"),
                dns_server_ip=Global[str](value="192.168.11.11"),
                target_vpns=[
                    TargetVpns(
                        uid=Global[str](value="2431234"),
                        vpns=Global[List[str]](value=["VPN_1"]),
                        umbrella_default=Global[bool](value=True),
                        local_domain_bypass_enabled=Global[bool](value=False),
                    )
                ],
            )

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)
