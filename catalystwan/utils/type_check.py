import uuid

from pydantic import ValidationError

from catalystwan.api.configuration_groups.parcel import Variable


def is_str_uuid(value: str) -> bool:
    try:
        uuid_ = uuid.UUID(value)
        return str(uuid_) == value or uuid_.hex == value
    except ValueError:
        return False


def is_str_variable(value: str) -> bool:
    try:
        Variable(value=value)
        return True
    except ValidationError:
        return False
