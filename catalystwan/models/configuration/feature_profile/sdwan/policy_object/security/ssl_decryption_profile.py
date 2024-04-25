# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

Categories = Literal[
    "abortion",
    "abused-drugs",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "dead-sites",
    "dynamic-content",
    "educational-institutions",
    "entertainment-and-arts",
    "fashion-and-beauty",
    "financial-services",
    "gambling",
    "games",
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
    "military",
    "motor-vehicles",
    "music",
    "news-and-media",
    "nudity",
    "online-greeting-cards",
    "online-personal-storage",
    "open-http-proxies",
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
    "spam-urls",
    "sports",
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
]

DecryptThreshold = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]


class SslDecryptionProfileParcel(_ParcelBase):
    type_: Literal["unified/ssl-decryption-profile"] = Field(default="unified/ssl-decryption-profile", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    decrypt_categories: Global[List[Categories]] = Field(
        default=Global[List[Categories]](value=[]), validation_alias=AliasPath("data", "decryptCategories")
    )
    never_decrypt_categories: Global[List[Categories]] = Field(
        default=Global[List[Categories]](value=[]), validation_alias=AliasPath("data", "neverDecryptCategories")
    )
    skip_decrypt_categories: Global[List[Categories]] = Field(
        default=None, validation_alias=AliasPath("data", "skipDecryptCategories")
    )
    reputation: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "reputation")
    )
    decrypt_threshold: Global[DecryptThreshold] = Field(
        default=None, validation_alias=AliasPath("data", "decryptThreshold")
    )
    skip_decrypt_threshold: Global[DecryptThreshold] = Field(
        default=None, validation_alias=AliasPath("data", "skipDecryptThreshold")
    )
    fail_decrypt: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "failDecrypt")
    )
    url_allowed_list: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "urlAllowedList"))
    url_blocked_list: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "urlBlockedList"))
