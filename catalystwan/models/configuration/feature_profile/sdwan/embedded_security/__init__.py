# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import _ParcelBase

from .ngfirewall import PolicyParcel

AnyEmbeddedSecurityParcel = Annotated[
    Union[
        PolicyParcel,
        _ParcelBase,
    ],
    Field(discriminator="type_"),
]

__all__ = ("AnyEmbeddedSecurityParcel", "PolicyParcel")


def __dir__() -> "List[str]":
    return list(__all__)
