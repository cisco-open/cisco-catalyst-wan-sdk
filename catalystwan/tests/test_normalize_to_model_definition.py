import unittest
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import List, Literal, Optional, Union

from parameterized import parameterized  # type: ignore
from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.utils.config_migration.converters.feature_template.model_definition_normalizer import (
    normalize_to_model_definition,
)

IntLiteral = Literal[2, 4, 8, 16]
StrLiteral = Literal["1", "2", "3"]


class ExampleModelField(BaseModel):
    field_1: Union[Variable, Default[str], Global[str]]


class ExampleParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["example"] = Field(default="example", frozen=True, exclude=True)

    str_field: Union[Variable, Default[str], Global[str]] = Field()
    int_field: Union[Variable, Default[int], Global[int]] = Field()
    bool_field: Union[Variable, Default[bool], Global[bool]] = Field()
    list_field: Union[Variable, Default[List[int]], Global[List[int]]] = Field()
    ipv4_address_field: Union[Variable, Default[IPv4Address], Global[IPv4Address]] = Field()
    ipv4_interface_field: Union[Variable, Default[IPv4Interface], Global[IPv4Interface]]
    ipv6_address_field: Union[Variable, Default[IPv6Address], Global[IPv6Address]] = Field()
    ipv6_interface_field: Union[Variable, Default[IPv6Interface], Global[IPv6Interface]]
    int_literal_field: Union[Variable, Default[IntLiteral], Global[IntLiteral]] = Field()
    str_literal_field: Union[Variable, Default[StrLiteral], Global[StrLiteral]] = Field()
    optional_field: Optional[Union[Variable, Default[int], Global[int]]] = Field()
    model_field: ExampleModelField = Field()
    model_field_list: List[ExampleModelField] = Field()


class TestNormalizeToModelDefinition(unittest.TestCase):
    @parameterized.expand(
        [
            ({"str_field": "str"}, {"str_field": Global[str](value="str")}),
            ({"str_field": 12}, {"str_field": Global[str](value="12")}),
            (
                {"str_field": Global[IPv4Address](value=IPv4Address("10.0.0.1"))},
                {"str_field": Global[str](value="10.0.0.1")},
            ),
            ({"str_field": Global[str](value="str")}, {"str_field": Global[str](value="str")}),
        ]
    )
    def test_str_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"int_field": 12}, {"int_field": Global[int](value=12)}),
            ({"int_field": "12"}, {"int_field": Global[int](value=12)}),
            ({"int_field": Global[int](value=12)}, {"int_field": Global[int](value=12)}),
        ]
    )
    def test_int_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"bool_field": True}, {"bool_field": Global[bool](value=True)}),
            ({"bool_field": "false"}, {"bool_field": Global[bool](value=False)}),
            ({"bool_field": Global[bool](value=True)}, {"bool_field": Global[bool](value=True)}),
            ({"bool_field": 123}, {"bool_field": 123}),
            ({"bool_field": "non_bool_str"}, {"bool_field": "non_bool_str"}),
        ]
    )
    def test_bool_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"list_field": ["12", "13", "14"]}, {"list_field": Global[List[int]](value=[12, 13, 14])}),
            ({"list_field": [12, 13, 14]}, {"list_field": Global[List[int]](value=[12, 13, 14])}),
            ({"list_field": ["12", "13", "a"]}, {"list_field": ["12", "13", "a"]}),
        ]
    )
    def test_list_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            (
                {"ipv4_address_field": "10.0.0.1"},
                {"ipv4_address_field": Global[IPv4Address](value=IPv4Address("10.0.0.1"))},
            ),
            ({"ipv4_address_field": "10.0.0.1/32"}, {"ipv4_address_field": "10.0.0.1/32"}),
            (
                {"ipv4_address_field": Global[IPv4Address](value=IPv4Address("10.0.0.1"))},
                {"ipv4_address_field": Global[IPv4Address](value=IPv4Address("10.0.0.1"))},
            ),
        ]
    )
    def test_ipv4_address_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            (
                {"ipv4_interface_field": "10.0.0.1"},
                {"ipv4_interface_field": Global[IPv4Interface](value=IPv4Interface("10.0.0.1/32"))},
            ),
            (
                {"ipv4_interface_field": "10.0.0.1/32"},
                {"ipv4_interface_field": Global[IPv4Interface](value=IPv4Interface("10.0.0.1/32"))},
            ),
            (
                {"ipv4_interface_field": Global[IPv4Interface](value=IPv4Interface("10.0.0.1/32"))},
                {"ipv4_interface_field": Global[IPv4Interface](value=IPv4Interface("10.0.0.1/32"))},
            ),
        ]
    )
    def test_ipv4_interface_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            (
                {"ipv6_address_field": "::3e46"},
                {"ipv6_address_field": Global[IPv6Address](value=IPv6Address("::3e46"))},
            ),
            ({"ipv6_address_field": "::3e46/64"}, {"ipv6_address_field": "::3e46/64"}),
            (
                {"ipv6_address_field": Global[IPv6Address](value=IPv6Address("::3e46"))},
                {"ipv6_address_field": Global[IPv6Address](value=IPv6Address("::3e46"))},
            ),
        ]
    )
    def test_ipv6_address_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            (
                {"ipv6_interface_field": "::3e46"},
                {"ipv6_interface_field": Global[IPv6Interface](value=IPv6Interface("::3e46/128"))},
            ),
            (
                {"ipv6_interface_field": "::3e46/64"},
                {"ipv6_interface_field": Global[IPv6Interface](value=IPv6Interface("::3e46/64"))},
            ),
            (
                {"ipv6_interface_field": Global[IPv6Interface](value=IPv6Interface("::3e46/64"))},
                {"ipv6_interface_field": Global[IPv6Interface](value=IPv6Interface("::3e46/64"))},
            ),
        ]
    )
    def test_ipv6_interface_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"str_literal_field": "1"}, {"str_literal_field": Global[StrLiteral](value="1")}),
            ({"str_literal_field": "4"}, {"str_literal_field": "4"}),
            ({"str_literal_field": 1}, {"str_literal_field": Global[StrLiteral](value="1")}),
            ({"str_literal_field": 4}, {"str_literal_field": 4}),
        ]
    )
    def test_str_literal_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"int_literal_field": 4}, {"int_literal_field": Global[IntLiteral](value=4)}),
            ({"int_literal_field": 6}, {"int_literal_field": 6}),
            ({"int_literal_field": "4"}, {"int_literal_field": Global[IntLiteral](value=4)}),
            ({"int_literal_field": "6"}, {"int_literal_field": "6"}),
        ]
    )
    def test_int_literal_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"model_field": {"field_1": "test"}}, {"model_field": {"field_1": "test"}}),
        ]
    )
    def test_model_field_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            ({"model_field": [{"field_1": "test"}]}, {"model_field": [{"field_1": "test"}]}),
        ]
    )
    def test_model_list_field_cast(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)

    @parameterized.expand(
        [
            (
                {"model_field": [{"field_1": Variable(value="{{variable}}")}]},
                {"model_field": [{"field_1": Variable(value="{{variable}}")}]},
            ),
        ]
    )
    def test_skip_variable(self, definition, expected):
        normalized_definition = normalize_to_model_definition(definition, ExampleParcel.model_fields)

        self.assertDictEqual(normalized_definition, expected)
