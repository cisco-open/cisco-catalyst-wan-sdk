import unittest
from unittest.mock import MagicMock, patch

from catalystwan.endpoints.url_monitoring import UrlMonitoring
from catalystwan.models.url_monitoring import DeleteUrlMonitorRequest, UrlMonitoringConfig


class TestUrlMonitoring(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock) -> None:
        self.session = session_mock

        self.mock_url_monitor_info_data = {"url": "/client/server/ready", "threshold": 98, "alarm_raised": False}

        self.mock_url_monitor_config_add_data = {"url": "/client/server/ready", "threshold": 98}
        self.mock_url_monitor_config_update_data = {"url": "/client/server/ready", "threshold": 90}
        self.mock_url_monitor_delete_url = DeleteUrlMonitorRequest(url="/client/server/ready")

    @patch("catalystwan.session.ManagerSession")
    def test_add_url_monitor(self, mock_session):
        # Arrange
        mock_response = MagicMock()
        mock_session.get_data.return_value = UrlMonitoringConfig(**self.mock_url_monitor_config_add_data)
        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        mock_session.post.return_value = mock_response
        url_monitor = UrlMonitoring(mock_session_instance)

        # Act
        response = url_monitor.add_url_monitor(self.mock_url_monitor_config_add_data)
        # Assert
        self.assertEqual(response, None)
        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()

    @patch("catalystwan.session.ManagerSession")
    @patch("catalystwan.response.ManagerResponse")
    def test_get_url_monitor(self, mock_session, mock_response):
        # Arrange
        mock_response = MagicMock()
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        url_monitor = UrlMonitoring(mock_session_instance)
        observed_url_monitor = url_monitor.get_url_monitor()
        # Assert
        self.assertIsNotNone(observed_url_monitor)

    @patch("catalystwan.session.ManagerSession")
    def test_update_url_monitor(self, mock_session):
        # Arrange
        mock_response = MagicMock()
        mock_session.get_data.return_value = UrlMonitoringConfig(**self.mock_url_monitor_config_update_data)
        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        url_monitor = UrlMonitoring(mock_session_instance)
        # Act
        response = url_monitor.update_url_monitor(self.mock_url_monitor_config_update_data)
        # Assert
        self.assertEqual(response, None)
        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()

    @patch("catalystwan.session.ManagerSession")
    def test_delete_url_monitor(self, mock_session):
        # Arrange
        mock_response = MagicMock()
        mock_session.get_data.return_value = self.mock_url_monitor_delete_url
        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        url_monitor = UrlMonitoring(mock_session_instance)
        # Act
        response = url_monitor.delete_url_monitor(self.mock_url_monitor_delete_url)
        # Assert
        self.assertEqual(response, None)
        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()
