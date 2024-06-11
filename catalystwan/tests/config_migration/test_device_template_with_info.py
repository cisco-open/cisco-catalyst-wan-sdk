import unittest

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo


class TestDeviceTemplate(unittest.TestCase):
    def setUp(self):
        self.device_template = DeviceTemplateWithInfo(
            template_id="1",
            factory_default=False,
            devices_attached=2,
            template_name="DT-example",
            template_description="DT-example",
            device_role="None",
            device_type="None",
            security_policy_id="None",
            policy_id="None",
            generalTemplates=[
                # Flat - stays flat
                GeneralTemplate(name="1level", templateId="1", templateType="cedge_aaa", subTemplates=[]),
                # No relation between system and logging in the UX2 - flatten them
                GeneralTemplate(
                    name="1level",
                    templateId="2",
                    templateType="cisco_system",
                    subTemplates=[
                        GeneralTemplate(
                            name="2level",
                            templateId="3",
                            templateType="cisco_logging",
                            subTemplates=[],
                        ),
                    ],
                ),
                # Cisco VPN - keep the structure
                GeneralTemplate(
                    name="1level",
                    templateId="4",
                    templateType="cisco_vpn",
                    subTemplates=[
                        GeneralTemplate(
                            name="2level",
                            templateId="5",
                            templateType="cisco_vpn_interface",
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name="2level",
                            templateId="6",
                            templateType="cedge_multicast",
                            subTemplates=[],
                        ),
                    ],
                ),
            ],
        )

    def test_flatten_general_templates(self):
        self.maxDiff = None
        self.assertEqual(
            self.device_template.get_flattened_general_templates(),
            [
                GeneralTemplate(name="1level", templateId="1", templateType="cedge_aaa", subTemplates=[]),
                GeneralTemplate(
                    name="2level",
                    templateId="3",
                    templateType="cisco_logging",
                    subTemplates=[],
                ),
                GeneralTemplate(name="1level", templateId="2", templateType="cisco_system", subTemplates=[]),
                GeneralTemplate(
                    name="1level",
                    templateId="4",
                    templateType="cisco_vpn",
                    subTemplates=[
                        GeneralTemplate(
                            name="2level",
                            templateId="5",
                            templateType="cisco_vpn_interface",
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name="2level",
                            templateId="6",
                            templateType="cedge_multicast",
                            subTemplates=[],
                        ),
                    ],
                ),
            ],
        )
