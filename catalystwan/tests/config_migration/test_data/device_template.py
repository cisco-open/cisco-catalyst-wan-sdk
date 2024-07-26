from uuid import uuid4

from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo


def create_device_template(name) -> DeviceTemplateWithInfo:
    return DeviceTemplateWithInfo(
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
