import unittest
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo


class TestDeviceTemplate(unittest.TestCase):
    def setUp(self):
        self.sig_uuid = (
            uuid4()
        )  # We need to generate a UUID for the SIG template to test the get_sig_template_uuid method
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
            general_templates=[
                # Flat - stays flat
                GeneralTemplate(name="1level", template_id="1", template_type="cedge_aaa", sub_templates=[]),
                # No relation between system and logging in the UX2 - flatten them
                GeneralTemplate(
                    name="1level",
                    template_id="2",
                    template_type="cisco_system",
                    sub_templates=[
                        GeneralTemplate(
                            name="2level",
                            template_id="3",
                            template_type="cisco_logging",
                            sub_templates=[],
                        ),
                    ],
                ),
                # Cisco VPN - keep the structure
                GeneralTemplate(
                    name="1level",
                    template_id="4",
                    template_type="cisco_vpn",
                    sub_templates=[
                        GeneralTemplate(
                            name="2level",
                            template_id="5",
                            template_type="cisco_vpn_interface",
                            sub_templates=[],
                        ),
                        GeneralTemplate(
                            name="2level",
                            template_id="6",
                            template_type="cedge_multicast",
                            sub_templates=[],
                        ),
                        GeneralTemplate(
                            name="2level - SIG Temaplte",
                            template_id=str(self.sig_uuid),
                            template_type="cisco_secure_internet_gateway",
                            sub_templates=[],
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
                GeneralTemplate(name="1level", template_id="1", template_type="cedge_aaa", sub_templates=[]),
                GeneralTemplate(
                    name="2level",
                    template_id="3",
                    template_type="cisco_logging",
                    sub_templates=[],
                ),
                GeneralTemplate(name="1level", template_id="2", template_type="cisco_system", sub_templates=[]),
                GeneralTemplate(
                    name="1level",
                    template_id="4",
                    template_type="cisco_vpn",
                    sub_templates=[
                        GeneralTemplate(
                            name="2level",
                            template_id="5",
                            template_type="cisco_vpn_interface",
                            sub_templates=[],
                        ),
                        GeneralTemplate(
                            name="2level",
                            template_id="6",
                            template_type="cedge_multicast",
                            sub_templates=[],
                        ),
                        GeneralTemplate(
                            name="2level - SIG Temaplte",
                            template_id=str(self.sig_uuid),
                            template_type="cisco_secure_internet_gateway",
                            sub_templates=[],
                        ),
                    ],
                ),
            ],
        )

    def test_when_sig_template_is_assigned_expect_correct_uuid(self):
        # Act, Assert
        self.assertEqual(self.device_template.get_sig_template_uuid(), self.sig_uuid)

    def test_when_sig_template_is_not_assigned_expect_correct_none(self):
        # Arrange
        self.device_template.general_templates[2].sub_templates = []

        # Act, Assert
        self.assertIsNone(self.device_template.get_sig_template_uuid())
