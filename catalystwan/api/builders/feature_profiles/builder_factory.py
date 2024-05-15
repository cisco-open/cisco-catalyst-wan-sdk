from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Mapping, Union

from catalystwan.api.builders.feature_profiles.cli import CliFeatureProfileBuilder
from catalystwan.api.builders.feature_profiles.other import OtherFeatureProfileBuilder
from catalystwan.api.builders.feature_profiles.service import ServiceFeatureProfileBuilder
from catalystwan.api.builders.feature_profiles.system import SystemFeatureProfileBuilder
from catalystwan.api.builders.feature_profiles.transport import TransportAndManagementProfileBuilder
from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.feature_profile.common import ProfileType

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

FeatureProfileBuilder = Union[
    ServiceFeatureProfileBuilder,
    SystemFeatureProfileBuilder,
    OtherFeatureProfileBuilder,
    TransportAndManagementProfileBuilder,
    CliFeatureProfileBuilder,
]

BUILDER_MAPPING: Mapping[ProfileType, Callable] = {
    "service": ServiceFeatureProfileBuilder,
    "system": SystemFeatureProfileBuilder,
    "other": OtherFeatureProfileBuilder,
    "transport": TransportAndManagementProfileBuilder,
    "cli": CliFeatureProfileBuilder,
}


class FeatureProfileBuilderFactory:
    def __init__(self, session: ManagerSession):
        self.session = session

    def create_builder(self, profile_type: ProfileType) -> FeatureProfileBuilder:
        """
        Creates a builder for the specified feature profile.

        Args:
            feature_profile_name (str): The name of the feature profile.

        Returns:
            FeatureProfileBuilder: The builder for the specified feature profile.

        Raises:
            CatalystwanException: If the feature profile is not found or has an unsupported type.
        """
        if profile_type not in BUILDER_MAPPING:
            raise CatalystwanException(f"Unsupported builder for type {profile_type}")
        return BUILDER_MAPPING[profile_type](self.session)
