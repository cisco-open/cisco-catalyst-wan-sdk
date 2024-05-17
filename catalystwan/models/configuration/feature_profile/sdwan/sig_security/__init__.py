from typing import List

from pydantic import Field
from typing_extensions import Annotated

from .sig_security import SIGParcel

AnySIGSecurityParcel = Annotated[
    SIGParcel,
    Field(discriminator="type_"),
]


__all__ = ("SIGParcel",)


def __dir__() -> List[str]:
    return list(__all__)
