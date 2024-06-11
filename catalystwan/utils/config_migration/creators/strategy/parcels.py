# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from collections import defaultdict
from typing import Dict, Iterator, List, cast
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.api.builders.feature_profiles.service import ServiceFeatureProfileBuilder
from catalystwan.api.builders.feature_profiles.transport import TransportAndManagementProfileBuilder
from catalystwan.models.configuration.config_migration import TransformedParcel
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.sdwan.routing.bgp import RoutingBgpParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospf import RoutingOspfParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospfv3 import (
    RoutingOspfv3IPv4Parcel,
    RoutingOspfv3IPv6Parcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyAssociatoryParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import LanVpnDhcpServerParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import AnyTransportVpnSubParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import CellularProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import ManagementVpnParcel, TransportVpnParcel
from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


def iterate_over_subparcels(
    parent: TransformedParcel, all_parcels: Dict[UUID, TransformedParcel]
) -> Iterator[TransformedParcel]:
    if not parent.header.subelements:
        yield from ()

    for element in parent.header.subelements:
        transformed_subparcel = all_parcels.get(element)
        if transformed_subparcel is None:
            logger.error(f"Parent {parent.header.origin}: subparcel {element} not found in all parcels. Skipping.")
            continue
        yield transformed_subparcel


class ParcelPusher:
    """
    Base class for pushing parcels to a feature profile.
    """

    def __init__(self, session: ManagerSession, profile_type: ProfileType):
        self.builder = session.api.builders.feature_profiles.create_builder(profile_type)

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> FeatureProfileBuildReport:
        raise NotImplementedError


class SimpleParcelPusher(ParcelPusher):
    """
    Simple implementation of ParcelPusher that creates parcels directly.
    Includes: Other and System feature profiles.
    """

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> FeatureProfileBuildReport:
        for transformed_parcel in target_parcels:
            self.builder.add_parcel(transformed_parcel.parcel)  # type: ignore
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()


class ServiceParcelPusher(ParcelPusher):
    """
    Parcel pusher for service feature profiles.
    """

    builder: ServiceFeatureProfileBuilder

    def __init__(self, session: ManagerSession, profile_type: ProfileType):
        super().__init__(session, profile_type)
        self.subparcel_name_counter: Dict[str, int] = defaultdict(lambda: 0)

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> FeatureProfileBuildReport:
        for transformed_parcel in target_parcels:
            parcel = transformed_parcel.parcel
            if not isinstance(parcel, LanVpnParcel):
                self.builder.add_parcel(parcel)  # type: ignore
            else:
                vpn_tag = self.builder.add_parcel_vpn(parcel)  # type: ignore

                for element_level_1 in iterate_over_subparcels(transformed_parcel, all_parcels):
                    resolved_parcel = self._resolve_parcel_naming(element_level_1)

                    if isinstance(
                        resolved_parcel,
                        (RoutingBgpParcel, RoutingOspfParcel, RoutingOspfv3IPv6Parcel, RoutingOspfv3IPv4Parcel),
                    ):
                        # Routing global parcels
                        self.builder.add_parcel_routing_attached(vpn_tag, resolved_parcel)
                    else:
                        # Interfaces
                        self.builder.add_parcel_vpn_subparcel(vpn_tag, resolved_parcel)  # type: ignore

                        for element_level_2 in iterate_over_subparcels(element_level_1, all_parcels):
                            if isinstance(element_level_2.parcel, LanVpnDhcpServerParcel):
                                logger.info(
                                    f"Interface {parcel.parcel_name}: "
                                    f"Adding DHCP server parcel {element_level_2.parcel.parcel_name}"
                                )
                                self.builder.add_parcel_dhcp_server(parcel.parcel_name, element_level_2.parcel)

        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()

    def _resolve_parcel_naming(self, transformed_subparcel: TransformedParcel) -> AnyAssociatoryParcel:
        """This occurs when a Device Template has many VPNs and the VPNs have assigned the same subcomponent.
        In UX2 every subparcel has to be unique, so we have to rename the subparcels to avoid conflicts.
        We check if the same name exist and if it does we add a counter to the name,
        create copy and change the name with the counter value.
        """
        self.subparcel_name_counter[transformed_subparcel.parcel.parcel_name] += 1
        parcel = cast(AnyAssociatoryParcel, transformed_subparcel.parcel)
        count_value = self.subparcel_name_counter[parcel.parcel_name]
        if count_value > 1:
            parcel = parcel.model_copy(deep=True)
            parcel.parcel_name += f"_{count_value}"
        return parcel


class TransportAndManagementParcelPusher(ParcelPusher):
    """
    Parcel pusher for transport and management feature profiles.
    """

    builder: TransportAndManagementProfileBuilder

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> FeatureProfileBuildReport:
        for transformed_parcel in target_parcels:
            parcel = transformed_parcel.parcel
            if isinstance(parcel, (ManagementVpnParcel, TransportVpnParcel)):
                vpn_tag = self.builder.add_parcel_vpn(parcel)
                for element in iterate_over_subparcels(transformed_parcel, all_parcels):
                    if isinstance(
                        element.parcel,
                        (RoutingBgpParcel, RoutingOspfParcel, RoutingOspfv3IPv6Parcel, RoutingOspfv3IPv4Parcel),
                    ):
                        # Routing global parcels
                        self.builder.add_parcel_routing_attached(vpn_tag, element.parcel)
                    else:
                        # Interfaces
                        self.builder.add_vpn_subparcel(vpn_tag, cast(AnyTransportVpnSubParcel, element.parcel))
            elif isinstance(parcel, CellularControllerParcel):
                cellular_tag = self.builder.add_parcel_cellular_controller(parcel)
                for element in iterate_over_subparcels(transformed_parcel, all_parcels):
                    if isinstance(element.parcel, (CellularProfileParcel, GpsParcel)):
                        self.builder.add_cellular_controller_subparcel(cellular_tag, element.parcel)
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()
