import unittest
from unittest.mock import MagicMock, patch

from catalystwan.endpoints.url_monitoring import UrlMonitoring
from catalystwan.models.url_monitoring import UrlMonitoringInfo #, UrlMonitoringConfig, DeleteUrlMonitorRequest


class TestUrlMonitoring(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_url_monitor_info_data = [{
            "url": "/client/server/ready",
            "threshold": 20,
            "alarm_raised": False
        }]
        self.mock_url_monitor_config_add_data = {
            "url": "/client/server/ready",
            "threshold": 98
        }


    @patch("catalystwan.session.ManagerSession")
    def test_get_url_monitor(self, mock_session):
        # Arrange
        # Create a MagicMock for the response that has a dataobj method
        mock_response = MagicMock()
        # Set up the mock response's dataobj method to return a UrlMonitoringInfo
        mock_response.dataobj.return_value = UrlMonitoringInfo(**self.mock_url_monitor_info_data)
        # Mock the request method of the ManagerSession to return the mock response
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        url_monitor = UrlMonitoring(mock_session_instance)

        # Act
        response = url_monitor.get_url_monitor()
        # response = self.client.get("/url/monitor")
        # Additional assertions to test the response content
        # Assert
        # self.assertIsInstance(response, UrlMonitoringInfo)
        self.assertEqual(response[0].url, self.mock_server_info_data["url"])
        self.assertEqual(response[0].threshold, self.mock_server_info_data["threshold"])
        self.assertEqual(response[0].alarm_raised, self.mock_server_info_data["alarm_raised"])
        self.assertEqual(response[0].url, "/client/server/ready")
        self.assertEqual(response[0].threshold, 20)
        self.assertEqual(response[0].alarm_raised, False)
        # Ensure the request method was called
        mock_session_instance.request.assert_called_once()
