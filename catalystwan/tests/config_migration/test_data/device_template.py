from typing import Optional
from uuid import UUID, uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo


def create_device_template(
    name,
    *,
    sig_uuid: Optional[UUID] = None,
    security_policy_uuid: Optional[UUID] = None,
    localized_policy_uuid: Optional[UUID] = None
) -> DeviceTemplateWithInfo:
    dt = DeviceTemplateWithInfo(
        template_id=str(uuid4()),
        factory_default=False,
        devices_attached=0,
        template_name=name,
        template_description="Description",
        device_role="None",
        device_type="None",
        security_policy_id="None",
        policy_id="None",
    )
    if sig_uuid:
        dt.general_templates = [
            GeneralTemplate(
                template_id=str(uuid4()),
                template_type="cisco_vpn",
                sub_templates=[
                    GeneralTemplate(template_id=str(sig_uuid), template_type="cisco_secure_internet_gateway")
                ],
            )
        ]
    if security_policy_uuid:
        dt.security_policy_id = str(security_policy_uuid)
    if localized_policy_uuid:
        dt.policy_id = str(localized_policy_uuid)

    return dt
