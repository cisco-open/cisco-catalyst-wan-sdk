# Copyright 2023 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional, Union
from uuid import UUID, uuid4

from catalystwan.api.builders.feature_profiles.report import (
    FeatureProfileBuildReport,
    handle_build_report,
    handle_build_report_for_failed_subparcel,
)
from catalystwan.api.feature_profile_api import TransportFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.parcel import ParcelAssociationPayload
from catalystwan.models.configuration.feature_profile.sdwan.routing import AnyRoutingParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    AnyTransportParcel,
    AnyTransportSuperParcel,
    AnyTransportVpnParcel,
    AnyTransportVpnSubParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import CellularProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsParcel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class TransportAndManagementProfileBuilder:
    """
    A class for building system feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = TransportFeatureProfileAPI(session)
        self._endpoints = TransportFeatureProfile(session)
        self._independent_items: List[AnyTransportSuperParcel] = []
        self._independent_items_vpns: Dict[UUID, AnyTransportVpnParcel] = {}
        self._independent_items_cellular_controllers: Dict[UUID, CellularControllerParcel] = {}
        self._dependent_items_on_vpns: Dict[UUID, List[AnyTransportVpnSubParcel]] = defaultdict(list)
        self._dependent_routing_items_on_vpns: Dict[UUID, List[AnyRoutingParcel]] = defaultdict(list)
        self._dependent_items_on_cellular_controllers: Dict[
            UUID, List[Union[CellularProfileParcel, GpsParcel]]
        ] = defaultdict(list)

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile.

        Args:
            name (str): The name of the feature profile.
            description (str): The description of the feature profile.

        Returns:
            None
        """
        self._profile = feature_profile

    def add_parcel(self, parcel: AnyTransportSuperParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnyTransportSuperParcel): The parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def add_parcel_routing_attached(self, vpn_tag: UUID, parcel: AnyRoutingParcel) -> None:
        """
        Adds a routing parcel to the feature profile.

        Args:
            parcel (AnyRoutingParcel): The parcel to add.

        Returns:
            None
        """
        logger.debug(f"Attaching routing {parcel.parcel_name} with to VPN with tag {vpn_tag}")
        self._dependent_routing_items_on_vpns[vpn_tag].append(parcel)

    def add_parcel_vpn(self, parcel: AnyTransportVpnParcel) -> UUID:
        """
        Adds a VPN parcel to the builder.

        Args:
            parcel (LanVpnParcel): The VPN parcel to add.

        Returns:
            UUID: The UUID tag of the added VPN parcel.
        """
        vpn_tag = uuid4()
        logger.debug(f"Adding VPN parcel {parcel.parcel_name} with tag {vpn_tag}")
        self._independent_items_vpns[vpn_tag] = parcel
        return vpn_tag

    def add_parcel_cellular_controller(self, parcel: CellularControllerParcel) -> UUID:
        """
        Adds a cellular controller parcel to the builder.

        Args:
            parcel (CellularControllerParcel): The cellular controller parcel to add.

        Returns:
            UUID: The UUID tag of the added cellular controller parcel.
        """
        cellular_controller_tag = uuid4()
        logger.debug(f"Adding cellular controller parcel {parcel.parcel_name} with tag {cellular_controller_tag}")
        self._independent_items_cellular_controllers[cellular_controller_tag] = parcel
        return cellular_controller_tag

    def add_cellular_controller_subparcel(
        self, cellular_controller_tag: UUID, parcel: Union[CellularProfileParcel, GpsParcel]
    ) -> None:
        """
        Adds a subparcel to the cellular controller parcel.

        Args:
            cellular_controller_tag (UUID): The UUID of the cellular controller.
            parcel (Union[CellularProfileParcel, GpsParcel]): The subparcel to add.

        Returns:
            None
        """
        self._dependent_items_on_cellular_controllers[cellular_controller_tag].append(parcel)

    def add_vpn_subparcel(self, vpn_tag: UUID, parcel: AnyTransportVpnSubParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnyTransportVpnSubParcel): The parcel to add.

        Returns:
            None
        """
        self._dependent_items_on_vpns[vpn_tag].append(parcel)

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the feature profile.

        Returns:
            UUID: The UUID of the created feature profile.
        """

        profile_uuid = self._endpoints.create_transport_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._independent_items:
            self._create_parcel(profile_uuid, parcel)

        for vpn_tag, vpn_parcel in self._independent_items_vpns.items():
            vpn_uuid = self._create_parcel(profile_uuid, vpn_parcel)
            for vpn_subparcel in self._dependent_items_on_vpns[vpn_tag]:
                if vpn_uuid is None:
                    handle_build_report_for_failed_subparcel(self.build_report, vpn_parcel, vpn_subparcel)
                else:
                    self._create_parcel(profile_uuid, vpn_subparcel, vpn_uuid)

            for routing_parcel in self._dependent_routing_items_on_vpns[vpn_tag]:
                if vpn_uuid is None:
                    handle_build_report_for_failed_subparcel(self.build_report, vpn_parcel, routing_parcel)
                else:
                    routing_uuid = self._create_parcel(profile_uuid, routing_parcel)
                    if not routing_uuid:
                        continue
                    self._endpoints.associate_with_vpn(
                        profile_uuid,
                        vpn_uuid,
                        routing_parcel._get_parcel_type(),
                        payload=ParcelAssociationPayload(parcel_id=routing_uuid),
                    )

        for cellular_controller_tag, cellular_controller_parcel in self._independent_items_cellular_controllers.items():
            controller_uuid = self._create_parcel(profile_uuid, cellular_controller_parcel)
            for cellular_subparcel in self._dependent_items_on_cellular_controllers[cellular_controller_tag]:
                if controller_uuid is None:
                    handle_build_report_for_failed_subparcel(
                        self.build_report, cellular_controller_parcel, cellular_subparcel
                    )
                else:
                    parcel_uuid = self._create_parcel(profile_uuid, cellular_subparcel)
                    if not parcel_uuid:
                        continue
                    self._endpoints.associate_with_cellular_controller(
                        profile_uuid,
                        controller_uuid,
                        cellular_subparcel._get_parcel_type(),
                        ParcelAssociationPayload(parcel_id=parcel_uuid),
                    )

        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyTransportParcel, vpn_uuid: Optional[None] = None) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel, vpn_uuid).id
