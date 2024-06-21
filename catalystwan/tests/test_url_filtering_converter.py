import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url_filtering import (
    UrlFilteringParcel,
)
from catalystwan.models.policy.definition.url_filtering import (
    BLOCK_PAGE_CONTENT_HEADER,
    UrlFilteringDefinition,
    UrlFilteringPolicyEditPayload,
)
from catalystwan.models.policy.policy_definition import Reference
from catalystwan.utils.config_migration.converters.policy.policy_definitions import url_filtering


class TestUrlFilteringConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()
        self.uuid = uuid4()

    def test_convert_security_url_filtering(self):
        policy = UrlFilteringPolicyEditPayload(
            definition_id=uuid4(),
            name="policy1",
            mode="security",
            definition=UrlFilteringDefinition(
                web_reputation="trustworthy",
                web_categories_action="allow",
                web_categories=["hacking", "hate-and-racism", "health-and-medicine"],
                block_page_action="text",
                block_page_contents=f"{BLOCK_PAGE_CONTENT_HEADER} test 123 test 456",
                enable_alerts=False,
                target_vpns=[1, 2, 4, 5],
            ),
        )

        parcel = url_filtering(policy, uuid=self.uuid, context=self.context).output

        assert isinstance(parcel, UrlFilteringParcel)
        assert parcel.parcel_name == "policy1"
        assert parcel.web_reputation.value == "trustworthy"
        assert parcel.web_categories_action.value == "allow"
        assert parcel.web_categories.value == ["hacking", "hate-and-racism", "health-and-medicine"]
        assert parcel.block_page_action.value == "text"
        assert parcel.block_page_contents.value == f"{BLOCK_PAGE_CONTENT_HEADER} test 123 test 456"
        assert parcel.enable_alerts.value is False
        assert parcel.url_allowed_list is None
        assert parcel.url_blocked_list is None
        assert parcel.alerts is None

        assert len(self.context.url_filtering_target_vpns) == 1
        assert self.uuid in self.context.url_filtering_target_vpns

    def test_convert_unified_url_filtering(self):
        policy = UrlFilteringPolicyEditPayload(
            definition_id=uuid4(),
            name="policy2",
            mode="unified",
            definition=UrlFilteringDefinition(
                web_reputation="suspicious",
                web_categories_action="allow",
                web_categories=["hacking", "health-and-medicine"],
                block_page_action="redirectUrl",
                block_page_contents="http://www.google.com",
                enable_alerts=True,
                alerts=["blacklist"],
            ),
        )

        parcel = url_filtering(policy, uuid=self.uuid, context=self.context).output

        assert isinstance(parcel, UrlFilteringParcel)
        assert parcel.parcel_name == "policy2"
        assert parcel.web_reputation.value == "suspicious"
        assert parcel.web_categories_action.value == "allow"
        assert parcel.web_categories.value == ["hacking", "health-and-medicine"]
        assert parcel.block_page_action.value == "redirect-url"
        assert parcel.block_page_contents.value == "http://www.google.com"
        assert parcel.enable_alerts.value is True
        assert parcel.url_allowed_list is None
        assert parcel.url_blocked_list is None
        assert parcel.alerts.value == ["blacklist"]

        assert len(self.context.url_filtering_target_vpns) == 0

    def test_convert_url_policy_with_allow_and_block_list(self):
        policy = UrlFilteringPolicyEditPayload(
            definition_id=uuid4(),
            name="policy3",
            mode="unified",
            definition=UrlFilteringDefinition(
                web_reputation="high-risk",
                web_categories_action="block",
                web_categories=["health-and-medicine"],
                block_page_action="text",
                block_page_contents=f"{BLOCK_PAGE_CONTENT_HEADER} test 555 test test 456",
                enable_alerts=True,
                alerts=["categories-reputation"],
                url_white_list=Reference(ref=uuid4()),
                url_black_list=Reference(ref=uuid4()),
            ),
        )

        parcel = url_filtering(policy, uuid=self.uuid, context=self.context).output

        assert isinstance(parcel, UrlFilteringParcel)
        assert parcel.parcel_name == "policy3"
        assert parcel.web_reputation.value == "high-risk"
        assert parcel.web_categories_action.value == "block"
        assert parcel.web_categories.value == ["health-and-medicine"]
        assert parcel.block_page_action.value == "text"
        assert parcel.block_page_contents.value == f"{BLOCK_PAGE_CONTENT_HEADER} test 555 test test 456"
        assert parcel.enable_alerts.value is True
        assert parcel.alerts.value == ["categories-reputation"]
        assert len(self.context.url_filtering_target_vpns) == 0

        assert parcel.url_allowed_list.ref_id.value == str(policy.definition.url_white_list.ref)
        assert parcel.url_blocked_list.ref_id.value == str(policy.definition.url_black_list.ref)
