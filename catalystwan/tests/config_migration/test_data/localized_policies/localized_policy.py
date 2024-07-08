# Copyright 2024 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.models.policy.localized import LocalizedPolicyInfo, LocalizedPolicySettings


def create_localized_policy_info(name: str) -> LocalizedPolicyInfo:
    policy = LocalizedPolicyInfo(
        policy_type="feature",
        policy_id=uuid4(),
        policy_name=name,
        created_by="tester",
        created_on=datetime.now(),
        last_updated_by="tester",
        last_updated_on=datetime.now(),
        policy_version=None,
    )
    settings = LocalizedPolicySettings(
        flow_visibility=True,
        flow_visibility_ipv6=True,
        app_visibility=True,
        app_visibility_ipv6=True,
        cloud_qos=True,
        cloud_qos_service_side=True,
        implicit_acl_logging=True,
        log_frequency=10,
        ip_visibility_cache_entries=100,
        ip_v6_visibility_cache_entries=200,
    )
    policy.set_definition([], settings)
    return policy
