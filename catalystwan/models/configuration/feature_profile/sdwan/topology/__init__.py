from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel

AnyTopologyParcel = Annotated[
    Union[
        MeshParcel,
        HubSpokeParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = [
    "AnyTopologyParcel",
    "HubSpokeParcel","MeshParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
