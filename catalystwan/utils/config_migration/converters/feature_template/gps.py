from copy import deepcopy
from typing import Dict, Optional

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsMode, GpsParcel
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none

from .base import FTConverter


class GpsConverter(FTConverter):
    supported_template_types = ("cellular-cedge-gps-controller",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> GpsParcel:
        """
        Creates an GpsParcel object based on the provided template values.

        Returns:
            GpsParcel: A GpsParcel object with the provided template values.
        """
        data = deepcopy(template_values)

        gps_data = data.get("gps", {})
        nmea_data = data.get("nmea", {}).get("ip", {}).get("udp", {})

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            enable=gps_data.get("enable"),
            mode=self.parse_mode(gps_data),
            nmea=gps_data.get("nmea_conf", {}).get("nmea"),
            source_address=nmea_data.get("source_address"),
            destination_address=nmea_data.get("destination_address"),
            destination_port=nmea_data.get("destination_port"),
        )

        return GpsParcel(**payload)

    def parse_mode(self, gps_data: Dict) -> Optional[Global[GpsMode]]:
        mode = gps_data.get("mode")
        if mode:
            return Global[GpsMode](value=mode.value)
        return None
