# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
import os
import unittest
from typing import Union
from uuid import UUID, uuid4

from packaging.version import Version  # type: ignore

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
from catalystwan.exceptions import CatalystwanException
from catalystwan.session import ManagerSession, create_manager_session

logger = logging.getLogger(__name__)

RUN_ID: str = str(uuid4())[:4]


def load_config() -> dict:
    """Load the configuration from the environment variables"""
    url = os.environ.get("VMANAGE_URL")
    port = os.environ.get("VMANAGE_PORT")
    username = os.environ.get("VMANAGE_USERNAME")
    password = os.environ.get("VMANAGE_PASSWORD")
    if url is None or port is None or username is None or password is None:
        raise CatalystwanException("Missing environment variables")
    return dict(
        url=url,
        port=port,
        username=username,
        password=password,
    )


def create_session() -> ManagerSession:
    """Try to create a session with the environment variables, if it fails, raise an exception"""
    try:
        session = create_manager_session(**load_config())
        return session
    except Exception:
        raise CatalystwanException("Failed to create session")


SESSION = create_session()
IS_API_20_12: bool = SESSION.api_version == Version("20.12")


def create_name_with_run_id(name: str) -> str:
    """Prevent collisions when running on the same resource"""
    return f"{RUN_ID}_{name}"


class TestCaseBase(unittest.TestCase):
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
        cls.session = SESSION
