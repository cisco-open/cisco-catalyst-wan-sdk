from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.service import ServiceFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    AnyServiceParcel,
    AppqoeParcel,
    InterfaceEthernetParcel,
    InterfaceGreParcel,
    InterfaceIpsecParcel,
    InterfaceSviParcel,
    LanVpnDhcpServerParcel,
    LanVpnParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import MulticastParcel

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)

IndependedParcels = Annotated[Union[AppqoeParcel, LanVpnDhcpServerParcel], Field(discriminator="type_")]
DependedVpnSubparcels = Annotated[
    Union[InterfaceGreParcel, InterfaceSviParcel, InterfaceEthernetParcel, InterfaceIpsecParcel, MulticastParcel],
    Field(discriminator="type_"),
]


class ServiceFeatureProfileBuilder:
    """
    A class for building service feature profiles.
    """

    def __init__(self, session: ManagerSession):
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = ServiceFeatureProfileAPI(session)
        self._endpoints = ServiceFeatureProfile(session)
        self._independent_items: List[IndependedParcels] = []
        self._independent_items_vpns: Dict[UUID, LanVpnParcel] = {}
        self._depended_items_on_vpns: Dict[UUID, List[DependedVpnSubparcels]] = defaultdict(list)

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

    def add_parcel(self, parcel: IndependedParcels) -> None:
        """
        Adds an independent parcel to the builder.

        Args:
            parcel (IndependedParcels): The independent parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def add_parcel_vpn(self, parcel: LanVpnParcel) -> UUID:
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

    def add_parcel_vpn_subparcel(self, vpn_tag: UUID, parcel: DependedVpnSubparcels) -> None:
        """
        Adds an subparcel parcel dependent on a VPN to the builder.

        Args:
            vpn_tag (UUID): The UUID of the VPN.
            parcel (DependedInterfaceParcels): The interface parcel to add.

        Returns:
            None
        """
        logger.debug(f"Adding subparcel parcel {parcel.parcel_name} to VPN {vpn_tag}")
        self._depended_items_on_vpns[vpn_tag].append(parcel)

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the feature profile by creating parcels for independent items,
        VPNs, and sub-parcels dependent on VPNs.

        Returns:
            Service feature profile UUID
        """
        profile_uuid = self._endpoints.create_sdwan_service_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._independent_items:
            self._create_parcel(profile_uuid, parcel)
        for vpn_tag, vpn_parcel in self._independent_items_vpns.items():
            vpn_uuid = self._create_parcel(profile_uuid, vpn_parcel)
            if vpn_uuid is None:
                for sub_parcel in self._depended_items_on_vpns[vpn_tag]:
                    subparcel_fail_message = (
                        f"Parent parcel: {vpn_parcel.parcel_name} failed to create. This subparcel is dependent on it."
                    )
                    self.build_report.add_failed_parcel(
                        sub_parcel.parcel_name,
                        sub_parcel._get_parcel_type(),  # type: ignore
                        subparcel_fail_message
                        # incompatible type "str"; expected ParcelType, we will fix _get_parcel_type()
                        # to return ParcelType but for now it gives circular import
                    )
            else:
                for sub_parcel in self._depended_items_on_vpns[vpn_tag]:
                    self._create_parcel(profile_uuid, sub_parcel, vpn_uuid)

        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyServiceParcel, vpn_uuid: Optional[None] = None) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel, vpn_uuid).id
