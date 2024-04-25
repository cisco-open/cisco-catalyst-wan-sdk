# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

SignatureSet = Literal["balanced", "connectivity", "security"]
InspectionMode = Literal["detection", "protection"]
LogLevel = Literal["emergency", "alert", "critical", "error", "warning", "notice", "info", "debug"]


class IntrusionPreventionParcel(_ParcelBase):
    type_: Literal["unified/intrusion-prevention"] = Field(default="unified/intrusion-prevention", exclude=True)
    signature_set: Global[SignatureSet] = Field(
        default=Global[SignatureSet](value="balanced"), validation_alias=AliasPath("data", "signatureSet")
    )
    inspection_mode: Global[InspectionMode] = Field(
        default=Global[InspectionMode](value="detection"), validation_alias=AliasPath("data", "inspectionMode")
    )
    signature_allowed_list: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "signatureAllowedList"))
    log_level: Global[LogLevel] = Field(
        default=Global[LogLevel](value="error"), validation_alias=AliasPath("data", "logLevel")
    )
    custom_signature: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "customSignature")
    )
