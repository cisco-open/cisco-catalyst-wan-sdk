# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest import TestCase, mock
from uuid import uuid4

from requests import Request
from requests.cookies import RequestsCookieJar

from catalystwan import USER_AGENT
from catalystwan.exceptions import CatalystwanException
from catalystwan.vmanage_auth import UnauthorizedAccessError, vManageAuth


class MockResponse:
    def __init__(self, status_code: int, text: str, cookies: dict):
        self._status_code = status_code
        self._text = text
        self.cookies = cookies
        self.request = Request()

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def text(self) -> str:  # TODO
        return self._text


def mock_request_j_security_check(*args, **kwargs):
    url_response = {
        "https://1.1.1.1:1111/j_security_check": {
            "admin": MockResponse(200, "", {"JSESSIONID": "xyz"}),
            "invalid_username": MockResponse(200, "<html>error</html>", {}),
        }
    }

    full_url = kwargs.get("url", "")
    data = kwargs.get("data", {})
    if full_url in url_response:
        return url_response[full_url][data["j_username"]]

    return MockResponse(404, "error", {})


def mock_valid_token(*args, **kw):
    return MockResponse(200, "valid-token", {})


def mock_invalid_token_status(*args, **kw):
    return MockResponse(503, "invalid-token", {})


def mock_invalid_token_format(*args, **kw):
    return MockResponse(200, "<html>error</html>", {})


class TestvManageAuth(TestCase):
    def setUp(self):
        self.base_url = "https://1.1.1.1:1111"
        self.password = str(uuid4())

    @mock.patch("catalystwan.vmanage_auth.post", side_effect=mock_request_j_security_check)
    def test_get_cookie(self, mock_post):
        # Arrange
        username = "admin"
        security_payload = {
            "j_username": username,
            "j_password": self.password,
        }
        # Act
        vManageAuth.get_jsessionid(self.base_url, username, self.password)

        # Assert
        mock_post.assert_called_with(
            url="https://1.1.1.1:1111/j_security_check",
            data=security_payload,
            verify=False,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT},
        )

    @mock.patch("catalystwan.vmanage_auth.post", side_effect=mock_request_j_security_check)
    def test_get_cookie_invalid_username(self, mock_post):
        # Arrange
        username = "invalid_username"
        security_payload = {
            "j_username": username,
            "j_password": self.password,
        }
        # Act
        with self.assertRaises(UnauthorizedAccessError):
            vManageAuth.get_jsessionid(self.base_url, username, self.password)

        # Assert
        mock_post.assert_called_with(
            url="https://1.1.1.1:1111/j_security_check",
            data=security_payload,
            verify=False,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT},
        )

    @mock.patch("catalystwan.vmanage_auth.get", side_effect=mock_valid_token)
    def test_fetch_token(self, mock_get):
        # Arrange
        valid_url = "https://1.1.1.1:1111/dataservice/client/token"

        # Act
        token = vManageAuth.get_xsrftoken(self.base_url, "xyz")

        # Assert
        self.assertEqual(token, "valid-token")
        cookies = RequestsCookieJar()
        cookies.set("JSESSIONID", "xyz")
        mock_get.assert_called_with(
            url=valid_url,
            verify=False,
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
            cookies=cookies,
        )

    @mock.patch("catalystwan.vmanage_auth.get", side_effect=mock_invalid_token_status)
    def test_incorrect_xsrf_token_status(self, mock_get):
        with self.assertRaises(CatalystwanException):
            vManageAuth.get_xsrftoken(self.base_url, "xyz")

    @mock.patch("catalystwan.vmanage_auth.get", side_effect=mock_invalid_token_format)
    def test_incorrect_xsrf_token_format(self, mock_get):
        with self.assertRaises(CatalystwanException):
            vManageAuth.get_xsrftoken(self.base_url, "xyz")


if __name__ == "__main__":
    unittest.main()
