# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator

from catalystwan.endpoints import JSON, APIEndpoints, get, post, put, view
from catalystwan.typed_list import DataSequence
from catalystwan.utils.session_type import ProviderView, SingleTenantView

OnOffMode = Literal["on", "off"]
DataStreamIPTypes = Literal["systemIp", "mgmtIp", "transportIp"]
PasswordPolicies = Literal["disabled", "mediumSecurity", "highSecurity"]
SmartLicensingSettingModes = Literal["on-prem", "offline", "online"]
CRLActions = Literal["disable", "revoke", "quarantine"]


class Organization(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    org: Optional[str] = Field(default=None)
    domain_id: Optional[str] = Field(default=None, serialization_alias="domain-id", validation_alias="domain-id")
    control_connection_up: Optional[bool] = Field(
        default=None, serialization_alias="controlConnectionUp", validation_alias="controlConnectionUp"
    )


class Device(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    domain_ip: Optional[str] = Field(default=None, serialization_alias="domainIp", validation_alias="domainIp")
    port: Optional[str] = Field(default="12346")


class EmailNotificationSettings(BaseModel):
    enabled: Optional[bool] = False


class HardwareRootCA(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    hardware_certificate: Optional[str] = Field(
        default=None, serialization_alias="hardwareCertificate", validation_alias="hardwareCertificate"
    )
    control_connection_up: Optional[bool] = Field(
        default=False, serialization_alias="controlConnectionUp", validation_alias="controlConnectionUp"
    )


class Certificate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    certificate_signing: str = Field(serialization_alias="certificateSigning", validation_alias="certificateSigning")
    validity_period: Optional[str] = Field(serialization_alias="validityPeriod", validation_alias="validityPeriod")
    retrieve_interval: Optional[str] = Field(
        serialization_alias="retrieveInterval", validation_alias="retrieveInterval"
    )
    first_name: Optional[str] = Field(default=None, serialization_alias="firstName", validation_alias="firstName")
    last_name: Optional[str] = Field(default=None, serialization_alias="lastName", validation_alias="lastName")
    email: Optional[str] = Field(default=None)


class VEdgeCloud(BaseModel):
    certificateauthority: Optional[str] = None


class Banner(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mode: Optional[OnOffMode] = "off"
    banner_detail: Optional[str] = Field(serialization_alias="bannerDetail", validation_alias="bannerDetail")


class ProxyHTTPServer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    proxy: bool
    proxy_ip: str = Field(default="", serialization_alias="proxyIp", validation_alias="proxyIp")
    proxy_port: str = Field(default="", serialization_alias="proxyPort", validation_alias="proxyPort")


class ReverseProxy(BaseModel):
    mode: Optional[OnOffMode] = "off"


class CloudX(BaseModel):
    mode: Optional[OnOffMode] = "off"


class ManageEncryptedPassword(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    manage_type8_password: Optional[bool] = Field(
        default=False, serialization_alias="manageType8Password", validation_alias="manageType8Password"
    )


class CloudServices(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    enabled: Optional[bool] = False
    vanalytics_enabled: Optional[bool] = Field(
        default=False, serialization_alias="vanalyticsEnabled", validation_alias="vanalyticsEnabled"
    )
    vmonitoring_enabled: Optional[bool] = Field(
        default=False, serialization_alias="vmonitoringEnabled", validation_alias="vmonitoringEnabled"
    )
    otp: Optional[str] = None
    cloud_gateway_url: Optional[str] = Field(
        default=None, serialization_alias="cloudGatewayUrl", validation_alias="cloudGatewayUrl"
    )
    vanalytics_enabled_time: Optional[datetime.datetime] = Field(
        default=None, serialization_alias="vanalyticsEnabledTime", validation_alias="vanalyticsEnabledTime"
    )
    vmonitoring_enabled_time: Optional[datetime.datetime] = Field(
        default=None, serialization_alias="vmonitoringEnabledTime", validation_alias="vmonitoringEnabledTime"
    )


class ClientSessionTimeout(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_enabled: Optional[bool] = Field(default=False, serialization_alias="isEnabled", validation_alias="isEnabled")
    timeout: Optional[int] = Field(default=None, ge=10, description="timeout in minutes")


class SessionLifeTime(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    session_life_time: int = Field(
        serialization_alias="sessionLifeTime",
        validation_alias="sessionLifeTime",
        ge=30,
        le=10080,
        description="lifetime in minutes",
    )


class ServerSessionTimeout(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    server_session_timeout: int = Field(
        serialization_alias="serverSessionTimeout",
        validation_alias="serverSessionTimeout",
        ge=10,
        le=30,
        description="timeout in minutes",
    )


class MaxSessionsPerUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    max_sessions_per_user: int = Field(
        serialization_alias="maxSessionsPerUser", validation_alias="maxSessionsPerUser", ge=1, le=8
    )


class PasswordPolicy(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    password_policy: Union[bool, PasswordPolicies] = Field(
        serialization_alias="passwordPolicy", validation_alias="passwordPolicy"
    )
    password_expiration_time: Optional[int] = Field(
        default=False,
        serialization_alias="passwordExpirationTime",
        validation_alias="passwordExpirationTime",
        ge=1,
        le=90,
        description="timeout in days",
    )


class VManageDataStream(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    enable: Optional[bool] = False
    ip_type: Optional[DataStreamIPTypes] = Field(default=None, serialization_alias="ipType", validation_alias="ipType")
    server_host_name: Union[IPvAnyAddress, DataStreamIPTypes, None] = Field(
        default=None, serialization_alias="serverHostName", validation_alias="serverHostName"
    )
    vpn: Optional[int] = Field(default=None, le=512)


class DataCollectionOnNotification(BaseModel):
    enabled: bool


class SDWANTelemetry(BaseModel):
    enabled: bool


class StatsOperation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    stats_operation: str = Field(serialization_alias="statsOperation", validation_alias="statsOperation")
    rid: int = Field(serialization_alias="@rid", validation_alias="@rid")
    operation_interval: int = Field(
        serialization_alias="operationInterval",
        validation_alias="operationInterval",
        ge=1,
        description="interval in minutes",
    )
    default_interval: int = Field(
        serialization_alias="defaultInterval",
        validation_alias="defaultInterval",
        ge=1,
        description="interval in minutes",
    )


class MaintenanceWindow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    enabled: Optional[bool] = False
    message: Optional[str] = ""
    start: Optional[int] = Field(
        default=None, serialization_alias="epochStartTimeInMillis", validation_alias="epochStartTimeInMillis"
    )
    end: Optional[int] = Field(
        default=None, serialization_alias="epochEndTimeInMillis", validation_alias="epochEndTimeInMillis"
    )


class ElasticSearchDBSize(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    index_name: str = Field(serialization_alias="indexName", validation_alias="indexName")
    size_in_gb: int = Field(serialization_alias="sizeInGB", validation_alias="sizeInGB")


class GoogleMapKey(BaseModel):
    key: str


class SoftwareInstallTimeout(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    download_timeout: str = Field(serialization_alias="downloadTimeoutInMin", validation_alias="downloadTimeoutInMin")
    activate_timeout: str = Field(serialization_alias="activateTimeoutInMin", validation_alias="activateTimeoutInMin")
    control_pps: Optional[str] = Field(serialization_alias="controlPps", validation_alias="controlPps")

    @field_validator("download_timeout")
    def check_download_timeout(cls, download_timeout_str: str):
        download_timeout = int(download_timeout_str)
        if download_timeout < 60 or download_timeout > 360:
            raise ValueError("download timeout should be in range 60-360")
        return download_timeout_str

    @field_validator("activate_timeout")
    def check_activate_timeout(cls, activate_timeout_str: str):
        activate_timeout = int(activate_timeout_str)
        if activate_timeout < 30 or activate_timeout > 180:
            raise ValueError("activate timeout should be in range 30-180")
        return activate_timeout_str

    @field_validator("control_pps")
    def check_control_pps(cls, control_pps_str: str):
        control_pps = int(control_pps_str)
        if control_pps < 300 or control_pps > 65535:
            raise ValueError("control pps should be in range 300-65535")
        return control_pps_str


class IPSSignatureSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_enabled: Optional[bool] = Field(default=False, serialization_alias="isEnabled", validation_alias="isEnabled")
    username: Optional[str] = None
    update_interval: Optional[int] = Field(
        default=None,
        serialization_alias="updateInterval",
        validation_alias="updateInterval",
        description="interval in minutes",
        ge=1,
        le=1440,
    )


class SmartAccountCredentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class PnPConnectSync(BaseModel):
    mode: Optional[OnOffMode] = "off"


class ClaimDevice(BaseModel):
    enabled: bool


class WalkMe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    walkme: bool
    walkme_analytics: bool = Field(serialization_alias="walkmeAnalytics", validation_alias="walkmeAnalytics")


class SmartLicensingSetting(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mode: Optional[SmartLicensingSettingModes] = None
    ssm_server_url: Optional[str] = Field(None, serialization_alias="ssmServerUrl", validation_alias="ssmServerUrl")
    ssm_client_id: Optional[str] = Field(None, serialization_alias="ssmClientId", validation_alias="ssmClientId")
    ssm_client_secret: Optional[str] = Field(
        None, serialization_alias="ssmClientSecret", validation_alias="ssmClientSecret"
    )


class StatsCollectionInterval(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    config_name: Literal["statsCollection"] = Field(
        default="statsCollection", serialization_alias="configName", validation_alias="configName"
    )
    operation_interval: int = Field(
        ge=5,
        le=180,
        serialization_alias="operationInterval",
        validation_alias="operationInterval",
        description="collecion interval in minutes",
    )


StatsConfigItem = Union[StatsCollectionInterval, None]  # open for extension for now only one option could be deduced


class StatsConfig(BaseModel):
    config: List[StatsConfigItem]

    @staticmethod
    def from_collection_interval(interval: int) -> "StatsConfig":
        return StatsConfig(config=[StatsCollectionInterval(operation_interval=interval)])


class CRLSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    action: CRLActions
    crl_url: Optional[str] = Field(None, serialization_alias="crlUrl", validation_alias="crlUrl")
    polling_interval: Optional[str] = Field(description="Retrieval interval (1-24 hours)")
    vpn: Optional[str]

    @field_validator("polling_interval")
    def check_polling_interval(cls, polling_interval_str: str):
        polling_interval = int(polling_interval_str)
        if polling_interval < 1 or polling_interval > 24:
            raise ValueError("Polling interval should be in range 1-24")
        return polling_interval_str

    @field_validator("vpn")
    def check_vpn(cls, vpn_str: str):
        vpn = int(vpn_str)
        if vpn < 0 or vpn > 65530:
            raise ValueError("vpn should be in range 0-65530")
        return vpn_str


class CloudCredentials(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    umbrella_org_id: Optional[str] = Field(
        default=None, validation_alias="umbrellaOrgId", serialization_alias="umbrellaOrgId"
    )
    umbrella_sig_auth_key: Optional[str] = Field(
        default=None, validation_alias="umbrellaSIGAuthKey", serialization_alias="umbrellaSIGAuthKey"
    )
    umbrella_sig_auth_secret: Optional[str] = Field(
        default=None, validation_alias="umbrellaSIGAuthSecret", serialization_alias="umbrellaSIGAuthSecret"
    )
    umbrella_dns_auth_key: Optional[str] = Field(
        default=None, validation_alias="umbrellaDNSAuthKey", serialization_alias="umbrellaDNSAuthKey"
    )
    umbrella_dns_auth_secret: Optional[str] = Field(
        default=None, validation_alias="umbrellaDNSAuthSecret", serialization_alias="umbrellaDNSAuthSecret"
    )

    zscaler_organization: Optional[str] = Field(
        default=None, validation_alias="zscalerOrganization", serialization_alias="zscalerOrganization"
    )
    zscaler_partner_base_uri: Optional[str] = Field(
        default=None, validation_alias="zscalerPartnerBaseUri", serialization_alias="zscalerPartnerBaseUri"
    )
    zscaler_partner_key: Optional[str] = Field(
        default=None, validation_alias="zscalerPartnerKey", serialization_alias="zscalerPartnerKey"
    )
    zscaler_username: Optional[str] = Field(
        default=None, validation_alias="zscalerUsername", serialization_alias="zscalerUsername"
    )
    zscaler_password: Optional[str] = Field(
        default=None, validation_alias="zscalerPassword", serialization_alias="zscalerPassword"
    )

    cisco_sse_org_id: Optional[str] = Field(
        default=None, validation_alias="ciscoSSEOrgId", serialization_alias="ciscoSSEOrgId"
    )
    cisco_sse_auth_key: Optional[str] = Field(
        default=None, validation_alias="ciscoSSEAuthKey", serialization_alias="ciscoSSEAuthKey"
    )
    cisco_sse_auth_secret: Optional[str] = Field(
        default=None, validation_alias="ciscoSSEAuthSecret", serialization_alias="ciscoSSEAuthSecret"
    )


class ConfigurationSettings(APIEndpoints):
    def create_analytics_data_file(self):
        # POST /settings/configuration/analytics/dca
        ...

    def edit_cert_configuration(self):
        # PUT /settings/configuration/certificate/{settingType}
        ...

    def edit_configuration(self):
        # PUT /settings/configuration/{settingType}
        ...

    def get_cert_configuration(self):
        # GET /settings/configuration/certificate/{settingType}
        ...

    @get("/settings/configuration/{setting_type}")
    def get_configuration_by_setting_type(self, setting_type: str) -> JSON:
        ...

    @get("/settings/configuration/organization", "data")
    def get_organizations(self) -> DataSequence[Organization]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/device", "data")
    def get_devices(self) -> DataSequence[Device]:
        ...

    @get("/settings/configuration/emailNotificationSettings", "data")
    def get_email_notification_settings(self) -> DataSequence[EmailNotificationSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/hardwarerootca", "data")
    def get_hardware_root_cas(self) -> DataSequence[HardwareRootCA]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/certificate", "data")
    def get_certificates(self) -> DataSequence[Certificate]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/vedgecloud", "data")
    def get_vedge_cloud(self) -> DataSequence[VEdgeCloud]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/crlSetting")
    def get_clr_settings(self) -> DataSequence[CRLSettings]:
        ...

    @get("/settings/configuration/banner", "data")
    def get_banner(self) -> DataSequence[Banner]:
        ...

    @get("/settings/configuration/proxyHttpServer", "data")
    def get_proxy_http_servers(self) -> DataSequence[ProxyHTTPServer]:
        ...

    @get("/settings/configuration/reverseproxy", "data")
    def get_reverse_proxies(self) -> DataSequence[ReverseProxy]:
        ...

    @get("/settings/configuration/cloudx", "data")
    def get_cloudx(self) -> DataSequence[CloudX]:
        ...

    @get("/settings/configuration/manageEncryptedPassword", "data")
    def get_manage_encrypted_password(self) -> DataSequence[ManageEncryptedPassword]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/cloudservices", "data")
    def get_cloudservices(self) -> DataSequence[CloudServices]:
        ...

    @get("/settings/configuration/clientSessionTimeout", "data")
    def get_client_session_timeout(self) -> DataSequence[ClientSessionTimeout]:
        ...

    @get("/settings/configuration/sessionLifeTime", "data")
    def get_session_life_time(self) -> DataSequence[SessionLifeTime]:
        ...

    @get("/settings/configuration/serverSessionTimeout", "data")
    def get_server_session_timeout(self) -> DataSequence[ServerSessionTimeout]:
        ...

    @get("/settings/configuration/maxSessionsPerUser", "data")
    def get_max_sessions_per_user(self) -> DataSequence[MaxSessionsPerUser]:
        ...

    @get("/settings/configuration/passwordPolicy", "data")
    def get_password_policy(self) -> DataSequence[PasswordPolicy]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/vmanagedatastream", "data")
    def get_vmanage_data_stream(self) -> DataSequence[VManageDataStream]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/dataCollectionOnNotification", "data")
    def get_data_collection_on_notification(self) -> DataSequence[DataCollectionOnNotification]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/sdWanTelemetry", "data")
    def get_sdwan_telemetry(self) -> DataSequence[SDWANTelemetry]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/management/statsconfig")
    def get_stats_config(self) -> DataSequence[StatsOperation]:
        ...

    @get("/settings/configuration/spMetadata")
    def get_sp_metadata(self) -> str:
        ...

    @get("/management/elasticsearch/index/size", "indexSize")
    def get_elasticsearch_db_size(self) -> DataSequence[ElasticSearchDBSize]:
        ...

    @get("/settings/configuration/googleMapKey", "data")
    def get_google_map_key(self) -> DataSequence[GoogleMapKey]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/maintenanceWindow", "data")
    def get_maintenance_window(self) -> DataSequence[MaintenanceWindow]:
        ...

    @get("/settings/configuration/softwareMaintenance", "data")
    def get_software_install_timeout(self) -> DataSequence[SoftwareInstallTimeout]:
        ...

    @get("/settings/configuration/credentials", "data")
    def get_ips_signature_settings(self) -> DataSequence[IPSSignatureSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/smartaccountcredentials", "data")
    def get_smart_account_credentials(self) -> DataSequence[SmartAccountCredentials]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/pnpConnectSync", "data")
    def get_pnp_connect_sync(self) -> DataSequence[PnPConnectSync]:
        ...

    @get("/settings/configuration/claimDevice", "data")
    def get_claim_device(self) -> DataSequence[ClaimDevice]:
        ...

    @get("/settings/configuration/walkme", "data")
    def get_walkme(self) -> DataSequence[WalkMe]:
        ...

    @view({SingleTenantView, ProviderView})
    @get("/settings/configuration/smartLicensing", "data")
    def get_smart_licensing_settings(self) -> DataSequence[SmartLicensingSetting]:
        ...

    @get("/settings/configuration/cloudProviderSetting", "data")
    def get_cloud_credentials(self) -> DataSequence[CloudCredentials]:
        ...

    def new_cert_configuration(self):
        # POST /settings/configuration/certificate/{settingType}
        ...

    def new_configuration(self):
        # POST /settings/configuration/{settingType}
        ...

    @put("/settings/configuration/{setting_type}")
    def edit_configuration_by_setting_type(self, setting_type: str, payload: JSON) -> JSON:
        ...

    @put("/settings/configuration/organization", "data")
    def edit_organizations(self, payload: Organization) -> DataSequence[Organization]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/device", "data")
    def edit_devices(self, payload: Device) -> DataSequence[Device]:
        ...

    @put("/settings/configuration/emailNotificationSettings", "data")
    def edit_email_notification_settings(
        self, payload: EmailNotificationSettings
    ) -> DataSequence[EmailNotificationSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/hardwarerootca", "data")
    def edit_hardware_root_cas(self, payload: HardwareRootCA) -> DataSequence[HardwareRootCA]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/certificate", "data")
    def edit_certificates(self, payload: Certificate) -> DataSequence[Certificate]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/vedgecloud", "data")
    def edit_vedge_cloud(self, payload: VEdgeCloud) -> DataSequence[VEdgeCloud]:
        ...

    @put("/settings/configuration/banner", "data")
    def edit_banner(self, payload: Banner) -> DataSequence[Banner]:
        ...

    @put("/settings/configuration/proxyHttpServer", "data")
    def edit_proxy_http_servers(self, payload: ProxyHTTPServer) -> DataSequence[ProxyHTTPServer]:
        ...

    @put("/settings/configuration/reverseproxy", "data")
    def edit_reverse_proxies(self, payload: ReverseProxy) -> DataSequence[ReverseProxy]:
        ...

    @put("/settings/configuration/cloudx", "data")
    def edit_cloudx(self, payload: CloudX) -> DataSequence[CloudX]:
        ...

    @put("/settings/configuration/manageEncryptedPassword", "data")
    def edit_manage_encrypted_password(self, payload: ManageEncryptedPassword) -> DataSequence[ManageEncryptedPassword]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/cloudservices", "data")
    def edit_cloudservices(self, payload: CloudServices) -> DataSequence[CloudServices]:
        ...

    @put("/settings/configuration/clientSessionTimeout", "data")
    def edit_client_session_timeout(self, payload: ClientSessionTimeout) -> DataSequence[ClientSessionTimeout]:
        ...

    @put("/settings/configuration/sessionLifeTime", "data")
    def edit_session_life_time(self, payload: SessionLifeTime) -> DataSequence[SessionLifeTime]:
        ...

    @put("/settings/configuration/serverSessionTimeout", "data")
    def edit_server_session_timeout(self, payload: ServerSessionTimeout) -> DataSequence[ServerSessionTimeout]:
        ...

    @put("/settings/configuration/maxSessionsPerUser", "data")
    def edit_max_sessions_per_user(self, payload: MaxSessionsPerUser) -> DataSequence[MaxSessionsPerUser]:
        ...

    @put("/settings/configuration/passwordPolicy", "data")
    def edit_password_policy(self, payload: PasswordPolicy) -> DataSequence[PasswordPolicy]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/vmanagedatastream", "data")
    def edit_vmanage_data_stream(self, payload: VManageDataStream) -> DataSequence[VManageDataStream]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/dataCollectionOnNotification", "data")
    def edit_data_collection_on_notification(
        self, payload: DataCollectionOnNotification
    ) -> DataSequence[DataCollectionOnNotification]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/sdWanTelemetry", "data")
    def edit_sdwan_telemetry(self, payload: SDWANTelemetry) -> DataSequence[SDWANTelemetry]:
        ...

    @view({SingleTenantView, ProviderView})
    @post("/management/statsconfig")
    def edit_stats_config(self, payload: StatsConfig) -> DataSequence[StatsOperation]:
        ...

    @put("/settings/configuration/spMetadata")
    def edit_sp_metadata(self, payload: str) -> str:
        ...

    @put("/management/elasticsearch/index/size", "indexSize")
    def edit_elasticsearch_db_size(self, payload: ElasticSearchDBSize) -> DataSequence[ElasticSearchDBSize]:
        ...

    @put("/settings/configuration/googleMapKey")
    def edit_google_map_key(self, payload: GoogleMapKey) -> DataSequence[GoogleMapKey]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/maintenanceWindow")
    def edit_maintenance_window(self, payload: MaintenanceWindow) -> DataSequence[MaintenanceWindow]:
        ...

    @put("/settings/configuration/softwareMaintenance", "data")
    def edit_software_install_timeout(self, payload: SoftwareInstallTimeout) -> DataSequence[SoftwareInstallTimeout]:
        ...

    @put("/settings/configuration/credentials", "data")
    def edit_ips_signature_settings(self, payload: IPSSignatureSettings) -> DataSequence[IPSSignatureSettings]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/smartaccountcredentials", "data")
    def edit_smart_account_credentials(self, payload: SmartAccountCredentials) -> DataSequence[SmartAccountCredentials]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/pnpConnectSync", "data")
    def edit_pnp_connect_sync(self, payload: PnPConnectSync) -> DataSequence[PnPConnectSync]:
        ...

    @put("/settings/configuration/claimDevice", "data")
    def edit_claim_device(self, payload: ClaimDevice) -> DataSequence[ClaimDevice]:
        ...

    @put("/settings/configuration/walkme", "data")
    def edit_walkme(self, payload: WalkMe) -> DataSequence[WalkMe]:
        ...

    @view({SingleTenantView, ProviderView})
    @put("/settings/configuration/smartLicensing", "data")
    def edit_smart_licensing_settings(self, payload: SmartLicensingSetting) -> DataSequence[SmartLicensingSetting]:
        ...

    @put("/settings/configuration/cloudProviderSetting", "data")
    def edit_cloud_credentials(self, payload: CloudCredentials) -> DataSequence[CloudCredentials]:
        ...

    @post("/settings/configuration/cloudProviderSetting", "data")
    def create_cloud_credentials(self, payload: CloudCredentials) -> DataSequence[CloudCredentials]:
        ...
