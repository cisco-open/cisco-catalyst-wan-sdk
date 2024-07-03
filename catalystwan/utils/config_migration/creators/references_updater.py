import logging
from typing import Dict, TypeVar
from uuid import UUID

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def update_parcel_references(parcel: T, uuid_map: Dict[UUID, UUID]) -> T:
    """
    Replaces UUID strings found in json dump based on provided map
    always returns a copy of original even when there was no substitution
    always perform output validation
    """
    target_dump = parcel.model_dump_json(by_alias=True)
    pattern = '"{}"'

    for origin_uuid, target_uuid in uuid_map.items():
        origin_uuid_str = pattern.format(str(origin_uuid))
        target_uuid_str = pattern.format(str(target_uuid))
        target_dump = target_dump.replace(origin_uuid_str, target_uuid_str)

    try:
        return parcel.model_validate_json(target_dump)
    except ValidationError as e:
        logging.error(f"Cannot validate model after references update: {e}")
        raise e
