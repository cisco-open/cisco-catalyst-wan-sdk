# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Optional, Tuple

from catalystwan.models.configuration.config_migration import ConvertStatus
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


class FTConverter:
    """Feature Template Converter base class."""

    supported_template_types: Tuple = tuple()

    def __init__(self) -> None:
        if not self.supported_template_types:
            raise ValueError("supported_template_types must be defined in the subclass")
        self._status: ConvertStatus = "complete"
        self._info: List[str] = []

    def create_parcel(self, name: str, description: str, template_values: dict) -> Optional[AnyParcel]:
        """This function can modify status and info attributes of the conversion process."""
        raise NotImplementedError("create_parcel method must be implemented")

    @property
    def status(self) -> ConvertStatus:
        return self._status

    @status.setter
    def status(self, value: ConvertStatus) -> None:
        self._status = value

    @property
    def info(self) -> List[str]:
        return self._info

    @info.setter
    def info(self, value: str) -> None:
        self._info.append(value)
