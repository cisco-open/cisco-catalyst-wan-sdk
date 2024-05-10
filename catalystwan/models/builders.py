from typing import Any, List, Optional, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.exceptions import ManagerErrorInfo
from catalystwan.models.configuration.feature_profile.parcel import ParcelType

ParcelName = str


class FailedRequestDetails(BaseModel):
    method: str
    url: str
    headers: str
    body: str


class FailedParcel(BaseModel):
    parcel_name: ParcelName
    parcel_type: ParcelType
    error_info: Union[ManagerErrorInfo, str]
    debug_details: Optional[FailedRequestDetails] = None


class FeatureProfileBuildRapport(BaseModel):
    profile_name: str = ""
    profile_uuid: UUID
    created_parcels: List[Tuple[ParcelName, UUID]] = Field(default_factory=list)
    failed_parcels: List[FailedParcel] = Field(default_factory=list)

    def add_created_parcel(self, parcel_name: ParcelName, parcel_uuid: UUID) -> None:
        self.created_parcels.append((parcel_name, parcel_uuid))

    def add_failed_parcel(
        self,
        parcel_name: ParcelName,
        parcel_type: ParcelType,
        error_info: Union[ManagerErrorInfo, str],
        request: Optional[Any] = None,
    ) -> None:
        if request is not None:
            request = (
                FailedRequestDetails(
                    method=str(request.method),
                    url=str(request.url),
                    headers=str(request.headers),
                    body=str(request.body),
                ),
            )

        self.failed_parcels.append(
            FailedParcel(parcel_name=parcel_name, parcel_type=parcel_type, error_info=error_info, debug_details=request)
        )
