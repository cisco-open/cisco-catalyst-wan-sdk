from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .config import ConfigParcel
from .full_config import FullConfigParcel

AnyCliParcel = Annotated[
    Union[
        ConfigParcel,
        FullConfigParcel,
    ],
    Field(discriminator="type_"),
]


__all__ = ("AnyCliParcel", "ConfigParcel", "FullConfigParcel")


def __dir__() -> List[str]:
    return list(__all__)
