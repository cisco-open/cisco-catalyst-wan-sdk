from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.feature_profile_api import OtherFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.other import OtherFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class OtherFeatureProfileBuilder:
    """
    A class for building Other feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = OtherFeatureProfileAPI(session)
        self._endpoints = OtherFeatureProfile(session)
        self._independent_items: List[AnyOtherParcel] = []

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

    def add_parcel(self, parcel: AnyOtherParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnySystemParcel): The parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the feature profile.

        Returns:
            UUID: The UUID of the created feature profile.
        """

        profile_uuid = self._endpoints.create_sdwan_other_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._independent_items:
            self._create_parcel(profile_uuid, parcel)
        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyOtherParcel) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel).id
