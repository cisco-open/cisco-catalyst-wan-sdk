import logging
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import BaseModel, Field, PositiveInt
from requests import PreparedRequest, post
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar

from catalystwan.exceptions import CatalystwanException
from catalystwan.response import ManagerResponse

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

LoginMode = Literal["machine", "user", "session"]


class ApiGwLogin(BaseModel):
    client_id: str
    client_secret: str
    org_name: str
    mode: Optional[LoginMode] = None
    username: Optional[str] = None
    session: Optional[str] = None
    tenant_user: Optional[bool] = None
    token_duration: PositiveInt = Field(default=10, description="in minutes")


class ApiGwAuth(AuthBase):
    def __init__(self, base_url: str, login: ApiGwLogin, verify: bool = False):
        self.base_url = base_url
        self.verify = verify
        self.login = login
        self.token = ""
        self.set_cookie = RequestsCookieJar()  # It is need for compatibility with ManagerSession::login method
        self.logger = logging.getLogger(__name__)

    def __call__(self, prepared_request: PreparedRequest) -> PreparedRequest:
        if self.token == "":
            self.token = self._get_token()
        prepared_request.headers.update(self._prepare_header())
        return prepared_request

    def _get_token(self) -> str:
        response = post(
            url=f"{self.base_url}/apigw/login",
            verify=self.verify,
            json=self.login.model_dump(exclude_none=True),
            timeout=10,
        )
        token = response.json().get("token", "")
        if not token or not isinstance(token, str):
            raise CatalystwanException("Failed to get bearer token")
        return token

    def _prepare_header(self) -> dict:
        return {
            "sdwan-org": self.login.org_name,
            "Authorization": f"Bearer {self.token}",
        }

    def __str__(self):
        return f"ApiGatewayAuth(base_url={self.base_url}, mode={self.login.mode})"

    def logout(self, session: "ManagerSession") -> Optional[ManagerResponse]:
        return None
