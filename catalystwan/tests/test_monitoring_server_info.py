# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from catalystwan.endpoints.monitoring.server_info import ServerInfo
from catalystwan.models.monitoring.server_info import ServerInfoResponse


class TestServerInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_server_info_data = {
            "Achitecture": "x86_64",
            "Available processors": 4,
        }  # Note the spelling error

    @patch("catalystwan.session.ManagerSession")
    def test_get_server_info(self, mock_session):
        # Arrange
        # Create a MagicMock for the response that has a dataobj method
        mock_response = MagicMock()
        # Set up the mock response's dataobj method to return a ServerInfoResponse
        mock_response.dataobj.return_value = ServerInfoResponse(**self.mock_server_info_data)

        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response

        server_info_api = ServerInfo(mock_session_instance)

        # Act
        response = server_info_api.get_server_info()

        # Assert
        self.assertIsInstance(response, ServerInfoResponse)
        self.assertEqual(response.architecture, self.mock_server_info_data["Achitecture"])
        self.assertEqual(
            response.available_processors,
            self.mock_server_info_data["Available processors"],
        )
        self.assertEqual(response.architecture, "x86_64")
        self.assertEqual(response.available_processors, 4)

        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
