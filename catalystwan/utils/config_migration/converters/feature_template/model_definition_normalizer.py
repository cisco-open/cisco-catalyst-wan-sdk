from typing import Any, Dict, Literal, Optional, Union, get_args, get_origin

from pydantic.fields import FieldInfo

from catalystwan.api.configuration_groups.parcel import Global, Variable
from catalystwan.utils.config_migration.converters.feature_template.normalizer import to_snake_case


def is_global(annotation: Any):
    try:
        return issubclass(annotation, Global)
    except TypeError:
        return False


def try_cast_literal(cast_type, value) -> Optional[Union[str, int]]:
    literal_args = get_args(cast_type)
    if all(isinstance(v, str) for v in literal_args):
        if str(value) in literal_args:
            return str(value)
    if all(isinstance(v, int) for v in literal_args):
        if int(value) in literal_args:
            return int(value)
    if value in literal_args:
        return value
    return None


def try_cast_list(cast_type, value):
    list_args = get_args(cast_type)
    new_value = []
    if not isinstance(value, list):
        return None
    for v in value:
        for list_arg in list_args:
            list_value = try_cast(list_arg, v)
            if list_value is not None:
                break
        if list_value is not None:
            new_value.append(list_value)
        else:
            return None
    return new_value


def try_cast_bool(value: Union[str, bool, Any]) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        return None
    else:
        return None


def try_cast(cast_type: Any, value: Any) -> Optional[Any]:
    if get_origin(cast_type) is Literal:
        new_value = try_cast_literal(cast_type, value)
    elif get_origin(cast_type) is list:
        new_value = try_cast_list(cast_type, value)
    elif cast_type is bool:
        new_value = try_cast_bool(value)
    else:
        new_value = cast_type(value)
    return new_value


def normalize_to_model_definition(d: dict, model_fields: Dict[str, FieldInfo]) -> dict:
    """Attempts to cast fields into types given in model definition."""

    def get_global(field_info: FieldInfo):
        def extract_from_annotation(annotation):
            if get_origin(annotation) is Union:
                for nested_annotation in get_args(annotation):
                    extracted_value = extract_from_annotation(nested_annotation)
                    if is_global(extracted_value):
                        return extracted_value
            return annotation

        annotation = field_info.annotation
        return extract_from_annotation(annotation)

    def transform_value(value: Union[dict, list, str, int], field_info: FieldInfo) -> Any:
        global_type = get_global(field_info)
        if not is_global(global_type):
            # Unexpected type, don't cast
            return value
        cast_type = global_type.model_fields["value"].annotation

        if value is None:
            return value
        elif isinstance(value, Variable):
            return value
        elif isinstance(value, dict):
            # A nested model, skip
            return value
        elif isinstance(value, list):
            if get_origin(cast_type) is not list:
                return value
            if all(isinstance(v, dict) for v in value):
                # A list of nested models, skip
                return value

        if isinstance(value, Global):
            inner_value = value.value
        else:
            inner_value = value
        try:
            casted_value = try_cast(cast_type, inner_value)
            if casted_value is None:
                return value
            return global_type(value=casted_value)
        except ValueError:
            return value

    result = {}
    for key, val in d.items():
        try:
            result[to_snake_case(key)] = transform_value(val, model_fields[to_snake_case(key)])
        except KeyError:
            result[to_snake_case(key)] = val
    return result


def flatten_datapaths(original_dict: dict) -> dict:
    """
    Flattens datapaths. Conflicting leaf names within the same level need to be resolved manually beforehand.
    Does not attempt to traverse list values, since they're usually nested models.
    """

    def get_flattened_dict(
        original_dict: dict,
        flattened_dict: Optional[dict] = None,
    ):
        if flattened_dict is None:
            flattened_dict = {}
        for key, value in original_dict.items():
            if isinstance(value, dict):
                get_flattened_dict(value, flattened_dict)
            else:
                flattened_dict[key] = value
        return flattened_dict

    flattened_dict: dict = {}
    get_flattened_dict(original_dict, flattened_dict)
    return flattened_dict
