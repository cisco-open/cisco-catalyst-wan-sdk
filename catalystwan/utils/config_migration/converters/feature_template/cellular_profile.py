import logging
from copy import deepcopy
from typing import Dict, Literal, Optional

from catalystwan.api.configuration_groups.parcel import Global, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import (
    Authentication,
    AuthenticationType,
    CellularProfileParcel,
    NeedAuthentication,
    PdnType,
    ProfileConfig,
    ProfileInfo,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

from .base import FTConverter

logger = logging.getLogger(__name__)


class CellularProfileConverter(FTConverter):
    supported_template_types = ("cellular-cedge-profile",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> CellularProfileParcel:
        """
        Creates an CellularProfileParcel object based on the provided template values.

        Returns:
            CellularProfileParcel: A CellularProfileParcel object with the provided template values.
        """
        data = deepcopy(template_values)
        return CellularProfileParcel(
            parcel_name=name,
            parcel_description=description,
            profile_config=self.parse_profile_config(data),
        )

    def parse_profile_config(self, data: Dict) -> ProfileConfig:
        id_ = data.get("id")
        if not id_:
            raise CatalystwanConverterCantConvertException("Cellular Profile ID is required")
        return ProfileConfig(
            id=id_,
            profile_info=self.parse_profile_info(data),
        )

    def parse_profile_info(self, data: Dict) -> ProfileInfo:
        apn = data.get("apn")
        if not apn:
            raise CatalystwanConverterCantConvertException("APN is required")
        return ProfileInfo(
            apn=apn,
            no_overwrite=data.get("no_overwrite"),
            pdn_type=self.parse_pdn_type(data),
            authentication=self.parse_authentication(data),
        )

    def parse_pdn_type(self, data: Dict) -> Optional[Global[PdnType]]:
        pdn_type = data.get("pdn_type")
        if pdn_type:
            return as_global(pdn_type.value, PdnType)
        return None

    def parse_authentication(self, data: Dict) -> Optional[Authentication]:
        authentication = data.get("authentication")
        if not authentication:
            return None
        if authentication.value == "none":
            return Authentication(no_authentication=as_default("none", Literal["none"]))
        return Authentication(need_authentication=self.parse_need_authentication(data))

    def parse_need_authentication(self, data: Dict) -> NeedAuthentication:
        authentication = data.get("authentication")
        password = data.get("password")
        username = data.get("username")

        if password is None or username is None or authentication is None:
            raise CatalystwanConverterCantConvertException("Username, password and authentication type are required")

        type_ = as_global(authentication.value, AuthenticationType)
        logger.warning(f"Using encrypted password: {password}, change after migration is required")

        return NeedAuthentication(
            username=username,
            password=password,
            type=type_,
        )
