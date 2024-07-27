from datetime import datetime
from uuid import uuid4

from catalystwan.models.policy.policy import DNSSecurityAssemblyItem, ZoneBasedFWAssemblyItem
from catalystwan.models.policy.security import SecurityPolicyDefinition, SecurityPolicyInfo


def create_security_policy(name) -> SecurityPolicyInfo:
    dns_uuid = uuid4()
    zbfw_uuid = uuid4()

    return SecurityPolicyInfo(
        policy_id=uuid4(),
        policy_name=name,
        policy_version="",
        policy_description="Description",
        policy_type="feature",
        created_by="tester",
        created_on=datetime.now(),
        last_updated_by="tester",
        last_updated_on=datetime.now(),
        policy_definition=SecurityPolicyDefinition(
            assembly=[DNSSecurityAssemblyItem(definition_id=dns_uuid), ZoneBasedFWAssemblyItem(definition_id=zbfw_uuid)]
        ),
        virtual_application_templates=[],
        supported_devices=[],
    )
