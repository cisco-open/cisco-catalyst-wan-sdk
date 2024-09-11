# Copyright 2022 Cisco Systems, Inc. and its affiliates

import logging
from typing import Callable, Optional
from urllib.parse import urlparse

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Response, get, post
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from catalystwan import USER_AGENT
from catalystwan.abstractions import APIEndpointClient, AuthProtocol
from catalystwan.exceptions import CatalystwanException
from catalystwan.response import ManagerResponse, auth_response_debug
from catalystwan.version import NullVersion


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


class vManageAuth(AuthBase, AuthProtocol):
    """Attaches vManage Authentication to the given Requests object.

    vManage REST API access control is based on sessions.
    The call method do whatever is required to make the vManage authentication work.
    The following are typical steps for a user to consume the API:
    1. Log in with a user name and password to establish a session.
    2. Get a cross-site request forgery prevention token, which is required for most POST operations.
    """

    def __init__(self, username: str, password: str, logger: Optional[logging.Logger] = None, verify=False):
        self.username = username
        self.password = password
        self.jsessionid: str = ""
        self.xsrftoken: str = ""
        self.verify = verify
        self.logger = logger or logging.getLogger(__name__)
        self._cookie: RequestsCookieJar = RequestsCookieJar()
        self._callback: Optional[Callable[[AuthBase], None]] = None
        self._base_url: Optional[str] = None

    def response_hook(self, r: Response, **kwargs) -> Response:
        _r = ManagerResponse(r)
        if _r.jsessionid_expired:
            self.clear()
        return r

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        self.handle_auth(request)
        self.build_digest_header(request)
        request.register_hook("response", self.response_hook)
        return request

    def handle_auth(self, request: PreparedRequest):
        if not self.jsessionid or not self.xsrftoken:
            self.authenticate(request)

    @staticmethod
    def get_jsessionid(
        base_url: str, username: str, password: str, logger: Optional[logging.Logger] = None, verify: bool = False
    ) -> str:
        security_payload = {
            "j_username": username,
            "j_password": password,
        }
        url = base_url + "/j_security_check"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT}
        response: Response = post(url=url, headers=headers, data=security_payload, verify=verify)
        if logger is not None:
            logger.debug(auth_response_debug(response))
        jsessionid = response.cookies.get("JSESSIONID", "")
        if response.text != "" or not isinstance(jsessionid, str) or jsessionid == "":
            raise UnauthorizedAccessError(username, password)
        return jsessionid

    @staticmethod
    def get_xsrftoken(
        base_url: str, jsessionid: str, logger: Optional[logging.Logger] = None, verify: bool = False
    ) -> str:
        url = base_url + "/dataservice/client/token"
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        cookie = RequestsCookieJar()
        cookie.set("JSESSIONID", jsessionid)
        response: Response = get(
            url=url,
            cookies=cookie,
            headers=headers,
            verify=verify,
        )
        if logger is not None:
            logger.debug(auth_response_debug(response))
        if response.status_code != 200 or "<html>" in response.text:
            raise CatalystwanException("Failed to get XSRF token")
        return response.text

    def authenticate(self, request: PreparedRequest):
        self._base_url = f"{str(urlparse(request.url).scheme)}://{str(urlparse(request.url).netloc)}"  # noqa: E231
        self.jsessionid = self.get_jsessionid(self._base_url, self.username, self.password, self.logger, self.verify)
        self._cookie = RequestsCookieJar()
        self._cookie.set("JSESSIONID", self.jsessionid)
        self.xsrftoken = self.get_xsrftoken(self._base_url, self.jsessionid, self.logger, self.verify)

    def build_digest_header(self, request: PreparedRequest) -> None:
        request.headers["x-xsrf-token"] = self.xsrftoken
        request.prepare_cookies(self._cookie)

    def logout(self, client: APIEndpointClient) -> None:
        if isinstance((version := client.api_version), NullVersion):
            self.logger.warning("Cannot perform logout without known api version.")
        elif self._base_url is None:
            self.logger.warning("Cannot perform logout without known base url")
        else:
            if version >= Version("20.12"):
                response = post(
                    f"{self._base_url}/logout",
                    cookies=self._cookie,
                    headers={"x-xsrf-token": self.xsrftoken},
                    verify=False,
                )
            else:
                response = get(f"{self._base_url}", cookies=self._cookie, verify=False)
            self.logger.debug(auth_response_debug(response))
            if response.status_code != 200:
                self.logger.error("Unsuccessfull logout")

    def __str__(self) -> str:
        return f"vManageAuth(username={self.username})"

    def clear(self) -> None:
        self.jsessionid = ""
        self.xsrftoken = ""
        self._cookie = RequestsCookieJar()
