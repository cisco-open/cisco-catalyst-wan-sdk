from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from catalystwan.models.policy.security import SecurityPolicyInfo


def create_security_policy(
    name, *, dns_uuid: Optional[UUID] = None, zbfw_uuid: Optional[UUID] = None
) -> SecurityPolicyInfo:
    spi = SecurityPolicyInfo(
        policy_id=uuid4(),
        policy_name=name,
        policy_version="",
        policy_description="Description",
        policy_type="feature",
        created_by="tester",
        created_on=datetime.now(),
        last_updated_by="tester",
        last_updated_on=datetime.now(),
        virtual_application_templates=[],
        supported_devices=[],
    )
    if dns_uuid:
        spi.add_dns_security(definition_id=dns_uuid)
    if zbfw_uuid:
        spi.add_zone_based_fw(definition_id=zbfw_uuid)
    return spi
