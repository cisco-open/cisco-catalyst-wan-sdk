# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Optional, Tuple

from catalystwan.models.configuration.config_migration import ConvertResult
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


class FTConverter:
    """Feature Template Converter base class."""

    supported_template_types: Tuple = tuple()

    def __init__(self) -> None:
        if not self.supported_template_types:
            raise ValueError("supported_template_types must be defined in the subclass")
        self._convert_result = ConvertResult[AnyParcel]()

    def create_parcel(self, name: str, description: str, template_values: dict) -> Optional[AnyParcel]:
        """This function can modify status and info attributes of the conversion process."""
        raise NotImplementedError("create_parcel method must be implemented")

    def convert(self, name: str, description: str, template_values: dict) -> ConvertResult[AnyParcel]:
        """Converts the template values into a parcel."""
        parcel = self.create_parcel(name, description, template_values)
        self._convert_result.output = parcel
        return self._convert_result
