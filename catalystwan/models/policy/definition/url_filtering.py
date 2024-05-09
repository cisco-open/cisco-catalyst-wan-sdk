# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.models.common import PolicyModeType, VpnId
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
)

BLOCK_PAGE_CONTENT_HEADER = "Access to the requested page has been denied."

BlockPageAction = Literal["text", "redirectUrl"]
UrlFilteringAlerts = Literal["blacklist", "whitelist", "categories-reputation"]
WebReputation = Literal["low-risk", "moderate-risk", "high-risk", "suspicious", "trustworthy"]
WebCategoriesAction = Literal["allow", "block"]
WebCategories = Literal[
    "abused-drugs",
    "abortion",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "games",
    "gambling",
    "financial-services",
    "fashion-and-beauty",
    "entertainment-and-arts",
    "educational-institutions",
    "dynamic-content",
    "dead-sites",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "government",
    "gross",
    "hacking",
    "hate-and-racism",
    "health-and-medicine",
    "home",
    "hunting-and-fishing",
    "illegal",
    "image-and-video-search",
    "individual-stock-advice-and-tools",
    "internet-communications",
    "internet-portals",
    "job-search",
    "keyloggers-and-monitoring",
    "kids",
    "legal",
    "local-information",
    "malware-sites",
    "marijuana",
    "p2p",
    "parked-sites",
    "pay-to-surf",
    "personal-sites-and-blogs",
    "philosophy-and-political-advocacy",
    "phishing-and-other-frauds",
    "private-ip-addresses",
    "proxy-avoid-and-anonymizers",
    "questionable",
    "real-estate",
    "recreation-and-hobbies",
    "reference-and-research",
    "religion",
    "search-engines",
    "sex-education",
    "shareware-and-freeware",
    "shopping",
    "social-network",
    "society",
    "sports",
    "spam-urls",
    "spyware-and-adware",
    "streaming-media",
    "swimsuits-and-intimate-apparel",
    "training-and-tools",
    "translation",
    "travel",
    "uncategorized",
    "unconfirmed-spam-sources",
    "violence",
    "weapons",
    "web-advertisements",
    "web-based-email",
    "web-hosting",
    "open-http-proxies",
    "online-personal-storage",
    "online-greeting-cards",
    "nudity",
    "news-and-media",
    "music",
    "motor-vehicles",
    "military",
]


class UrlFilteringDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    web_categories_action: WebCategoriesAction = Field(
        validation_alias="webCategoriesAction", serialization_alias="webCategoriesAction"
    )
    web_categories: List[WebCategories] = Field(validation_alias="webCategories", serialization_alias="webCategories")
    web_reputation: WebReputation = Field(validation_alias="webReputation", serialization_alias="webReputation")
    url_white_list: Optional[Reference] = Field(
        default=None, validation_alias="urlWhiteList", serialization_alias="urlWhiteList"
    )
    url_black_list: Optional[Reference] = Field(
        default=None, validation_alias="urlBlackList", serialization_alias="urlBlackList"
    )
    block_page_action: BlockPageAction = Field(
        validation_alias="blockPageAction", serialization_alias="blockPageAction"
    )
    block_page_contents: str = Field(
        default=BLOCK_PAGE_CONTENT_HEADER, validation_alias="blockPageContents", serialization_alias="blockPageContents"
    )
    logging: List[str] = Field(default=[])
    enable_alerts: bool = Field(validation_alias="enableAlerts", serialization_alias="enableAlerts")
    alerts: Set[UrlFilteringAlerts] = Field(default=[], validation_alias="alerts", serialization_alias="alerts")
    target_vpns: List[VpnId] = Field(default=[], validation_alias="targetVpns", serialization_alias="targetVpns")

    @field_validator("url_black_list", "url_white_list", mode="before")
    @classmethod
    def convert_empty_dict_to_none(cls, value):
        if not value:
            return None

        return value


class UrlFilteringPolicy(PolicyDefinitionBase):
    type: Literal["urlFiltering"] = "urlFiltering"
    mode: PolicyModeType = "security"
    definition: UrlFilteringDefinition


class UrlFilteringPolicyEditPayload(UrlFilteringPolicy, PolicyDefinitionId):
    pass


class UrlFilteringPolicyGetResponse(UrlFilteringPolicy, PolicyDefinitionGetResponse):
    pass
