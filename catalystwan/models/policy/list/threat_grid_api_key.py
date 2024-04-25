# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo

ServerRegion = Literal["nam", "eur"]


class ThreatGridApiKeyEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    region: ServerRegion
    api_key: str = Field(validation_alias="apikey", serialization_alias="apikey")


class ThreatGridApiKeyList(PolicyListBase):
    type: Literal["threatGridApiKey"] = "threatGridApiKey"
    entries: List[ThreatGridApiKeyEntry] = []

    def add_entry(self, api_key: str, region: ServerRegion) -> None:
        entry = ThreatGridApiKeyEntry(api_key=api_key, region=region)
        self.entries.append(entry)


class ThreatGridApiKeyListEditPayload(ThreatGridApiKeyList, PolicyListId):
    pass


class ThreatGridApiKeyListInfo(ThreatGridApiKeyList, PolicyListInfo):
    pass
