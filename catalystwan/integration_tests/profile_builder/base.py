import os
import unittest

from catalystwan.session import ManagerSession, create_manager_session


class TestFeatureProfileBuilder(unittest.TestCase):
    session: ManagerSession

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
