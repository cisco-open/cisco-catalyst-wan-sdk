from uuid import uuid4

from catalystwan.models.policy.security import SecurityPolicy


def create_security_policy(name) -> SecurityPolicy:
    return SecurityPolicy(
        policy_id=uuid4(),
        policy_name=name,
        policy_description="Description",
        policy_type="feature",
    )
