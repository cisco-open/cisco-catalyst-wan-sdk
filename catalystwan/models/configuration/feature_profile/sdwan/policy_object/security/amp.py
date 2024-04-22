# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase

FileReputationServer = Literal["nam", "eur", "apjc"]
FileReputationAlert = Literal["critical", "warning", "info"]
FileAnalysisServer = Literal["nam", "eur"]
FileAnalysisAlert = Literal["critical", "warning", "info"]


class AdvancedMalwareProtectionParcel(_ParcelBase):
    type_: Literal["unified/advanced-malware-protection"] = Field(
        default="unified/advanced-malware-protection", exclude=True
    )
    description: str = "advancedMalwareProtection"
    match_all_vpn: Global[bool] = Field(
        default=Global[bool](value=True), validation_alias=AliasPath("data", "matchAllVpn")
    )
    file_reputation_cloud_server: Global[FileReputationServer] = Field(
        validation_alias=AliasPath("data", "fileReputationCloudServer")
    )
    file_reputation_est_server: Global[FileReputationServer] = Field(
        validation_alias=AliasPath("data", "fileReputationEstServer")
    )
    file_reputation_alert: Global[FileReputationAlert] = Field(
        default=Global[FileReputationAlert](value="critical"), validation_alias=AliasPath("data", "fileReputationAlert")
    )
    file_analysis_enabled: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "fileAnalysisEnabled")
    )
    file_analysis_cloud_server: Global[FileAnalysisServer] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisCloudServer")
    )
    file_analysis_file_types: Global[List[str]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisFileTypes")
    )
    file_analysis_alert: Global[FileAnalysisAlert] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisAlert")
    )
