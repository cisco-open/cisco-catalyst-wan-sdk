import functools
from typing import Optional
from uuid import UUID

from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


def handle_build_report(func):
    """Wrapper to make creating raport simple and keep it DRY."""

    @functools.wraps(func)
    def wrapper(self, profile_uuid: UUID, parcel: AnyParcel, *args, **kwargs) -> Optional[UUID]:
        try:
            uuid = func(self, profile_uuid, parcel, *args, **kwargs)
            self.build_raport.add_created_parcel(parcel.parcel_name, uuid)
            return uuid
        except ManagerHTTPError as e:
            self.build_raport.add_failed_parcel(
                parcel_name=parcel.parcel_name,
                parcel_type=parcel._get_parcel_type(),
                error_info=e.info,
                request=e.request,
            )
            return None

    return wrapper
