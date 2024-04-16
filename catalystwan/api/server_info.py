# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from catalystwan.models.server_info import ServerInfoResponse

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class ServerInfoAPI:
    """API methods of Server Info.

    Attributes:
        session: logged in API client session
    Usage example:
        # Create session
        session = create_manager_session(...)
        # Create device vpn
        server_info = session.api.server_info.get()
    """

    def __init__(self, session: ManagerSession):
        self.session = session

    def get(self) -> ServerInfoResponse:
        """Get server info.

        Args:
        Returns:
            ServerInfoResponse.
        """
        response = self._endpoints.server_info()
        return response.dataseq(ServerInfoResponse)
