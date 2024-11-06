# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from catalystwan.dataclasses import TenantAAA, TenantRadiusServer, TenantTacacsServer
from catalystwan.exceptions import CatalystwanException
from catalystwan.utils.creation_tools import asdict, create_dataclass

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class AAAConfigNotPresent(CatalystwanException):
    pass


def status_ok(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        return True if response.status_code in [200, 204] else False

    return wrapper


class TenantAaaAPI:
    """
    Used to configure  mtt tenant management users remote servers
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/aaa"

    def __str__(self) -> str:
        return str(self.session)

    def aaa_exists(self) -> bool:
        return True if self.session.get_data(self.url_path) else False

    @status_ok
    def add_aaa(self, tenant_aaa: TenantAAA):
        """ "
        TenantAAA:
            "authOrder": [ "local", "radius", "tacacs"],
            "authFallback": true,
            "adminAuthOrder": false,
            "auditDisable": false,
            "accounting": false,
            "radiusServers": "server1"
        returns bool depending on the api post call
        """
        data = asdict(tenant_aaa)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    def get_aaa(self) -> TenantAAA:
        """
        Returns the Tenant AAA
        :param aaa:
        :return:
        """
        logger.debug("AAA config")
        tenant_aaa = self.session.get_data(self.url_path)
        # return tenant_aaa
        return create_dataclass(TenantAAA, tenant_aaa)

    @status_ok
    def del_aaa(self):
        """
        Delete aaa works only for tenants
        :return:
        """
        if not self.aaa_exists():
            raise AAAConfigNotPresent("No AAA config present for Tenant")
        logger.debug("Delete AAA config on tenant")
        return self.session.delete(self.url_path)

    @status_ok
    def put_aaa(self, tenant_AAA: TenantAAA):
        """
        Updated the AAA for tenant
        :return:
        """
        data = asdict(tenant_AAA)  # type: ignore
        return self.session.put(url=self.url_path, json=data)


class TenantRadiusAPI:
    """
    Used to configure  mtt tenant remote aaa radius servers
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/radius"

    def __str__(self) -> str:
        return str(self.session)

    @status_ok
    def add_radius(self, radius_server: TenantRadiusServer):
        """
        Create RADIUS for tenant
        :param radius_server:
        :return:
        """
        logger.debug("Add RADIUS config")
        data = asdict(radius_server)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    @status_ok
    def put_radius(self, radius_server: TenantRadiusServer):
        """
        edit radius server
        :param radius_server:
        :return:
        """
        logger.debug("Update RADIUS config")
        data = asdict(radius_server)  # type: ignore
        return self.session.put(url=self.url_path, json=data)

    @status_ok
    def delete_radius(self):
        """
        edit radius server
        :param radius_server:
        :return: True|False
        """
        logger.debug("Delete RADIUS config")
        return self.session.delete(self.url_path)

    def get_radius(self) -> TenantRadiusServer:
        """
        Retrieve Radius server
        :return: TenantRadiusServer
        """
        logger.debug("RADIUS config")
        data = self.session.get_data(self.url_path)
        return create_dataclass(TenantRadiusServer, data)


class TenantTacacsAPI:
    """
    Used to configure mtt tenant remote aaa TACACS servers
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.url_path = "/dataservice/admin/tacacs"

    def __str__(self) -> str:
        return str(self.session)

    @status_ok
    def add_tacacs(self, tacacs_server: TenantTacacsServer):
        """
        Create TACACS for tenant
        :param tacacs_server:
        :return:
        """
        logger.debug("TACACS config")
        data = asdict(tacacs_server)  # type: ignore
        return self.session.post(url=self.url_path, json=data)

    @status_ok
    def put_tacacs(self, tacacs_server: TenantTacacsServer):
        """
        Update tacacs server
        :param tacacs_server:
        :return:
        """
        logger.debug("Update TACACS config")
        data = asdict(tacacs_server)  # type: ignore
        return self.session.put(url=self.url_path, json=data)

    @status_ok
    def delete_tacacs(self):
        """
        Deletes tacacs server
        :param tacacs_server:
        :return: True|False
        """
        logger.debug("Delete TACACS config")
        return self.session.delete(self.url_path)

    def get_tacacs(self) -> TenantTacacsServer:
        """
        Retrieves Tacacs server
        :return: TenantTacacsServer
        """
        logger.debug("TACACS config")
        data = self.session.get_data(self.url_path)
        return create_dataclass(TenantTacacsServer, data)
