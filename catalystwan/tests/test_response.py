# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from typing import Any, List, Optional
from unittest.mock import patch

from attr import define, field  # type: ignore
from parameterized import parameterized  # type: ignore
from pydantic import BaseModel, Field, ValidationError
from requests.exceptions import JSONDecodeError

from catalystwan.dataclasses import DataclassBase
from catalystwan.response import ManagerErrorInfo, ManagerResponse
from catalystwan.typed_list import DataSequence


@define
class ParsedDataTypeAttrs(DataclassBase):
    key1: str
    key2: int
    key3: Optional[float] = field(default=None)


class ParsedDataTypePydanticV2(BaseModel):
    key1: str
    key2: int
    key3: Optional[float] = Field(default=None)


class DataForValidateTest(BaseModel):
    important: str
    not_important: ParsedDataTypePydanticV2


PARSE_DATASEQ_TEST_DATA: List = [
    (True, None, 0, "data"),
    (True, "string", 0, "data"),
    (True, {}, 0, "data"),
    (True, {"key1": "string", "key2": 12, "key3": 4.5}, 0, "data"),
    (True, 15, 0, "data"),
    (True, {"data": None}, 0, "data"),
    (True, {"data": {}}, 0, "data"),
    (False, {"data": []}, 0, "data"),
    (True, {"data": "something"}, 0, "data"),
    (False, {"data": {"key1": "string", "key2": 12, "key3": None}}, 1, "data"),
    (True, {"data": {"key1": "string", "key2": 12, "key3": None}}, 1, "other"),
    (False, {"other": {"key1": "string", "key2": 12, "key3": None}}, 1, "other"),
    (False, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}, 2, "data"),
    (True, {"headers": {"key1": 1, "key2": "two"}}, 0, "data"),
    (True, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}, 0, "data"),
]


PARSE_DATAOBJ_TEST_DATA: List = [
    (True, None, "data"),
    (True, "string", "data"),
    (True, {}, "data"),
    (True, {"data": "something"}, "data"),
    (False, {"data": {"key1": "string", "key2": 12, "key3": None}}, "data"),
    (True, {"data": {"key1": "string", "key2": 12, "key3": None}}, "other"),
    (False, {"other": {"key1": "string", "key2": 12, "key3": 55.13}}, "other"),
    (True, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}, "data"),
]

VALIDATE_DATASEQ_TEST_DATA = [
    {"important": "correct1", "not_important": {"invalid-key1": "string", "key2": "not int"}},
    {"important": "correct2", "not_important": {}},
]


class TestResponse(unittest.TestCase):
    @patch("requests.Response")
    def setUp(self, response_mock) -> None:
        self.response_mock = response_mock
        self.response_mock.headers = {"set-cookie": ""}
        self.response_mock.cookies = {}
        self.response_mock.status_code = 200

    @parameterized.expand(PARSE_DATASEQ_TEST_DATA)
    def test_dataseq_attrs(self, raises: bool, json: Any, expected_len: int, sourcekey: str):
        self.response_mock.json.return_value = json
        vmng_response = ManagerResponse(self.response_mock)
        if not raises:
            data_sequence = vmng_response.dataseq(ParsedDataTypeAttrs, sourcekey)
            assert isinstance(data_sequence, DataSequence)
            assert len(data_sequence) == expected_len
        else:
            with self.assertRaises(Exception):
                vmng_response.dataseq(ParsedDataTypeAttrs, sourcekey)

    @parameterized.expand(PARSE_DATASEQ_TEST_DATA)
    def test_dataseq_pydantic(self, raises: bool, json: Any, expected_len: int, sourcekey: str):
        self.response_mock.json.return_value = json
        vmng_response = ManagerResponse(self.response_mock)
        if not raises:
            data_sequence = vmng_response.dataseq(ParsedDataTypePydanticV2, sourcekey)
            assert isinstance(data_sequence, DataSequence)
            assert len(data_sequence) == expected_len
        else:
            with self.assertRaises(Exception):
                vmng_response.dataseq(ParsedDataTypePydanticV2, sourcekey)

    @parameterized.expand(PARSE_DATAOBJ_TEST_DATA)
    def test_dataobj_attrs(self, raises: bool, json: Any, sourcekey: str):
        self.response_mock.json.return_value = json
        vmng_response = ManagerResponse(self.response_mock)
        if not raises:
            data_object = vmng_response.dataobj(ParsedDataTypeAttrs, sourcekey)
            assert isinstance(data_object, ParsedDataTypeAttrs)
        else:
            with self.assertRaises(Exception):
                vmng_response.dataobj(ParsedDataTypeAttrs, sourcekey)

    @parameterized.expand(PARSE_DATAOBJ_TEST_DATA)
    def test_dataobj_pydantic(self, raises: bool, json: Any, sourcekey: str):
        self.response_mock.json.return_value = json
        vmng_response = ManagerResponse(self.response_mock)
        if not raises:
            data_object = vmng_response.dataobj(ParsedDataTypePydanticV2, sourcekey)
            assert isinstance(data_object, ParsedDataTypePydanticV2)
        else:
            with self.assertRaises(Exception):
                vmng_response.dataobj(ParsedDataTypePydanticV2, sourcekey)

    @parameterized.expand(
        [
            (True, "string"),
            (True, {}),
            (True, {"key1": "string", "key2": 12, "key3": 4.5}),
            (True, 15),
            (True, {"data": None}),
            (True, {"data": {}}),
            (True, {"data": []}),
            (True, {"data": "something"}),
            (True, {"data": {"key1": "string", "key2": 12, "key3": -0.7}}),
            (True, {"data": [{"key1": "string", "key2": 66}, {"key1": "required", "key2": 18, "key3": 0.1}]}),
            (True, {"headers": {"key1": 1, "key2": "two"}}),
            (False, {"error": {"message": "Error happened!", "details": "error details", "code": "ABC123"}}),
        ]
    )
    def test_get_error(self, empty_error: bool, json: Any):
        self.response_mock.json.return_value = json
        vmng_response = ManagerResponse(self.response_mock)
        error_info = vmng_response.get_error_info()
        assert isinstance(error_info, ManagerErrorInfo)
        if empty_error:
            assert error_info.message is None
            assert error_info.details is None
            assert error_info.code is None

    def test_dataobj_optional_validate(self):
        # Arrange
        self.response_mock.json.return_value = VALIDATE_DATASEQ_TEST_DATA[0]
        vmng_response = ManagerResponse(self.response_mock)
        # Act
        data = vmng_response.dataobj(DataForValidateTest, sourcekey=None, validate=False)
        # Assert
        assert isinstance(data, DataForValidateTest)
        assert data.important == VALIDATE_DATASEQ_TEST_DATA[0]["important"]
        with self.assertRaises(ValidationError):
            vmng_response.dataobj(DataForValidateTest, sourcekey=None, validate=True)

    def test_dataseq_optional_validate(self):
        self.response_mock.json.return_value = VALIDATE_DATASEQ_TEST_DATA
        vmng_response = ManagerResponse(self.response_mock)
        # Act
        dataseq = vmng_response.dataseq(DataForValidateTest, sourcekey=None, validate=False)
        # Assert
        assert isinstance(dataseq, DataSequence)
        for i, data in enumerate(dataseq):
            assert isinstance(data, DataForValidateTest)
            assert data.important == VALIDATE_DATASEQ_TEST_DATA[i]["important"]
        with self.assertRaises(ValidationError):
            vmng_response.dataseq(DataForValidateTest, sourcekey=None, validate=True)

    def test_dataseq_with_misisng_data(self):
        self.response_mock.json.side_effect = JSONDecodeError("test", "test", 1)
        vmng_response = ManagerResponse(self.response_mock)
        # Act
        dataseq = vmng_response.dataseq(DataForValidateTest, sourcekey="data", validate=True)
        # Assert
        assert isinstance(dataseq, DataSequence)
        assert len(dataseq) == 0
