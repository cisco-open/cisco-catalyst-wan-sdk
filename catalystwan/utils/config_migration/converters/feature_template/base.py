from typing_extensions import Protocol

from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


class FeatureTemplateConverter(Protocol):
    def create_parcel(self, name: str, description: str, template_values: dict) -> AnyParcel:
        ...
