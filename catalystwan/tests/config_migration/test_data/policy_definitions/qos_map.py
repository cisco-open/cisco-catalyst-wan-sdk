# Copyright 2024 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.models.policy.definition.qos_map import QoSMapPolicyGetResponse


def create_qos_map_policy(name: str) -> QoSMapPolicyGetResponse:
    policy = QoSMapPolicyGetResponse(
        definition_id=uuid4(),
        name=name,
        description=f"{name} description",
        last_updated=datetime.now(),
        owner="tester",
        reference_count=0,
        references=[],
        is_activated_by_vsmart=False,
    )
    policy.add_scheduler(queue=1, class_map_ref=uuid4(), scheduling="llq", drops="red-drop", bandwidth=10)
    policy.add_scheduler(queue=2, class_map_ref=uuid4(), scheduling="wrr", drops="red-drop", bandwidth=20)
    policy.add_scheduler(queue=3, class_map_ref=uuid4(), scheduling="llq", drops="tail-drop", bandwidth=30)
    policy.add_scheduler(queue=4, class_map_ref=uuid4(), scheduling="wrr", drops="tail-drop", bandwidth=40)
    return policy
