# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class RealTimeMonitoringAPI:
    """Real Time Monitoring API gathers information from Real time Monitoring page.

    Attributes:
        session (ManagerSession): logged in API client session

    Usage example:
        # Create session
        session = create_manager_session(...)
        # Get information about tenant status
        tenant_status = session.api.dashboard.get_tenant_status()
    """

    def __init__(self, session: ManagerSession):
        self.session = session

    def get_bfd_summary(self, device_id) -> List:
        """
        Get information about bfd summary from a device.

        Returns:
            List of bfd summary
        """
        bfd_summary = self.session.get_data("/dataservice/device/bfd/summary?deviceId={}".format(device_id))

        return bfd_summary

    def get_device_status(self, device_id) -> List:
        """
        Get system status from a device.

        Returns:
            List of system status
        """
        device_status = self.session.get_data("/dataservice/device/system/status?deviceId={}".format(device_id))

        return device_status

    def get_hardware_status_summary(self, device_id) -> List:
        """
        Get hardware status summary from a device.

        Returns:
            List of hardware status.
        """
        device_hw = self.session.get_data("/dataservice/device/hardware/status/summary?deviceId={}".format(device_id))

        return device_hw

    def get_approute_trans_summary(self, site_id) -> List:
        """
        Get app route stats for a tunnel with loss percentage from a site.

        Returns:
            List of app route state
        """
        approute_summary = self.session.get_data(
            "dataservice/statistics/approute/tunnels/health/loss_percentage?"
            "limit=10000&last_n_hours=24&site-id={}".format(site_id)
        )

        return approute_summary
