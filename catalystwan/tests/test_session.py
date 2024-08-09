# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from typing import Optional
from unittest.mock import patch

from parameterized import parameterized  # type: ignore
from requests import HTTPError, Request, RequestException, Response

from catalystwan.exceptions import CatalystwanException, ManagerHTTPError, ManagerRequestException
from catalystwan.session import ManagerSession, create_base_url
from catalystwan.vmanage_auth import vManageAuth


class TestSession(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com:80"
        self.username = "admin"
        self.password = "admin"  # pragma: allowlist secret

    def test_session_str(self):
        # Arrange, Act
        session = ManagerSession(self.url, auth=vManageAuth(self.username, self.password))

        # Assert
        self.assertEqual(
            str(session),
            "ManagerSession(session_type=SessionType.NOT_DEFINED, " "auth=vManageAuth(username=admin))",
        )

    @parameterized.expand(
        [
            (None, "http://example.com:666", "http://example.com:666"),
            (None, "www.example.com", "https://www.example.com"),
            (123, "example.com", "https://example.com:123"),
            (123, "http://example.com", "http://example.com:123"),
            (123, "https://example.com", "https://example.com:123"),
            (None, "https://example.com", "https://example.com"),
        ]
    )
    def test_base_url(self, port: Optional[int], user_url: str, expected_url: str):
        # Arrange, Act
        base_url = create_base_url(user_url, port=port)
        # Assert
        self.assertEqual(base_url, expected_url)

    @parameterized.expand(
        [
            (123, "/devices", "https://example.com:123/devices"),
            (123, "devices", "https://example.com:123/devices"),
            (None, "/devices", "https://example.com/devices"),
            (None, "devices", "https://example.com/devices"),
        ]
    )
    def test_get_full_url(self, port: Optional[int], url: str, expected_url: str):
        # Arrange, Act
        base_url = create_base_url("https://example.com", port=port)
        session = ManagerSession(base_url=base_url, auth=vManageAuth(base_url, self.username, self.password))

        # Assert
        self.assertEqual(session.get_full_url(url), expected_url)


class TestSessionExceptions(unittest.TestCase):
    def setUp(self):
        self.session = ManagerSession(
            base_url="https://domain.com:9443",
            auth=vManageAuth(username="admin", password="admin"),
        )
        response = Response()
        response.json = lambda: {
            "error": {
                "message": "Delete users request failed",
                "details": "No user with name XYZ was found",
                "code": "USER0006",
            }
        }
        response.status_code = 500
        response.request = Request(method="GET", url="/v1/data")
        self.response = response

    @parameterized.expand(
        [
            (RequestException(), [CatalystwanException, ManagerRequestException, RequestException]),
            (HTTPError(), [CatalystwanException, ManagerHTTPError, ManagerRequestException, RequestException]),
        ]
    )
    @patch("requests.sessions.Session.request")
    def test_session_request_exceptions(self, lib_exception, sdk_exceptions, mock_request_base):
        # Arrange
        if isinstance(lib_exception, HTTPError):
            mock_request_base.return_value = self.response
        else:
            mock_request_base.side_effect = lib_exception
        for sdk_exception in sdk_exceptions:
            # Act / Assert
            with self.assertRaises(sdk_exception):
                self.session.request(self.response.request.method, self.response.request.url)


if __name__ == "__main__":
    unittest.main()
