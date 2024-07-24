# Copyright 2024 Cisco Systems, Inc. and its affiliates
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, Union

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global
from catalystwan.models.configuration.config_migration import ConvertResult
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.utils import convert_interface_name


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
        except (CatalystwanConverterCantConvertException, AttributeError, LookupError, TypeError, ValueError) as e:
            self._convert_result.update_status("failed", str(e.__class__.__name__ + ": " + str(e)))
        return self._convert_result

    def parse_interface_name(self, data: Dict) -> Union[Global[str], Variable]:
        if_name = data.get("if_name")
        if isinstance(if_name, Variable):
            return if_name
        elif isinstance(if_name, Global):
            converted_if_name = convert_interface_name(if_name.value)
            if converted_if_name != if_name.value:
                self._convert_result.update_status(
                    "partial", f"Converted interface name: {if_name.value} -> {converted_if_name}"
                )
            return as_global(converted_if_name)
        raise CatalystwanConverterCantConvertException("Interface name is required")
