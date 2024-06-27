from typing import Callable, Mapping, Union

from catalystwan.api.feature_profile_api import (
    CliFeatureProfileAPI,
    DnsSecurityFeatureProfileAPI,
    EmbeddedSecurityFeatureProfileAPI,
    OtherFeatureProfileAPI,
    PolicyObjectFeatureProfileAPI,
    ServiceFeatureProfileAPI,
    SystemFeatureProfileAPI,
    TopologyFeatureProfileAPI,
    TransportFeatureProfileAPI,
)
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession

FEATURE_PROFILE_API_MAPPING: Mapping[ProfileType, Callable] = {
    "system": SystemFeatureProfileAPI,
    "other": OtherFeatureProfileAPI,
    "policy-object": PolicyObjectFeatureProfileAPI,
    "service": ServiceFeatureProfileAPI,
    "transport": TransportFeatureProfileAPI,
    "cli": CliFeatureProfileAPI,
    "topology": TopologyFeatureProfileAPI,
    "dns-security": DnsSecurityFeatureProfileAPI,
    "embedded-security": EmbeddedSecurityFeatureProfileAPI,
}

FeatureProfile = Union[
    SystemFeatureProfileAPI,
    OtherFeatureProfileAPI,
    PolicyObjectFeatureProfileAPI,
    ServiceFeatureProfileAPI,
    TransportFeatureProfileAPI,
    CliFeatureProfileAPI,
]


class FeatureProfileAPIFactory:
    """
    Factory class for creating FeatureProfileAPI instances.
    """

    @staticmethod
    def get_api(profile_type: ProfileType, session: ManagerSession) -> FeatureProfile:
        """
        Get the appropriate FeatureProfileAPI instance based on the profile type.

        Args:
            profile_type (ProfileType): The type of the feature profile.
            session (ManagerSession): The session object.

        Returns:
            FeatureProfileAPI: The appropriate FeatureProfileAPI instance.
        """
        api_class = FEATURE_PROFILE_API_MAPPING.get(profile_type)
        if api_class is None:
            raise ValueError(f"Invalid profile type: {profile_type}")
        return api_class(session)
