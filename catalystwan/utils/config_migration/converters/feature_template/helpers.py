# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Optional, Type, TypeVar, Union

from catalystwan.api.configuration_groups.parcel import Global, OptionType, Variable

T = TypeVar("T")


def create_dict_without_none(**kwargs) -> dict:
    """Create a dictionary without None values.
    This speeds up the converting because we don't need to check for None values.
    If pydantic model input doesn't have a key:value pair, it will use a default value."""
    return {k: v for k, v in kwargs.items() if v is not None}


def return_global_variable_or_none(
    data: dict, key: str, global_type: Type[Global[T]]
) -> Optional[Union[Global[T], Variable]]:
    """Return a Global or Variable object from the data dictionary or None if the key doesn't exist."""
    value = data.get(key)
    if value is None:
        return None
    return global_type(value=value.value) if value.option_type == OptionType.GLOBAL else value
