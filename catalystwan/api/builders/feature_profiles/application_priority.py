# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.feature_profile_api import ApplicationPriorityFeatureProfileAPI
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import AnyApplicationPriorityParcel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class ApplicationPriorityFeatureProfileBuilder:
    """
    A class for building Application Priority feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = ApplicationPriorityFeatureProfileAPI(session)
        self._parcels: List[AnyApplicationPriorityParcel] = []

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile.

        Args:
            feature_profile (FeatureProfileCreationPayload): Payload containing the name and description.

        Returns:
            None
        """
        self._profile = feature_profile

    def add_parcel(self, parcel: AnyApplicationPriorityParcel) -> None:
        self._parcels.append(parcel)

    def build(self) -> FeatureProfileBuildReport:
        profile_uuid = self._api.create_profile(self._profile.name, self._profile.description).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._parcels:
            self._create_parcel(profile_uuid, parcel)
        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyApplicationPriorityParcel) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel).id
