# mypy: disable-error-code="empty-body"
from typing import Dict

from vmngclient.endpoints import APIEndpoints, post, request, view
from vmngclient.utils.pydantic import BaseModel, Field
from vmngclient.utils.session_type import ProviderView


class FeatureToCLIPayload(BaseModel):
    device_specific_variables: Dict[str, str] = Field(alias="device")
    is_edited: bool = Field(alias="isEdited")
    is_master_edited: bool = Field(alias="isMasterEdited")
    is_RFS_required: bool = Field(alias="isRFSRequired")
    template_id: str = Field(alias="templateId")


class ConfigurationDeviceTemplate(APIEndpoints):
    @view({ProviderView})
    @request(post, "/template/device/config/config/")
    def get_device_configuration_preview(self, payload: FeatureToCLIPayload) -> str:
        ...
