# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional
from uuid import UUID

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

SignatureSet = Literal["balanced", "connectivity", "security"]
InspectionMode = Literal["detection", "protection"]
LogLevel = Literal["emergency", "alert", "critical", "error", "warning", "notice", "info", "debug"]


class IntrusionPreventionParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["unified/intrusion-prevention"] = Field(default="unified/intrusion-prevention", exclude=True)
    signature_set: Global[SignatureSet] = Field(
        default=Global[SignatureSet](value="balanced"), validation_alias=AliasPath("data", "signatureSet")
    )
    inspection_mode: Global[InspectionMode] = Field(
        default=Global[InspectionMode](value="detection"), validation_alias=AliasPath("data", "inspectionMode")
    )
    signature_allowed_list: Optional[RefIdItem] = Field(
        default=None, validation_alias=AliasPath("data", "signatureAllowedList")
    )
    log_level: Global[LogLevel] = Field(
        default=Global[LogLevel](value="error"), validation_alias=AliasPath("data", "logLevel")
    )
    custom_signature: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "customSignature")
    )

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        signature_set: SignatureSet = "balanced",
        inspection_mode: InspectionMode = "detection",
        signature_allowed_list: Optional[UUID] = None,
        log_level: LogLevel = "error",
        custom_signature: bool = False,
    ) -> "IntrusionPreventionParcel":
        sal: Optional[RefIdItem] = None
        if signature_allowed_list:
            sal = RefIdItem(ref_id=Global[str](value=str(signature_allowed_list)))

        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            signature_set=Global[SignatureSet](value=signature_set),
            inspection_mode=Global[InspectionMode](value=inspection_mode),
            signature_allowed_list=sal,
            log_level=Global[LogLevel](value=log_level),
            custom_signature=Global[bool](value=custom_signature),
        )
