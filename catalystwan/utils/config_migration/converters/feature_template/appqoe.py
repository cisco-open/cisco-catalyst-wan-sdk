from copy import deepcopy
from typing import List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.appqoe import (
    Appqoe,
    AppqoeParcel,
    ForwarderAppnavControllerGroup,
    ForwarderController,
    ForwarderNodeGroup,
    ForwarderRole,
    ResourceProfile,
    ServiceContext,
    ServiceNodeGroupName,
    ServiceNodeGroupsNames,
    ServiceNodeInformation,
    ServiceNodeRole,
    VirtualApplication,
    VirtualApplicationType,
)

from .base import FTConverter


class AppqoeConverter(FTConverter):
    supported_template_types = ("appqoe",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> AppqoeParcel:
        """
        Create an AppqoeParcel object based on the provided name, description, and template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): The template values used to create the parcel.

        Returns:
            AppqoeParcel: The created AppqoeParcel object.
        """
        data = deepcopy(template_values)

        virtual_application = self.parse_virtual_applications(
            data.get("virtual_applications", {}).get("virtual_application", [])
        )
        dreopt = self.parse_dreopt(data)
        service_node = self.parse_service_node(data.get("service_node", []))
        forwarder = self.parse_forwarder(data)

        return AppqoeParcel(
            parcel_name=name,
            parcel_description=description,
            dreopt=dreopt,
            virtual_application=virtual_application,
            service_node=service_node,
            forwarder=forwarder,
        )

    def parse_dreopt(self, values: dict) -> Optional[Global[bool]]:
        return values.get("dreopt")

    def parse_virtual_applications(self, virtual_applications: list) -> List[VirtualApplication]:
        return [self.parse_virtual_application(va) for va in virtual_applications]

    def parse_virtual_application(self, va: dict) -> VirtualApplication:
        return VirtualApplication(
            instance_id=as_global(int(va["instance_id"].value)),
            application_type=as_global(va["application_type"].value, VirtualApplicationType),
            resource_profile=self.parse_resource_profile(va.get("dreopt", {}).get("resource_profile")),
        )

    def parse_resource_profile(
        self, resource_profile: Optional[Global[str]]
    ) -> Union[Global[ResourceProfile], Default[ResourceProfile]]:
        if not resource_profile:
            return Default[ResourceProfile](value="default")
        return as_global(resource_profile.value, ResourceProfile)

    def parse_service_node(self, service_node: list) -> Optional[ServiceNodeRole]:
        """There can't be any other values that default values for service node"""
        if not service_node:
            return None
        return ServiceNodeRole()

    def parse_forwarder(self, data: dict) -> Optional[ForwarderRole]:
        return ForwarderRole(
            appnav_controller_group=self.parse_appnav_controller_group(data.get("appnav_controller_group", [])),
            service_node_group=self.parse_service_node_group(data.get("service_node_group", [])),
            service_context=self.parse_service_context(data.get("service_context", {}).get("appqoe", [])),
        )

    def parse_service_context(self, service_context: list) -> ServiceContext:
        if not service_context:
            return ServiceContext()
        return ServiceContext(appqoe=[self.parse_appqoe(sc) for sc in service_context])

    def parse_appqoe(self, appqoe: dict) -> Appqoe:
        return Appqoe(
            service_node_groups=self.parse_service_node_groups(appqoe.get("service_node_groups")),
            enable=appqoe.get("enable", Global[bool](value=True)),
            vpn=appqoe.get("vpn", Default[None](value=None)),
        )

    def parse_service_node_groups(
        self, service_node_groups: Optional[Global[List[str]]]
    ) -> List[Global[ServiceNodeGroupsNames]]:
        if not service_node_groups:
            return []
        return [as_global(sng, ServiceNodeGroupsNames) for sng in service_node_groups.value]

    def parse_appnav_controller_group(self, appnav_controller_group: list) -> List[ForwarderAppnavControllerGroup]:
        return [self.parse_fowarder_appnav_controller_group(acg) for acg in appnav_controller_group]

    def parse_fowarder_appnav_controller_group(self, appnav_controller_group: dict) -> ForwarderAppnavControllerGroup:
        return ForwarderAppnavControllerGroup(
            appnav_controllers=[
                self.parse_fowarder_controller(controller)
                for controller in appnav_controller_group.get("appnav_controllers", [])
            ]
        )

    def parse_fowarder_controller(self, controller: dict) -> ForwarderController:
        return ForwarderController(
            address=controller["address"],
            vpn=controller.get("vpn", Global[int](value=1)),
        )

    def parse_service_node_group(self, service_node_group: list) -> List[ForwarderNodeGroup]:
        return [self.parse_forwarder_node(sng) for sng in service_node_group]

    def parse_forwarder_node(self, sng: dict) -> ForwarderNodeGroup:
        return ForwarderNodeGroup(
            name=sng.get("name", Default[ServiceNodeGroupName](value="SNG-APPQOE")),
            internal=sng.get("internal", Default[bool](value=False)),
            service_node=[self.parse_service_node_information(node) for node in sng.get("service_node", [])],
        )

    def parse_service_node_information(self, node: dict) -> ServiceNodeInformation:
        return ServiceNodeInformation(address=node["address"])
