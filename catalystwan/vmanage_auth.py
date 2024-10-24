# Copyright 2022 Cisco Systems, Inc. and its affiliates

import logging
from http.cookies import SimpleCookie
from threading import RLock
from typing import Optional
from urllib.parse import urlparse

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Response, get, post
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar, merge_cookies

from catalystwan import USER_AGENT
from catalystwan.abstractions import APIEndpointClient, AuthProtocol
from catalystwan.exceptions import CatalystwanException, TenantSubdomainNotFound
from catalystwan.models.tenant import Tenant
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


def update_headers(
    request: PreparedRequest,
    jsessionid: Optional[str],
    xsrftoken: Optional[str] = None,
    vsessionid: Optional[str] = None,
) -> None:
    if jsessionid is not None:
        # preserve existing cookies and insert JSESSIONID
        # PreparedRequest.preparce_cookies cannot be used as they can be already set in session context
        cookie: SimpleCookie = SimpleCookie()
        cookie.load(request.headers.get("Cookie", ""))
        cookie["JSESSIONID"] = jsessionid
        request.headers["Cookie"] = cookie.output(header="", sep=";").strip()
    if xsrftoken is not None:
        request.headers["x-xsrf-token"] = xsrftoken
    if vsessionid is not None:
        request.headers["VSessionId"] = vsessionid


class vManageAuth(AuthBase, AuthProtocol):
    """Attaches vManage Authentication to the given Requests object.

    vManage REST API access control is based on sessions.
    The call method do whatever is required to make the vManage authentication work.
    The following are typical steps for a user to consume the API:
    1. Log in with a user name and password to establish a session.
    2. Get a cross-site request forgery prevention token, which is required for most POST operations.
    """

    def __init__(self, username: str, password: str, logger: Optional[logging.Logger] = None, verify: bool = False):
        self.username = username
        self.password = password
        self.xsrftoken: Optional[str] = None
        self.verify = verify
        self.logger = logger or logging.getLogger(__name__)
        self.cookies: RequestsCookieJar = RequestsCookieJar()
        self._base_url: str = ""
        self.session_count: int = 0
        self.lock: RLock = RLock()

    def __str__(self) -> str:
        return f"vManageAuth(username={self.username})"

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        with self.lock:
            self.handle_auth(request)
            update_headers(request, self.jsessionid, self.xsrftoken)
            return request

    def sync_cookies(self, cookies: RequestsCookieJar) -> None:
        self.cookies = merge_cookies(self.cookies, cookies)

    @property
    def jsessionid(self) -> Optional[str]:
        return self.cookies.get("JSESSIONID")

    def handle_auth(self, request: PreparedRequest):
        if not self.jsessionid or not self.xsrftoken:
            self.authenticate(request)

    def get_jsessionid(self) -> str:
        security_payload = {
            "j_username": self.username,
            "j_password": self.password,
        }
        url = self._base_url + "/j_security_check"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT}
        response: Response = post(url=url, headers=headers, data=security_payload, verify=self.verify)
        self.sync_cookies(response.cookies)
        self.logger.debug(auth_response_debug(response, str(self)))
        if response.text != "" or not isinstance(self.jsessionid, str) or self.jsessionid == "":
            raise UnauthorizedAccessError(self.username, self.password)
        return self.jsessionid

    def get_xsrftoken(self) -> str:
        url = self._base_url + "/dataservice/client/token"
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        response: Response = get(
            url=url,
            cookies=self.cookies,
            headers=headers,
            verify=self.verify,
        )
        self.sync_cookies(response.cookies)
        self.logger.debug(auth_response_debug(response, str(self)))
        if response.status_code != 200 or "<html>" in response.text:
            raise CatalystwanException("Failed to get XSRF token")
        return response.text

    def authenticate(self, request: PreparedRequest):
        self._base_url = f"{str(urlparse(request.url).scheme)}://{str(urlparse(request.url).netloc)}"  # noqa: E231
        self.get_jsessionid()
        self.xsrftoken = self.get_xsrftoken()

    def logout(self, client: APIEndpointClient) -> None:
        with self.lock:
            if self.session_count > 1:
                # Other sessions still use the auth, unregister and return
                return

            # last session using the auth, logout
            if isinstance((version := client.api_version), NullVersion):
                self.logger.warning("Cannot perform logout without known api version.")
            elif self._base_url is None:
                self.logger.warning("Cannot perform logout without known base url")
            else:
                headers = {"x-xsrf-token": self.xsrftoken, "User-Agent": USER_AGENT}
                if version >= Version("20.12"):
                    response = post(
                        f"{self._base_url}/logout", headers=headers, cookies=self.cookies, verify=self.verify
                    )
                else:
                    response = get(
                        f"{self._base_url}/logout", headers=headers, cookies=self.cookies, verify=self.verify
                    )
                self.logger.debug(auth_response_debug(response, str(self)))
                if response.status_code != 200:
                    self.logger.error("Unsuccessfull logout")
            self._clear()

    def _clear(self) -> None:
        with self.lock:
            self.cookies.clear_session_cookies()
            self.xsrftoken = None

    def increase_session_count(self) -> None:
        with self.lock:
            self.session_count += 1

    def decrease_session_count(self) -> None:
        with self.lock:
            self.session_count -= 1

    def clear(self, last_request: Optional[PreparedRequest]) -> None:
        with self.lock:
            # extract previously used jsessionid
            if last_request is None:
                jsessionid = None
            else:
                cookie: SimpleCookie = SimpleCookie()
                cookie.load(last_request.headers.get("Cookie", ""))
                try:
                    jsessionid = cookie["JSESSIONID"].value
                except KeyError:
                    jsessionid = None

            if self.jsessionid is None or self.jsessionid == jsessionid:
                # used auth was up-to-date, clear state
                return self._clear()
            else:
                # used auth was out-of-date, repeat the request with a new one
                return


class vSessionAuth(vManageAuth):
    def __init__(
        self,
        username: str,
        password: str,
        subdomain: str,
        logger: Optional[logging.Logger] = None,
        verify: bool = False,
    ):
        super().__init__(username, password, logger, verify)
        self.subdomain = subdomain
        self.vsessionid: Optional[str] = None

    def __str__(self) -> str:
        return f"vSessionAuth(username={self.username},subdomain={self.subdomain})"  # noqa: E231

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        with self.lock:
            self.handle_auth(request)
            update_headers(request, self.jsessionid, self.xsrftoken, self.vsessionid)
            return request

    def authenticate(self, request: PreparedRequest):
        super().authenticate(request)
        tenantid = self.get_tenantid()
        self.vsessionid = self.get_vsessionid(tenantid)

    def get_tenantid(self) -> str:
        url = self._base_url + "/dataservice/tenant"
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT, "x-xsrf-token": self.xsrftoken}
        response: Response = get(
            url=url,
            cookies=self.cookies,
            headers=headers,
            verify=self.verify,
        )
        self.sync_cookies(response.cookies)
        self.logger.debug(auth_response_debug(response, str(self)))
        tenants = ManagerResponse(response).dataseq(Tenant)
        tenant = tenants.filter(subdomain=self.subdomain).single_or_default()
        if not tenant or not tenant.tenant_id:
            raise TenantSubdomainNotFound(f"Tenant ID for sub-domain: {self.subdomain} not found")
        return tenant.tenant_id

    def get_vsessionid(self, tenantid: str) -> str:
        url = self._base_url + f"/dataservice/tenant/{tenantid}/vsessionid"
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT, "x-xsrf-token": self.xsrftoken}
        response: Response = post(
            url=url,
            cookies=self.cookies,
            headers=headers,
            verify=self.verify,
        )
        self.sync_cookies(response.cookies)
        self.logger.debug(auth_response_debug(response, str(self)))
        return response.json()["VSessionId"]

    def _clear(self) -> None:
        with self.lock:
            super()._clear()
            self.vsessionid = None


def create_vmanage_auth(
    username: str,
    password: str,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    verify: bool = False,
) -> vManageAuth:
    if subdomain is not None:
        return vSessionAuth(username, password, subdomain, logger=logger, verify=verify)
    else:
        return vManageAuth(username, password, logger=logger, verify=verify)
