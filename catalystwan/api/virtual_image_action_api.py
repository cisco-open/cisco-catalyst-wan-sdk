# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, cast

from catalystwan.api.task_status_api import Task
from catalystwan.api.versions_utils import DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration_device_actions import (
    LxcImageActivatePayload,
    LxcImageDeletePayload,
    LxcImageUpgradePayload,
    LxcInstallInput,
)
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.exceptions import EmptyVersionPayloadError, ImageNotInRepositoryError  # type: ignore
from catalystwan.typed_list import DataSequence
from catalystwan.utils.upgrades_helper import get_install_specification, validate_personality_homogeneity

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class LxcActionAPI:
    """
    API methods for virtual software actions. All methods
    are executable on all device categories.

    Usage example:
    # Create session
    session = create_manager_session(...)

    # Prepare specific device for Lxc image actions
    all_dev = session.api.devices.get()
    dev = all_dev.filter(hostname="pm1044")
    ver = "1.0.0_SV3.1.67.0_XE17.14"

    # Upgrade
    del_id = session.api.lxcsoftware.lxcdelete(dev,ver)
    up_id = session.api.lxcsoftware.lxcupgrade(dev,ver)
    act_id = session.api.lxcsoftware.lxcactivate(dev,ver)

    # Check upgrade status
    TaskAPI(session, software_action_id).wait_for_completed()
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session)

    def lxcactivate(
        self,
        devices: DataSequence[DeviceDetailsResponse],
        version_to_activate: str,
    ) -> Task:
        """
        Requires that selected devices have already version_to_activate installed(upgraded)

        Args:
            devices (List[DeviceDetailsResponse]): For those devices software will be activated
            version_to_activate (Optional[str]): version to be set as current version

            Notice: Have to pass one of those arguments (version_to_activate, image)

        Raises:
            EmptyVersionPayloadError: If selected version_to_activate or image not detected in available files

        Returns:
            str: Activate software action id
        """
        validate_personality_homogeneity(devices)
        version = cast(str, version_to_activate)

        if not version:
            raise ImageNotInRepositoryError(
                "Based on provided arguments, virtual software version to activate on device(s) cannot be detected."
            )

        payload_devices = self.device_versions.get_lxcactivate_device_list(version, devices)
        for device in payload_devices:
            if not device.install_images[0].version_name:
                raise EmptyVersionPayloadError("lxc activate payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        install_input = LxcInstallInput(v_edge_vpn="0", version_type="vmanage")
        partition_payload = LxcImageActivatePayload(
            action="lxc_activate",
            devices=[dev for dev in payload_devices],
            device_type=device_type,
            input=install_input,
        )

        partition_action = self.session.endpoints.configuration_device_actions.process_lxc_activate(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)

    def lxcupgrade(
        self,
        devices: DataSequence[DeviceDetailsResponse],
        version_to_upgrade: Optional[str] = "",
        image: Optional[str] = "",
    ) -> Task:
        """
        Requires that selected devices have already version_to_upgrade

        Args:
            devices (List[DeviceDetailsResponse]): For those devices software will be activated
            version_to_upgrade (Optional[str]): version to be set as current version
            image (Optional[str]): software image name in available files

            Notice: Have to pass one of those arguments (version_to_activate, image)

        Raises:
            EmptyVersionPayloadError: If selected version_to_activate or image not detected in available files

        Returns:
            str: Activate software action id
        """
        validate_personality_homogeneity(devices)
        if image and not version_to_upgrade:
            version = cast(str, self.repository.get_image_version(image))
        elif version_to_upgrade and not image:
            version = cast(str, version_to_upgrade)
        else:
            raise ValueError("You can not provide software_image and image version at the same time!")

        if not version:
            raise ImageNotInRepositoryError(
                "Based on provided arguments, virtual software version to activate on device(s) cannot be detected."
            )

        payload_devices = self.device_versions.get_lxcupgrade_device_list(version, devices)
        for device in payload_devices:
            if not device.install_images[0].version_name:
                raise EmptyVersionPayloadError("lxc upgrade payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        install_input = LxcInstallInput(v_edge_vpn="0", version_type="vmanage")
        partition_payload = LxcImageUpgradePayload(
            action="lxc_upgrade", devices=[dev for dev in payload_devices], device_type=device_type, input=install_input
        )

        partition_action = self.session.endpoints.configuration_device_actions.process_lxc_upgrade(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)

    def lxcdelete(
        self,
        devices: DataSequence[DeviceDetailsResponse],
        version_to_delete: str,
    ) -> Task:
        """
        Requires that selected devices have already version_to_delete

        Args:
            devices (List[DeviceDetailsResponse]): For those devices lxc software will be deleted
            version_to_delete (Optional[str]): version to delete

            Notice: Have to pass one of those arguments (version_to_delete)

        Raises:
            EmptyVersionPayloadError: If selected version_to_activate or image not detected in available files

        Returns:
            str: Delete software action id
        """
        validate_personality_homogeneity(devices)
        version = cast(str, version_to_delete)

        if not version:
            raise ImageNotInRepositoryError(
                "Based on provided arguments, virtual software version to delete on device(s) cannot be detected."
            )

        payload_devices = self.device_versions.get_lxcupgrade_device_list(version, devices)
        for device in payload_devices:
            if not device.install_images[0].version_name:
                raise EmptyVersionPayloadError("lxc device payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        partition_payload = LxcImageDeletePayload(
            action="lxc_delete",
            devices=[dev for dev in payload_devices],
            device_type=device_type,
        )

        partition_action = self.session.endpoints.configuration_device_actions.process_lxc_delete(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)
