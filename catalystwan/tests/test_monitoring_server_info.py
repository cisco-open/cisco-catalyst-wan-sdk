# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from catalystwan.endpoints.monitoring.server_info import ServerInfo


class TestServerInfo(unittest.TestCase):
    def test_get_server_info(self):
        # Arrange
        self.api._endpoints.get_server_info.return_value = self.server_info_response
        # Act
        result = self.api.get_server_info()
        # Assert
        assert result == self.server_info_response


    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.response.ManagerResponse")
    def setUp(self, mock_session, mock_response) -> None:
        self.server_info_response = {'Achitecture': 'amd64', 'Available processors': 8}
        self.session = mock_session
        self.api = ServerInfo(self.session)
        self.api._endpoints = MagicMock()
        mock_response.json.return_value = self.server_info_response
