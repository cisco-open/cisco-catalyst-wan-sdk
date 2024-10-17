# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class MediaProfileList(PolicyListBase):
    type: Literal["mediaprofile"] = "mediaprofile"


class MediaProfileListEditPayload(MediaProfileList, PolicyListId):
    pass


class MediaProfileListInfo(MediaProfileList, PolicyListInfo):
    pass
