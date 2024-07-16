# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest

from parameterized import parameterized  # type: ignore

from catalystwan.api.templates.models.supported import available_models
from catalystwan.utils.feature_template.choose_model import choose_model

# For "cisco_secure_internet_gateway" there are required values


class TestChooseModel(unittest.TestCase):
    @parameterized.expand(
        [
            (key, value)
            for key, value in available_models.items()
            if key not in ["cisco_secure_internet_gateway", "vpn_vsmart"]  # required values
        ]
    )
    def test_choose_model(self, model_type, model_cls):
        # Arrange
        name = "My model name"
        description = "My model description"
        model_from_cls = model_cls(template_name=name, template_description=description)

        # Act
        chosen_model = choose_model(model_type)
        model_from_choice = chosen_model(template_name=name, template_description=description)

        # Assert
        self.assertEqual(model_from_choice, model_from_cls)
