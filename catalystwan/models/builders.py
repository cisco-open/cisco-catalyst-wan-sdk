from typing import Any, List, Optional, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.exceptions import ManagerErrorInfo
from catalystwan.models.configuration.feature_profile.parcel import ParcelType

ParcelName = str


class FailedRequestDetails(BaseModel):
    method: str
    url: str
    headers: str
    body: str


class FailedParcel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parcel_name: ParcelName = Field(serialization_alias="parcelName", validation_alias="parcelName")
    parcel_type: ParcelType = Field(serialization_alias="parcelType", validation_alias="parcelType")
    error_info: Union[ManagerErrorInfo, str] = Field(serialization_alias="errorInfo", validation_alias="errorInfo")
    request_details: Optional[FailedRequestDetails] = Field(
        default=None, serialization_alias="failedRequest", validation_alias="failedRequest"
    )


class FeatureProfileBuildRaport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    profile_name: str = Field(serialization_alias="profileName", validation_alias="profileName")
    profile_uuid: UUID = Field(serialization_alias="profileUuid", validation_alias="profileUuid")
    created_parcels: List[Tuple[ParcelName, UUID]] = Field(
        default_factory=list, serialization_alias="createdParcels", validation_alias="createdParcels"
    )
    failed_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="failedParcels", validation_alias="failedParcels"
    )

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
            request = FailedRequestDetails(
                method=str(request.method),
                url=str(request.url),
                headers=str(request.headers),
                body=str(request.body),
            )

        self.failed_parcels.append(
            FailedParcel(
                parcel_name=parcel_name, parcel_type=parcel_type, error_info=error_info, request_details=request
            )
        )
