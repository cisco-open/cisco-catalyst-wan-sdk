# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .cflowd import CflowdParcel
from .node import NodeInfo

AnyNetworkHierarchyParcel = Annotated[
    Union[CflowdParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "CflowdParcel",
    "NodeInfo",
]


def __dir__() -> "List[str]":
    return list(__all__)
