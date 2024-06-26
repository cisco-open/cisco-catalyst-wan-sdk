from copy import deepcopy
from typing import Dict, List

from catalystwan.models.configuration.feature_profile.sdwan.system import NtpParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.ntp import (
    Authentication,
    AuthenticationVariable,
    Leader,
    ServerItem,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none

from .base import FTConverter


class NtpConverter(FTConverter):
    supported_template_types = ("cisco_ntp", "ntp")

    def create_parcel(self, name: str, description: str, template_values: dict) -> NtpParcel:
        """
        Creates an NtpParcel object based on the provided template values.

        Returns:
            NtpParcel: An NtpParcel object with the provided template values.
        """
        data = deepcopy(template_values)

        leader = self.parse_leader(data.get("master", {}))
        server = self.parse_server_items(data.get("server", []))
        authentication = self.parse_authentication(data.get("keys", {}))

        return NtpParcel(
            parcel_name=name,
            parcel_description=description,
            server=server,
            authentication=authentication,
            leader=leader,
        )

    def parse_server_items(self, server_data: List[Dict]) -> List[ServerItem]:
        return [ServerItem(**data) for data in server_data]

    def parse_authentication(self, keys: Dict) -> Authentication:
        trusted_keys = keys.get("trusted")
        authentication_keys = self.parse_authentication_keys(keys.get("authentication", []))

        return Authentication(trusted_keys=trusted_keys, authentication_keys=authentication_keys)

    def parse_authentication_keys(self, key_data: List[Dict]) -> List[AuthenticationVariable]:
        return [
            AuthenticationVariable(
                key_id=data["number"],
                md5_value=data["md5"],
            )
            for data in key_data
        ]

    def parse_leader(self, leader_data: Dict) -> Leader:
        if not leader_data:
            return Leader()

        payload = create_dict_without_none(
            enable=leader_data.get("enable"),
            stratum=leader_data.get("stratum"),
            source=leader_data.get("source"),
        )

        return Leader(**payload)
