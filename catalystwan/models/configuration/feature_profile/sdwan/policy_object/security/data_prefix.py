# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network
from typing import List, Literal

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry, as_global


class SecurityDataPrefixEntry(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    ip_prefix: Global[IPv4Network] = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")


class SecurityDataPrefixParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["security-data-ip-prefix"] = Field(default="security-data-ip-prefix", exclude=True)
    entries: List[SecurityDataPrefixEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ip_prefix: IPv4Network):
        self.entries.append(SecurityDataPrefixEntry(ip_prefix=as_global(ip_prefix)))
