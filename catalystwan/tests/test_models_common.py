# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest
from typing import Any, Dict, Set

from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, SerializationInfo, SerializerFunctionWrapHandler, model_serializer
from typing_extensions import Annotated

from catalystwan.models.common import VersionedField

A = Annotated[
    int, VersionedField(versions=">=1", serialization_alias="a-kebab"), Field(default=0, serialization_alias="aCamel")
]

B = Annotated[
    float,
    VersionedField(versions=">=2", serialization_alias="b-kebab"),
]


class VersionedFieldsModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    a: A
    b: B = Field(default=0.0, serialization_alias="bCamel")
    c: Annotated[bool, VersionedField(versions=">=3", serialization_alias="c-kebab")] = False

    @model_serializer(mode="wrap")
    def dump(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> Dict[str, Any]:
        return VersionedField.dump(self.model_fields, handler(self), info)


class Payload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: VersionedFieldsModel


class TestModelsCommonVersionedField(unittest.TestCase):
    def setUp(self):
        self.model = Payload(data=VersionedFieldsModel())

    @parameterized.expand(
        [
            ("0.9", {"aCamel", "bCamel", "c"}),
            ("1.0", {"a-kebab", "bCamel", "c"}),
            ("2.1", {"a-kebab", "b-kebab", "c"}),
            ("3.0.1", {"a-kebab", "b-kebab", "c-kebab"}),
        ]
    )
    def test_versioned_field_model_serialize(self, version: str, expected_fields: Set[str]):
        data_dict = self.model.model_dump(by_alias=True, context={"api_version": Version(version)}).get("data")
        assert expected_fields == data_dict.keys()
