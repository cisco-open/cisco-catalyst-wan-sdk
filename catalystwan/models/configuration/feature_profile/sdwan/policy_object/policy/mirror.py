# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field
from pydantic.networks import IPvAnyAddress

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class MirrorEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    remote_dest_ip: Global[str] = Field(validation_alias="remoteDestIp", serialization_alias="remoteDestIp")
    source_ip: Global[str] = Field(validation_alias="sourceIp", serialization_alias="sourceIp")


class MirrorParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["mirror"] = Field(default="mirror", exclude=True)
    entries: List[MirrorEntry] = Field(
        default=[], validation_alias=AliasPath("data", "entries"), min_length=1, max_length=1
    )

    @classmethod
    def create(cls, remote_dest_ip: IPvAnyAddress, source_ip: IPvAnyAddress, *args, **kwargs):
        entry = MirrorEntry(remote_dest_ip=as_global(str(remote_dest_ip)), source_ip=as_global(str(source_ip)))
        return cls(entries=[entry], *args, **kwargs)
