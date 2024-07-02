# Copyright 2024 Cisco Systems, Inc. and its affiliates
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from catalystwan.models.configuration.config_migration import ConvertResult
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


class FTConverter(ABC):
    """Feature Template Converter abstract base class."""

    supported_template_types: Tuple = tuple()

    def __init__(self):
        self._convert_result = ConvertResult[AnyParcel]()

    @abstractmethod
    def create_parcel(self, name: str, description: str, template_values: dict) -> Optional[AnyParcel]:
        """This function can modify status and info attributes of the conversion process."""
        ...

    def convert(self, name: str, description: str, template_values: dict) -> ConvertResult[AnyParcel]:
        if not self.supported_template_types:
            self._convert_result.update_status(
                "unsupported", "supported_template_types must be defined in the subclass"
            )
            return self._convert_result

        try:
            parcel = self.create_parcel(name, description, template_values)
            self._convert_result.output = parcel
        except CatalystwanConverterCantConvertException as e:
            self._convert_result.update_status("failed", str(e))
        return self._convert_result
