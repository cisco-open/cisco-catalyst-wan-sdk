# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from typing import Optional
from uuid import UUID

from catalystwan.integration_tests.base import IS_API_20_12, TestCaseBase
from catalystwan.models.configuration.network_hierarchy.cflowd import CflowdParcel


@unittest.skipIf(IS_API_20_12, "cflowd is not supported in 20.12")
class TestCflowd(TestCaseBase):
    parcel_id: Optional[UUID] = None
    global_node_id: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        nodes = cls.session.endpoints.network_hierarchy.list_nodes()
        for node in nodes:
            if node.data.label == "GLOBAL":
                cls.global_node_id = UUID(node.id)
                return
        raise ValueError("Global node not found")

    def test_create_cflowd(self):
        # Arrange
        protocol = "ipv4"
        active_timeout = 1000
        inactive_timeout = 3000
        refresh_time = 5000
        sampling_interval = 6000
        collect_tos = False
        collect_dscp_output = True
        vpn_id = 50
        address = "10.0.2.3"
        port = 9900
        export_spread = True
        bfd_metrics_export = True
        export_interval = 1000
        cflowd = CflowdParcel()
        cflowd.add_collector(
            address=address,
            bfd_metrics_export=bfd_metrics_export,
            export_interval=export_interval,
            export_spread=export_spread,
            udp_port=port,
            vpn_id=vpn_id,
        )
        cflowd.set_customized_ipv4_record_fields(collect_tos=collect_tos, collect_dscp_output=collect_dscp_output)
        cflowd.set_flow(
            active_timeout=active_timeout,
            inactive_timeout=inactive_timeout,
            refresh_time=refresh_time,
            sampling_interval=sampling_interval,
        )
        cflowd.set_protocol(protocol)
        # Act
        self.parcel_id = self.session.endpoints.network_hierarchy.create_cflowd(self.global_node_id, cflowd).id
        parcel = (
            self.session.endpoints.network_hierarchy.get_cflowd(self.global_node_id)
            .find(parcel_id=self.parcel_id)
            .payload
        )
        # Assert
        assert parcel.protocol.value == protocol
        assert parcel.flow_active_timeout.value == active_timeout
        assert parcel.flow_inactive_timeout.value == inactive_timeout
        assert parcel.flow_refresh_time.value == refresh_time
        assert parcel.flow_sampling_interval.value == sampling_interval
        assert parcel.customized_ipv4_record_fields.collect_dscp_output.value == collect_dscp_output
        assert parcel.customized_ipv4_record_fields.collect_tos.value == collect_tos
        assert parcel.collectors[0].vpn_id.value == vpn_id
        assert parcel.collectors[0].address.value == address
        assert parcel.collectors[0].udp_port.value == port
        assert parcel.collectors[0].bfd_metrics_export.value == bfd_metrics_export
        assert parcel.collectors[0].export_interval.value == export_interval
        assert parcel.collectors[0].export_spread.value == export_spread

    def tearDown(self) -> None:
        if self.parcel_id:
            self.session.endpoints.network_hierarchy.delete_cflowd(self.global_node_id, self.parcel_id)
        super().tearDown()
