# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.network_hierarchy.cflowd import CflowdParcel
from catalystwan.models.policy.definition.cflowd import (
    CflowdDefinition,
    CflowdPolicy,
    Collector,
    CustomizedIpv4RecordFields,
    IpProtocol,
)
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestCflowdConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_cflowd_conversion(self):
        # Arrange
        protocol: IpProtocol = "ipv4"
        flow_active_timeout = 1000
        flow_inactive_timeout = 3000
        template_refresh = 5000
        flow_sampling_interval = 6000
        collect_tos = False
        collect_dscp_output = True
        vpn_id = 50
        address = "0::"
        port = 9900
        transport = "transport_udp"
        source_interface = "eth0"
        export_spread = None
        bfd_metrics_export = "enable"
        export_interval = 1000
        collector = Collector(
            vpn=vpn_id,
            address=address,
            port=port,
            transport=transport,
            source_interface=source_interface,
            export_spread=export_spread,
            bfd_metrics_export=bfd_metrics_export,
            export_interval=export_interval,
        )
        customized_ipv4_record_fields = CustomizedIpv4RecordFields(
            collect_tos=collect_tos,
            collect_dscp_output=collect_dscp_output,
        )
        definition = CflowdDefinition(
            protocol=protocol,
            flow_active_timeout=flow_active_timeout,
            flow_inactive_timeout=flow_inactive_timeout,
            template_refresh=template_refresh,
            flow_sampling_interval=flow_sampling_interval,
            customized_ipv4_record_fields=customized_ipv4_record_fields,
            collectors=[collector],
        )
        cflowd = CflowdPolicy(
            name="cflowd_policy",
            description="cflowd description",
            definition=definition,
        )
        uuid = uuid4()
        self.context.activated_centralized_policy_item_ids = set([uuid])
        # Act
        convert(cflowd, uuid, context=self.context)
        parcel = self.context.cflowd
        # Assert
        assert isinstance(parcel, CflowdParcel)
        assert parcel.protocol.value == protocol
        assert parcel.flow_active_timeout.value == flow_active_timeout
        assert parcel.flow_inactive_timeout.value == flow_inactive_timeout
        assert parcel.flow_refresh_time.value == template_refresh
        assert parcel.flow_sampling_interval.value == flow_sampling_interval
        assert parcel.customized_ipv4_record_fields.collect_dscp_output.value == collect_dscp_output
        assert parcel.customized_ipv4_record_fields.collect_tos.value == collect_tos
        assert parcel.collectors[0].vpn_id.value == vpn_id
        assert parcel.collectors[0].address.value == address
        assert parcel.collectors[0].udp_port.value == port
        assert parcel.collectors[0].bfd_metrics_export.value == (bfd_metrics_export is not None)
        assert parcel.collectors[0].export_interval.value == export_interval
        assert parcel.collectors[0].export_spread.value == (export_spread is not None)
