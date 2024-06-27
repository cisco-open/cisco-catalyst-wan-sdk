# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .ngfirewall import NgfirewallParcel
from .policy import PolicyParcel, PolicySettings

AnyEmbeddedSecurityParcel = Annotated[
    Union[
        PolicyParcel,
        NgfirewallParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = ("AnyEmbeddedSecurityParcel", "PolicyParcel", "PolicySettings", "NgfirewallParcel")


def __dir__() -> "List[str]":
    return list(__all__)
