import unittest
from ipaddress import IPv4Network
from random import randrange
from typing import List
from uuid import UUID, uuid4

from catalystwan.models.configuration.config_migration import ConvertResult, PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import NgfirewallParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.ngfirewall import (
    AppList,
    AppListFlat,
    DestinationDataPrefixList,
    DestinationFqdn,
    DestinationFqdnList,
    DestinationGeoLocation,
    DestinationGeoLocationList,
    DestinationIp,
    DestinationPort,
    DestinationPortList,
    DestinationScalableGroupTagList,
    Protocol,
    ProtocolNameList,
    ProtocolNameMatch,
    SourceDataPrefixList,
    SourceGeoLocation,
    SourceGeoLocationList,
    SourceIp,
    SourcePort,
    SourcePortList,
    SourceScalableGroupTagList,
)
from catalystwan.models.policy.definition.zone_based_firewall import (
    AdvancedInspectionProfileAction,
    ConnectionEventsAction,
    LogAction,
    ZoneBasedFWPolicy,
)
from catalystwan.models.policy.policy_definition import (
    AppListEntry,
    AppListFlatEntry,
    DestinationDataPrefixListEntry,
    DestinationFQDNEntry,
    DestinationFQDNListEntry,
    DestinationGeoLocationEntry,
    DestinationGeoLocationListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationPortListEntry,
    DestinationScalableGroupTagListEntry,
    ProtocolEntry,
    ProtocolNameEntry,
    ProtocolNameListEntry,
    Reference,
    RuleSetListEntry,
    SourceDataPrefixListEntry,
    SourceGeoLocationEntry,
    SourceGeoLocationListEntry,
    SourceIPEntry,
    SourcePortEntry,
    SourcePortListEntry,
    SourceScalableGroupTagListEntry,
)
from catalystwan.utils.config_migration.converters.policy.zone_based_firewall import (
    convert_sequence_actions,
    convert_sequence_match_entry,
    convert_zone_based_fw,
)


class TestSequenceMatchConverters(unittest.TestCase):
    def setUp(self) -> None:
        self._in_reference_uuid = [uuid4() for _ in range(randrange(1, 5))]
        self._convert_result = ConvertResult[NgfirewallParcel]()

    def _uuid_list_to_str_list(self, uuid_list: List[UUID]) -> List[str]:
        return list(map(str, uuid_list))

    def test_convert_source_data_prefix_list(self) -> None:
        in_ = SourceDataPrefixListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceDataPrefixList
        assert out_.source_data_prefix_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_data_prefix_list(self) -> None:
        in_ = DestinationDataPrefixListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationDataPrefixList
        assert out_.destination_data_prefix_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_fqdn_list(self) -> None:
        in_ = DestinationFQDNListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationFqdnList
        assert out_.destination_fqdn_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_geo_location_list(self) -> None:
        in_ = SourceGeoLocationListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceGeoLocationList
        assert out_.source_geo_location_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_geo_location_list(self) -> None:
        in_ = DestinationGeoLocationListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationGeoLocationList
        assert out_.destination_geo_location_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_port_list(self) -> None:
        in_ = SourcePortListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourcePortList
        assert out_.source_port_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_port_list(self) -> None:
        in_ = DestinationPortListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationPortList
        assert out_.destination_port_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_scalable_group_tag_list(self) -> None:
        in_ = SourceScalableGroupTagListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceScalableGroupTagList
        assert out_.source_scalable_group_tag_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_scalable_group_tag_list(self) -> None:
        in_ = DestinationScalableGroupTagListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationScalableGroupTagList
        assert out_.destination_scalable_group_tag_list.ref_id.value == self._uuid_list_to_str_list(
            self._in_reference_uuid
        )
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_protocol_name_list(self) -> None:
        in_ = ProtocolNameListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is ProtocolNameList
        assert out_.protocol_name_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_app_list(self) -> None:
        in_ = AppListEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is AppList
        assert out_.app_list.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_app_flat_list(self) -> None:
        in_ = AppListFlatEntry(ref=self._in_reference_uuid)
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is AppListFlat
        assert out_.app_list_flat.ref_id.value == self._uuid_list_to_str_list(self._in_reference_uuid)
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_ip_with_ip_networks(self) -> None:
        in_ = SourceIPEntry(value="10.0.0.0/24 192.168.0.0/16")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceIp
        assert out_.source_ip.ipv4_value.value == [IPv4Network("10.0.0.0/24"), IPv4Network("192.168.0.0/16")]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_ip_with_variable_name(self) -> None:
        in_ = SourceIPEntry(vip_variable_name="{{some_var}}")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceIp
        assert out_.source_ip.ipv4_value.value == "{{some_var}}"
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_dst_ip_with_ip_networks(self) -> None:
        in_ = DestinationIPEntry(value="10.0.0.0/24 192.168.0.0/16")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationIp
        assert out_.destination_ip.ipv4_value.value == [IPv4Network("10.0.0.0/24"), IPv4Network("192.168.0.0/16")]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_dst_ip_with_variable_name(self) -> None:
        in_ = DestinationIPEntry(vip_variable_name="{{some_var}}")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationIp
        assert out_.destination_ip.ipv4_value.value == "{{some_var}}"
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_port(self) -> None:
        in_ = DestinationPortEntry(value="1-1000 100 200")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationPort
        assert out_.destination_port.port_value.value == ["1-1000", "100", "200"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_port(self) -> None:
        in_ = SourcePortEntry(value="1-33 100 2400")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourcePort
        assert out_.source_port.port_value.value == ["1-33", "100", "2400"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_fqdn_entry(self) -> None:
        in_ = DestinationFQDNEntry(value="cisco.com sth.com")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationFqdn
        assert out_.destination_fqdn.fqdn_value.value == ["cisco.com", "sth.com"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_source_geo_location_entry(self) -> None:
        in_ = SourceGeoLocationEntry(value="AF KHM")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is SourceGeoLocation
        assert out_.source_geo_loacation.value == ["AF", "KHM"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_destination_geo_location_entry(self) -> None:
        in_ = DestinationGeoLocationEntry(value="AF")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is DestinationGeoLocation
        assert out_.destination_geo_loacation.value == ["AF"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_protocol_name_entry(self) -> None:
        in_ = ProtocolNameEntry(value="cisco-svcs cisco-net-mgmt cisco-sys")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is ProtocolNameMatch
        assert out_.protocol_name.value == ["cisco-svcs", "cisco-net-mgmt", "cisco-sys"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_protocol_entry(self) -> None:
        in_ = ProtocolEntry(value="1 2 3 4")
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert type(out_) is Protocol
        assert out_.protocol.value == ["1", "2", "3", "4"]
        assert self._convert_result.status == "complete"
        assert not self._convert_result.info

    def test_convert_unknown_entry(self) -> None:
        in_ = RuleSetListEntry(ref=[uuid4(), uuid4()])
        out_ = convert_sequence_match_entry(in_, self._convert_result)
        assert out_ is None
        assert self._convert_result.status == "partial"
        assert len(self._convert_result.info) == 1


class TestSequenceActionsConverters(unittest.TestCase):
    def setUp(self) -> None:
        self._convert_result = ConvertResult[NgfirewallParcel]()

    def test_convert_sequence_actions(self):
        in_actions = [
            LogAction(),
            ConnectionEventsAction(),
            AdvancedInspectionProfileAction(parameter=Reference(ref=uuid4())),
        ]

        out = convert_sequence_actions(in_actions, self._convert_result)

        assert len(out) == 3
        assert out[0].type.value == "log"
        assert out[1].type.value == "connectionEvents"
        assert out[2].type.value == "advancedInspectionProfile"
        assert self._convert_result.status == "complete"


class TestConvertZoneBasedFirewall(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_convert_zone_based_firewall(self):
        fw = ZoneBasedFWPolicy(name="fw1")
        fw.add_zone_pair(uuid4(), uuid4())
        rule = fw.add_ipv4_rule("rule1", "pass", log=True)
        rule.match_destination_port_list([uuid4(), uuid4()])
        fw.add_ipv4_rule("rule2", "pass", log=True)

        out = convert_zone_based_fw(fw, uuid4(), self.context)

        assert type(out) is ConvertResult
        assert out.status == "complete"
        assert not out.info
        assert type(out.output) is NgfirewallParcel
        assert out.output.parcel_name == "fw1"
        assert len(out.output.sequences) == 2
        assert out.output.sequences[0].sequence_name.value == "rule1"
        assert len(out.output.sequences[0].match.entries) == 1
        assert out.output.sequences[1].sequence_name.value == "rule2"
        assert len(out.output.sequences[1].match.entries) == 0
