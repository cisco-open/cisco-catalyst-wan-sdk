# Copyright 2024 Cisco Systems, Inc. and its affiliates

import json
from typing import Any, List

from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.utils.feature_template.find_template_values import find_template_values


class TestFindTemplateValues(TestCaseBase):
    def test_find_template_value(self):
        # Arrange
        self.templates = self.session.api.templates._get_feature_templates(summary=False)
        # Act, Assert
        for template in self.templates:
            definition = json.loads(template.template_definition)
            with self.subTest(template_name=template.name):
                parsed_values = find_template_values(definition)
                self.assertFalse(
                    self.is_key_present(parsed_values, ["vipType", "vipValue", "vipVariableName", "vipObjectType"])
                )

    def is_key_present(self, d: dict, keys: List[Any]):
        """
        Checks if any key from keys is present within the dictionary d
        """
        for key, value in d.items():
            if key in keys:
                return True
            if isinstance(value, dict):
                if self.is_key_present(value, keys):
                    return True
            if isinstance(value, list):
                for v in value:
                    if isinstance(v, dict):
                        if self.is_key_present(v, keys):
                            return True
        return False
