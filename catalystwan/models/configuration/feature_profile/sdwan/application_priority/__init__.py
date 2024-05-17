# Copyright 2024 Cisco Systems, Inc. and its affiliates


from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy_settings import Cflowd, PolicySettingsParcel
from .qos_policy import QosMap, QosPolicyParcel, QosSchedulers, Target

AnyApplicationPriorityParcel = Annotated[
    Union[
        PolicySettingsParcel,
        QosPolicyParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AnyApplicationPriorityParcel",
    "PolicySettingsParcel",
    "QosPolicyParcel",
    "Target",
    "QosMap",
    "QosSchedulers",
    "Cflowd",
)


def __dir__() -> "List[str]":
    return list(__all__)
