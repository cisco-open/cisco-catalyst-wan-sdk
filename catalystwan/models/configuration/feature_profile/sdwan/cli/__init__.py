from typing import List

from pydantic import Field
from typing_extensions import Annotated

from .config import ConfigParcel

AnyCliParcel = Annotated[
    ConfigParcel,
    Field(discriminator="type_"),
]


__all__ = ("ConfigParcel",)


def __dir__() -> List[str]:
    return list(__all__)
