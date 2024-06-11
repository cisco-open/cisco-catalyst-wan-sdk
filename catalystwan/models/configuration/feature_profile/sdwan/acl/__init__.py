# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from .ipv4acl import Ipv4AclParcel
from .ipv6acl import Ipv6AclParcel

AnyAclParcel = Annotated[
    Union[Ipv4AclParcel, Ipv6AclParcel],
    Field(discriminator="type_"),
]
