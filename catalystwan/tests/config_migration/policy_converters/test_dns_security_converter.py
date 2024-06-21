import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.dns_security.dns import DnsParcel
from catalystwan.models.policy.definition.dns_security import DnsSecurityDefinition, DnsSecurityPolicy, TargetVpn
from catalystwan.models.policy.policy_definition import Reference
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestDnsSecurityConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()
        self.context.lan_vpn_map = {"vpn1": 1, "vpn2": 2, "vpn6": 6, "vpn7": 7, "vpn8": 7}
        self.uuid = uuid4()
        self.umbrella_data = Reference(ref=uuid4())
        self.local_domain_ref = Reference(ref=uuid4())

    def test_policy_with_match_all_vpns_and_umbrella_default(self):
        policy = DnsSecurityPolicy(
            name="test1",
            description="destription 1",
            definition=DnsSecurityDefinition(
                umbrella_data=self.umbrella_data,
                match_all_vpn=True,
                umbrella_default=True,
            ),
        )

        parcel = convert(policy, self.uuid, self.context).output

        assert isinstance(parcel, DnsParcel)
        assert parcel.parcel_name == "test1"
        assert parcel.parcel_description == "destription 1"
        assert parcel.child_org_id is None
        assert parcel.dns_crypt.value is True
        assert parcel.dns_server_ip is None
        assert parcel.local_domain_bypass_enabled is None
        assert parcel.local_domain_bypass_list is None
        assert parcel.match_all_vpn.value is True
        assert parcel.target_vpns is None
        assert parcel.umbrella_default.value is True

        assert len(self.context.dns_security_umbrella_data) == 1
        assert self.context.dns_security_umbrella_data[self.uuid] == self.umbrella_data.ref

    def test_policy_with_match_all_vpns_and_dns_server_ip(self):
        policy = DnsSecurityPolicy(
            name="test2",
            definition=DnsSecurityDefinition.create_match_all_vpns_config(
                child_org_id=12345,
                umbrella_data=self.umbrella_data,
                umbrella_default=False,
                dns_server_ip="1.2.3.4",
                dns_crypt=False,
            ),
        )

        parcel = convert(policy, self.uuid, self.context).output

        assert isinstance(parcel, DnsParcel)
        assert parcel.parcel_name == "test2"
        assert parcel.child_org_id.value == str(12345)
        assert parcel.dns_crypt.value is False
        assert parcel.dns_server_ip.value == "1.2.3.4"
        assert parcel.local_domain_bypass_enabled.value is False
        assert parcel.local_domain_bypass_list is None
        assert parcel.match_all_vpn.value is True
        assert parcel.target_vpns is None
        assert parcel.umbrella_default.value is False

        assert len(self.context.dns_security_umbrella_data) == 1
        assert self.context.dns_security_umbrella_data[self.uuid] == self.umbrella_data.ref

    def test_policy_with_match_all_vpns_and_local_domain_bypass_list(self):
        policy = DnsSecurityPolicy(
            name="test3",
            definition=DnsSecurityDefinition.create_match_all_vpns_config(
                child_org_id=65645645,
                umbrella_data=self.umbrella_data,
                umbrella_default=False,
                dns_server_ip="1.2.3.4",
                dns_crypt=False,
                local_domain_bypass_list=self.local_domain_ref,
            ),
        )

        parcel = convert(policy, self.uuid, self.context).output

        assert isinstance(parcel, DnsParcel)
        assert parcel.parcel_name == "test3"
        assert parcel.child_org_id.value == str(65645645)
        assert parcel.dns_crypt.value is False
        assert parcel.dns_server_ip.value == "1.2.3.4"
        assert parcel.local_domain_bypass_enabled.value is True
        assert parcel.local_domain_bypass_list.ref_id.value == str(self.local_domain_ref.ref)
        assert parcel.match_all_vpn.value is True
        assert parcel.target_vpns is None
        assert parcel.umbrella_default.value is False

        assert len(self.context.dns_security_umbrella_data) == 1
        assert self.context.dns_security_umbrella_data[self.uuid] == self.umbrella_data.ref

    def test_policy_with_vpn_list(self):
        policy = DnsSecurityPolicy(
            name="test4",
            definition=DnsSecurityDefinition.create_match_custom_vpns_config(
                umbrella_data=self.umbrella_data,
                dns_crypt=True,
                local_domain_bypass_list=self.local_domain_ref,
                target_vpns=[
                    TargetVpn(vpns=[1, 2], umbrella_default=True, local_domain_bypass_enabled=False, uid=100000),
                    TargetVpn(vpns=[6, 7], umbrella_default=True, uid=200000),
                ],
            ),
        )

        parcel = convert(policy, self.uuid, self.context).output

        assert isinstance(parcel, DnsParcel)
        assert parcel.parcel_name == "test4"
        assert parcel.child_org_id is None
        assert parcel.dns_crypt.value is True
        assert parcel.dns_server_ip is None
        assert parcel.local_domain_bypass_enabled is None
        assert parcel.local_domain_bypass_list.ref_id.value == str(self.local_domain_ref.ref)
        assert parcel.match_all_vpn.value is False
        assert parcel.umbrella_default is None

        assert len(parcel.target_vpns) == 2
        assert parcel.target_vpns[0].local_domain_bypass_enabled.value is False
        assert parcel.target_vpns[0].umbrella_default.value is True
        assert parcel.target_vpns[0].uid.value == str(100000)
        assert parcel.target_vpns[0].dns_server_ip is None
        assert parcel.target_vpns[0].vpns.value == ["vpn1", "vpn2"]

        assert parcel.target_vpns[1].local_domain_bypass_enabled.value is True
        assert parcel.target_vpns[1].umbrella_default.value is True
        assert parcel.target_vpns[1].uid.value == str(200000)
        assert parcel.target_vpns[1].dns_server_ip is None
        assert parcel.target_vpns[1].vpns.value == ["vpn6", "vpn7", "vpn8"]

        assert len(self.context.dns_security_umbrella_data) == 1
        assert self.context.dns_security_umbrella_data[self.uuid] == self.umbrella_data.ref
