# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import WellKnownBGPCommunities
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class CommunityListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    community: str = Field(examples=["1000:10000", "internet", "local-AS"])


class ExtendedCommunityListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    community: str = Field(examples=["soo 1.2.3.4:1000", "rt 10:100"])


class CommunityListBase(PolicyListBase):
    entries: List[CommunityListEntry] = []

    def add_well_known_community(self, community: WellKnownBGPCommunities) -> None:
        self._add_entry(CommunityListEntry(community=community))

    def add_community(self, as_number: int, community_number: int) -> None:
        self._add_entry(CommunityListEntry(community=f"{as_number}:{community_number}"))


class CommunityList(CommunityListBase):
    type: Literal["community"] = "community"


class CommunityListEditPayload(CommunityList, PolicyListId):
    pass


class CommunityListInfo(CommunityList, PolicyListInfo):
    pass


class ExpandedCommunityList(CommunityListBase):
    type: Literal["expandedCommunity"] = "expandedCommunity"


class ExpandedCommunityListEditPayload(ExpandedCommunityList, PolicyListId):
    pass


class ExpandedCommunityListInfo(ExpandedCommunityList, PolicyListInfo):
    pass


class ExtendedCommunityList(PolicyListBase):
    entries: List[ExtendedCommunityListEntry] = []
    type: Literal["extCommunity"] = "extCommunity"

    def add_site_of_origin_community(
        self, ip_address: Union[IPv4Address, IPv6Address], port: int, name: Optional[str] = None
    ):
        entry = f"soo {ip_address}:{port}"
        self.entries.append(ExtendedCommunityListEntry(community=self._append_name(entry, name)))

    def add_route_target_community(self, as_number: int, community_number: int, name: Optional[str] = None):
        entry = f"rt {as_number}:{community_number}"
        self.entries.append(ExtendedCommunityListEntry(community=self._append_name(entry, name)))

    def _append_name(self, entry: str, name: Optional[str] = None) -> str:
        if not name:
            return entry

        return f"{name} {entry}"


class ExtendedCommunityListEditPayload(ExtendedCommunityList, PolicyListId):
    pass


class ExtendedCommunityListInfo(ExtendedCommunityList, PolicyListInfo):
    pass
