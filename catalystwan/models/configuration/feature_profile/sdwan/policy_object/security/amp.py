# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global

FileReputationServer = Literal["nam", "eur", "apjc"]
FileReputationAlert = Literal["critical", "warning", "info"]
FileAnalysisServer = Literal["nam", "eur"]
FileAnalysisAlert = Literal["critical", "warning", "info"]

FileAnalysisFileTypes = Literal[
    "pdf", "ms-exe", "new-office", "rtf", "mdb", "mscab", "msole2", "wri", "xlw", "flv", "swf"
]


class AdvancedMalwareProtectionParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
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
    file_analysis_cloud_server: Optional[Global[FileAnalysisServer]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisCloudServer")
    )
    file_analysis_file_types: Optional[Global[List[FileAnalysisFileTypes]]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisFileTypes")
    )
    file_analysis_alert: Optional[Global[FileAnalysisAlert]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisAlert")
    )

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        file_reputation_cloud_server: FileReputationServer,
        file_reputation_est_server: FileReputationServer,
        file_reputation_alert: FileReputationAlert,
        match_all_vpn: bool,
        file_analysis_enabled: bool = False,
        file_analysis_alert: Optional[FileAnalysisAlert] = None,
        file_analysis_cloud_server: Optional[FileAnalysisServer] = None,
        file_analysis_file_types: List[FileAnalysisFileTypes] = [],
    ):
        _file_analysis_alert = as_global(file_analysis_alert, FileAnalysisAlert) if file_analysis_alert else None
        _file_analysis_cloud_server = (
            Global[FileAnalysisServer](value=file_analysis_cloud_server) if file_analysis_cloud_server else None
        )

        _file_analysis_file_types = (
            Global[List[FileAnalysisFileTypes]](value=file_analysis_file_types) if file_analysis_file_types else None
        )

        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            file_reputation_cloud_server=as_global(file_reputation_cloud_server, FileReputationServer),
            file_reputation_est_server=as_global(file_reputation_est_server, FileReputationServer),
            file_analysis_alert=_file_analysis_alert,
            file_analysis_cloud_server=_file_analysis_cloud_server,
            file_reputation_alert=as_global(file_reputation_alert, FileReputationAlert),
            match_all_vpn=as_global(match_all_vpn),
            file_analysis_enabled=as_global(file_analysis_enabled),
            file_analysis_file_types=_file_analysis_file_types,
        )
