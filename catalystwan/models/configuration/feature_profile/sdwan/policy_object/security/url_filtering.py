# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.configuration.feature_profile.common import RefIdItem

WebCategories = Literal[
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

WebCategoriesAction = Literal["block", "allow"]
WebReputation = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]
BlockPageAction = Literal["text", "redirect-url"]
Alerts = Literal["blacklist", "whitelist", "categories-reputation"]


class UrlFilteringParcel(_ParcelBase):
    type_: Literal["unified/url-filtering"] = Field(default="unified/url-filtering", exclude=True)
    web_categories_action: Global[WebCategoriesAction] = Field(
        validation_alias=AliasPath("data", "webCategoriesAction")
    )
    web_categories: Global[List[WebCategories]] = Field(validation_alias=AliasPath("data", "webCategories"))
    web_reputation: Global[WebReputation] = Field(validation_alias=AliasPath("data", "webReputation"))
    url_allowed_list: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "urlAllowedList"))
    url_blocked_list: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "urlBlockedList"))
    block_page_action: Global[BlockPageAction] = Field(validation_alias=AliasPath("data", "blockPageAction"))
    block_page_contents: Optional[Global[str]] = Field(
        default=None, validation_alias=AliasPath("data", "blockPageContents")
    )
    redirect_url: Optional[Global[str]] = Field(default=None, validation_alias=AliasPath("data", "redirectUrl"))
    enable_alerts: Global[bool] = Field(validation_alias=AliasPath("data", "enableAlerts"))
    alerts: Optional[Global[List[Alerts]]] = Field(default=None, validation_alias=AliasPath("data", "alerts"))

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        web_categories_action: WebCategoriesAction,
        web_categories: List[WebCategories],
        web_reputation: WebReputation,
        enable_alerts: bool,
        block_page_action: BlockPageAction,
        block_page_contents: str,
        alerts: List[Alerts] = [],
        url_allowed_list: Optional[RefIdItem] = None,
        url_blocked_list: Optional[RefIdItem] = None,
    ):
        _alerts = Global[List[Alerts]](value=alerts) if alerts else None

        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            web_categories_action=as_global(web_categories_action, WebCategoriesAction),
            web_categories=Global[List[WebCategories]](value=web_categories),
            web_reputation=as_global(web_reputation, WebReputation),
            block_page_action=as_global(block_page_action, BlockPageAction),
            block_page_contents=as_global(block_page_contents),
            enable_alerts=as_global(enable_alerts),
            alerts=_alerts,
            url_allowed_list=url_allowed_list,
            url_blocked_list=url_blocked_list,
        )
