# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class ExtendedCommunityEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    extended_community: Global[str] = Field(serialization_alias="extCommunity", validation_alias="extCommunity")

    @classmethod
    def from_string(cls, entry: str):
        return cls(extended_community=as_global(entry))


class ExtendedCommunityParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["ext-community"] = Field(default="ext-community", exclude=True)
    entries: List[ExtendedCommunityEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_site_of_origin_community(self, ip_address: IPv4Address, port: int):
        entry = f"soo {ip_address}:{port}"
        self._add_community(entry)

    def add_route_target_community(self, as_number: int, community_number: int):
        entry = f"rt {as_number}:{community_number}"
        self._add_community(entry)

    def _add_community(self, exteneded_community: str):
        self.entries.append(ExtendedCommunityEntry.from_string(exteneded_community))
