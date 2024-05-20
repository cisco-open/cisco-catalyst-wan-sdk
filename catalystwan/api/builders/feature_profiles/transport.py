# Copyright 2023 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional
from uuid import UUID, uuid4

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.feature_profile_api import TransportFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    AnyTransportParcel,
    AnyTransportSuperParcel,
    AnyTransportVpnParcel,
    AnyTransportVpnSubParcel,
)

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
        self._dependent_items_on_vpns: Dict[UUID, List[AnyTransportVpnSubParcel]] = defaultdict(list)

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

    def add_vpn_subparcel(self, parcel: AnyTransportVpnSubParcel, vpn_tag: UUID) -> None:
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
            # TODO: Add subparcels to VPN
            vpn_uuid = self._create_parcel(profile_uuid, vpn_parcel)
            for subparcel in self._dependent_items_on_vpns[vpn_tag]:
                self._create_parcel(profile_uuid, subparcel, vpn_uuid)
        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyTransportParcel, vpn_uuid: Optional[None] = None) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel, vpn_uuid).id
