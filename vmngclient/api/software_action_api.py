from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from vmngclient.api.task_status_api import Task
from vmngclient.api.versions_utils import DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.exceptions import VersionDeclarationError  # type: ignore
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import asdict
from vmngclient.utils.personality import Personality
from vmngclient.utils.upgrades_helper import get_install_specification, validate_personality_homogeneity

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class SoftwareActionAPI:
    """
    API methods for software actions. All methods
    are exececutable on all device categories.

    Usage example:
    # Create session
    session = create_vManageSession(...)

    # Prepare devices list
    devices = session.api.devices.get()
    vsmarts = devices.filter(personality=Personality.VSMART)
    software_image = "viptela-20.7.2-x86_64.tar.gz"

    # Upgrade
    upgrade_id = SoftwareActionAPI(session).install(devices = vmanages,
    software_image=software_image)

    # Check upgrade status
    TaskAPI(session, software_action_id).wait_for_completed()
    """

    def __init__(self, session: vManageSession) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session)

    def activate(
        self,
        devices: DataSequence[Device],
        version_to_activate: Optional[str] = "",
        image: Optional[str] = "",
    ) -> Task:
        """
        Set chosen version as current version

        Args:
            devices (List[Device]): For those devices software will be activated
            version_to_activate (Optional[str]): version to be set as current version
            software_image (Optional[str]): path to software image

            Notice: Have to pass one of those arguments (version_to_activate,
            software_image)

        Returns:
            str: Activate software action id
        """
        validate_personality_homogeneity(devices)
        if image and not version_to_activate:
            version = cast(str, self.repository.get_image_version(image))
        elif version_to_activate and not image:
            version = cast(str, version_to_activate)
        else:
            raise VersionDeclarationError("You can not provide software_image and image version at the same time!")

        url = "/dataservice/device/action/changepartition"
        payload = {
            "action": "changepartition",
            "devices": [
                asdict(device) for device in self.device_versions.get_device_available(version, devices)  # type: ignore
            ],
            "deviceType": get_install_specification(devices.first()).device_type.value,
        }
        activate = dict(self.session.post(url, json=payload).json())
        return Task(self.session, activate["id"])

    def install(
        self,
        devices: DataSequence[Device],
        reboot: bool = False,
        sync: bool = True,
        image: Optional[str] = "",
        image_version: Optional[str] = "",
    ) -> Task:
        """
        Method to install new software

        Args:
            devices (List[Device]): For those devices software will be activated
            install_spec (InstallSpecification): specification of devices
            on which the action is to be performed
            reboot (bool): reboot device after action end
            sync (bool, optional): Synchronize settings. Defaults to True.
            software_image (Optional[str]): path to software image
            image_version (Optional[str]): version of software image

            Notice: Have to pass one of those arguments (image_version,
            software_image)

        Raises:
            ValueError: Raise error if downgrade in certain cases

        Returns:
            str: action id
        """
        validate_personality_homogeneity(devices)
        if image and not image_version:
            version = cast(str, self.repository.get_image_version(image))
        elif image_version and not image:
            version = cast(str, image_version)
        else:
            raise VersionDeclarationError("You can not provide software_image and image version at the same time")
        install_specification = get_install_specification(devices.first())

        url = "/dataservice/device/action/install"
        payload: Dict[str, Any] = {
            "action": "install",
            "input": {
                "vEdgeVPN": 0,
                "vSmartVPN": 0,
                "family": install_specification.family.value,
                "version": version,
                "versionType": install_specification.version_type.value,
                "reboot": reboot,
                "sync": sync,
            },
            "devices": [
                {"deviceId": device.deviceId, "deviceIP": device.deviceIP}
                for device in self.device_versions.get_device_list(devices)
            ],  # type: ignore
            "deviceType": install_specification.device_type.value,
        }
        if devices.first().personality in (
            Personality.VMANAGE,
            Personality.EDGE,
        ):  # block downgrade for edges and vmanages
            self._downgrade_check(payload["devices"], payload["input"]["version"], install_specification.family.value)
        upgrade = dict(self.session.post(url, json=payload).json())
        return Task(self.session, upgrade["id"])

    def _downgrade_check(self, payload_devices: List[dict], version_to_upgrade: str, family: str) -> None:
        """
        Check if upgrade operation is not actually a downgrade opeartion.
        If so, in some cases action is being blocked.

        Args:
            version_to_upgrade (str): version to upgrade
            devices_category (DeviceCategory): devices category

        Returns:
            List[str]: list of devices with no permission to downgrade
        """
        incorrect_devices = []
        devices_versions_repo = self.repository.get_devices_versions_repository()
        for device in payload_devices:
            dev_current_version = str(devices_versions_repo[device["deviceId"]].current_version)
            splited_version_to_upgrade = version_to_upgrade.split(".")
            for priority, label in enumerate(dev_current_version.split("-")[0].split(".")):
                try:
                    label = int(label)  # type: ignore
                    version = int(splited_version_to_upgrade[priority])
                except ValueError:
                    pass

                if label > version:  # type: ignore
                    if family == "vmanage" and label == 2:
                        continue
                    incorrect_devices.append(device["deviceId"])
                    break
                elif label < version:  # type: ignore
                    break
        if incorrect_devices:
            raise ValueError(
                f"Current version of devices with id's {incorrect_devices} is \
                higher than upgrade version. Action denied!"
            )