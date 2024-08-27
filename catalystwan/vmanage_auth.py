# Copyright 2022 Cisco Systems, Inc. and its affiliates

import logging
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlparse

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Response, get, post
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from catalystwan import USER_AGENT
from catalystwan.exceptions import CatalystwanException
from catalystwan.response import ManagerResponse
from catalystwan.version import NullVersion

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class UnauthorizedAccessError(CatalystwanException):
    """Exception raised for wrong username/password or when user not authorized to access vManage.

    Attributes:
        username (str): vManage username.
        password (str): vManage password.
        message (str): precise error explanation.
    """

    def __init__(
        self,
        username: str,
        password: str,
        message: str = "Wrong username/password or user not authorized to access vManage. Please try again!",
    ):
        self.username = username
        self.password = password
        self.message = message

    def __str__(self):
        return f"Trying to access vManage with the following credentials: {self.username}/****. {self.message}"


class vManageAuth(AuthBase):
    """Attaches vManage Authentication to the given Requests object.

    vManage REST API access control is based on sessions.
    The call method do whatever is required to make the vManage authentication work.
    The following are typical steps for a user to consume the API:
    1. Log in with a user name and password to establish a session.
    2. Get a cross-site request forgery prevention token, which is required for most POST operations.
    """

    def __init__(self, username: str, password: str, logger: Optional[logging.Logger] = None):
        self.username = username
        self.password = password
        self.jsessionid: str = ""
        self.xsrftoken: str = ""
        self.logger = logger or logging.getLogger(__name__)
        self._cookie: RequestsCookieJar = RequestsCookieJar()

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        self.handle_auth(request)
        self.build_digest_header(request)
        return request

    def handle_auth(self, request: PreparedRequest):
        cookie = request.headers.get("Cookie")
        wrong_cookie = cookie is None or (cookie is not None and "JSESSION" not in cookie)
        if self.jsessionid is None or self.xsrftoken is None or wrong_cookie:
            self.authenticate(request)

    @staticmethod
    def get_jsessionid(base_url: str, username: str, password: str) -> str:
        security_payload = {
            "j_username": username,
            "j_password": password,
        }
        url = base_url + "/j_security_check"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT}
        response: Response = post(url=url, headers=headers, data=security_payload, verify=False)
        jsessionid = response.cookies.get("JSESSIONID", "")
        if response.text != "" or not isinstance(jsessionid, str) or jsessionid == "":
            raise UnauthorizedAccessError(username, password)
        return jsessionid

    @staticmethod
    def get_xsrftoken(base_url: str, jsessionid: str) -> str:
        url = base_url + "/dataservice/client/token"
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        cookie = RequestsCookieJar()
        cookie.set("JSESSIONID", jsessionid)
        response: Response = get(
            url=url,
            cookies=cookie,
            headers=headers,
            verify=False,
        )
        if response.status_code != 200 or "<html>" in response.text:
            raise CatalystwanException("Failed to get XSRF token")
        return response.text

    def authenticate(self, request: PreparedRequest):
        base_url = f"{str(urlparse(request.url).scheme)}://{str(urlparse(request.url).netloc)}"
        self.jsessionid = self.get_jsessionid(base_url, self.username, self.password)
        self._cookie = RequestsCookieJar()
        self._cookie.set("JSESSIONID", self.jsessionid)
        self.xsrftoken = self.get_xsrftoken(base_url, self.jsessionid)

    def build_digest_header(self, request: PreparedRequest) -> None:
        request.headers["x-xsrf-token"] = self.xsrftoken
        request.prepare_cookies(self._cookie)

    def logout(self, session: "ManagerSession") -> Optional[ManagerResponse]:
        response = None
        if isinstance((version := session.api_version), NullVersion):
            session.logger.warning("Cannot perform logout operation without known api_version.")
            return response
        else:
            # disable automatic relogin before performing logout request
            _relogin = session.enable_relogin
            try:
                session.enable_relogin = False
                if version >= Version("20.12"):
                    response = session.post("/logout")
                else:
                    response = session.get("/logout")
            finally:
                # restore original setting after performing logout request
                session.enable_relogin = _relogin
        return response

    def __str__(self) -> str:
        return f"vManageAuth(username={self.username})"

    def clear_tokens_and_cookies(self) -> None:
        self.jsessionid = ""
        self.xsrftoken = ""
        self._cookie = RequestsCookieJar()
