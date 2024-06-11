import os
import unittest
from typing import Union
from uuid import UUID

from catalystwan.api.feature_profile_api import (
    ApplicationPriorityFeatureProfileAPI,
    CliFeatureProfileAPI,
    DnsSecurityFeatureProfileAPI,
    OtherFeatureProfileAPI,
    ServiceFeatureProfileAPI,
    SIGSecurityAPI,
    SystemFeatureProfileAPI,
    TransportFeatureProfileAPI,
)
from catalystwan.session import ManagerSession, create_manager_session


class TestFeatureProfileModels(unittest.TestCase):
    session: ManagerSession
    profile_uuid: UUID
    api: Union[
        SystemFeatureProfileAPI,
        ServiceFeatureProfileAPI,
        OtherFeatureProfileAPI,
        TransportFeatureProfileAPI,
        CliFeatureProfileAPI,
        DnsSecurityFeatureProfileAPI,
        SIGSecurityAPI,
        ApplicationPriorityFeatureProfileAPI,
    ]

    @classmethod
    def setUpClass(cls) -> None:
        # TODO: Add those params to PyTest
        cls.session = create_manager_session(
            url=os.environ.get("TEST_VMANAGE_URL", "localhost"),
            port=int(os.environ.get("TEST_VMANAGE_PORT", 443)),
            username=os.environ.get("TEST_VMANAGE_USERNAME", "admin"),
            password=os.environ.get("TEST_VMANAGE_PASSWORD", "admin"),
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
