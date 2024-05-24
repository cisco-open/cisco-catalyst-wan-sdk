# Copyright 2023 Cisco Systems, Inc. and its affiliates
import functools
from typing import Any, List, Optional, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from requests import Response

from catalystwan.exceptions import ManagerErrorInfo, ManagerHTTPError
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


def handle_build_report(func):
    """Wrapper to make creating report simple and keep it DRY."""

    @functools.wraps(func)
    def wrapper(self, profile_uuid: UUID, parcel: AnyParcel, *args, **kwargs) -> Optional[UUID]:
        try:
            uuid = func(self, profile_uuid, parcel, *args, **kwargs)
            self.build_report.add_created_parcel(parcel.parcel_name, uuid)
            return uuid
        except ManagerHTTPError as e:
            self.build_report.add_failed_parcel(
                parcel_name=parcel.parcel_name,
                parcel_type=parcel._get_parcel_type(),
                error_info=e.info,
                request=e.request,
            )
            return None

    return wrapper


class FailedRequestDetails(BaseModel):
    method: str
    url: str
    headers: str
    body: str

    @staticmethod
    def from_response(response: Response):
        request = response.request
        FailedRequestDetails(
            method=str(request.method), url=str(request.url), headers=str(request.headers), body=str(request.body)
        )


class FailedParcel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parcel_name: str = Field(serialization_alias="parcelName", validation_alias="parcelName")
    parcel_type: str = Field(serialization_alias="parcelType", validation_alias="parcelType")
    error_info: Union[ManagerErrorInfo, str] = Field(serialization_alias="errorInfo", validation_alias="errorInfo")
    request_details: Optional[FailedRequestDetails] = Field(
        default=None, serialization_alias="failedRequest", validation_alias="failedRequest"
    )


class FeatureProfileBuildReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    profile_name: str = Field(serialization_alias="profileName", validation_alias="profileName")
    profile_uuid: UUID = Field(serialization_alias="profileUuid", validation_alias="profileUuid")
    created_parcels: List[Tuple[str, UUID]] = Field(
        default_factory=list, serialization_alias="createdParcels", validation_alias="createdParcels"
    )
    failed_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="failedParcels", validation_alias="failedParcels"
    )

    def add_created_parcel(self, parcel_name: str, parcel_uuid: UUID) -> None:
        self.created_parcels.append((parcel_name, parcel_uuid))

    def add_failed_parcel(
        self,
        parcel_name: str,
        parcel_type: str,
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


def handle_build_report_for_failed_subparcel(
    build_report: FeatureProfileBuildReport, parent: AnyParcel, subparcel: AnyParcel
) -> None:
    parent_failed_to_create_message = (
        f"Parent parcel: {parent.parcel_name} failed to create. This subparcel is dependent on it."
    )
    build_report.add_failed_parcel(
        parcel_name=subparcel.parcel_name,
        parcel_type=subparcel._get_parcel_type(),
        error_info=parent_failed_to_create_message,
    )
