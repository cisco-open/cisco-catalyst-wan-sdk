import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.policy.definition.qos_map import QoSMapPolicy
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestQosMapConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()
        self.uuid = uuid4()

    def test_convert_qos_map_policy(self):
        policy = QoSMapPolicy(name="policy1", description="desc1")

        policy.add_scheduler(queue=1, class_map_ref=uuid4(), scheduling="llq", drops="red-drop", bandwidth=10)
        policy.add_scheduler(queue=2, class_map_ref=uuid4(), scheduling="wrr", drops="red-drop", bandwidth=20)
        policy.add_scheduler(queue=3, class_map_ref=uuid4(), scheduling="llq", drops="tail-drop", bandwidth=30)
        policy.add_scheduler(queue=4, class_map_ref=uuid4(), scheduling="wrr", drops="tail-drop", bandwidth=40)

        convert_result = convert(policy, self.uuid, self.context)
        parcel = convert_result.output

        assert convert_result.status == "complete"
        assert parcel.target is None
        assert len(parcel.qos_map.qos_schedulers) == 5
        assert len(self.context.qos_map_residues[self.uuid]) == 5
        assert parcel.qos_map.qos_schedulers[0].class_map_ref is None

        for i in range(1, 5):
            source_scheduler = policy.definition.qos_schedulers[i]
            target_scheduler = parcel.qos_map.qos_schedulers[i]
            assert target_scheduler.bandwidth_percent.value == str(source_scheduler.bandwidth_percent)
            assert target_scheduler.class_map_ref.ref_id.value == str(source_scheduler.class_map_ref)
            assert target_scheduler.drops.value == source_scheduler.drops
            assert target_scheduler.queue.value == str(source_scheduler.queue)
            assert target_scheduler.scheduling.value == source_scheduler.scheduling
            assert self.context.qos_map_residues[self.uuid][i].burst == source_scheduler.burst
            assert self.context.qos_map_residues[self.uuid][i].temp_key_values == source_scheduler.temp_key_values
            assert self.context.qos_map_residues[self.uuid][i].buffer_percent == source_scheduler.buffer_percent
