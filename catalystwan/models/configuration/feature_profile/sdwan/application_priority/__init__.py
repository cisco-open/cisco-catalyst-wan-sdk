# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from .policy_settings import PolicySettingsParcel

AnyApplicationPriorityParcel = PolicySettingsParcel

# AnyApplicationPriorityParcel = Annotated[
#    Union[
#        PolicySettingsParcel,
#        PolicyParcel,
#    ],
#    Field(discriminator="type_"),
# ]

__all__ = ("AnyApplicationPriorityParcel", "PolicySettignsParcel")


def __dir__() -> "List[str]":
    return list(__all__)
