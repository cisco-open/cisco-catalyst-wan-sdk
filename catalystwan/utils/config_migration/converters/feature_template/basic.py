from copy import deepcopy
from typing import Dict, Optional

from catalystwan.api.configuration_groups.parcel import Global, OptionType, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import (
    Clock,
    ConsoleBaudRate,
    GeoFencing,
    GpsVariable,
    Sms,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.timezone import Timezone

from .base import FTConverter


class SystemToBasicConverter(FTConverter):
    supported_template_types = ("cisco_system", "system-vsmart", "system-vedge")

    def create_parcel(self, name: str, description: str, template_values: dict) -> BasicParcel:
        """
        Converts the provided template values into a BasicParcel object.

        Args:
            name (str): The name of the BasicParcel.
            description (str): The description of the BasicParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BasicParcel: A BasicParcel object with the provided template values.
        """
        data = deepcopy(template_values)

        track_default_gateway = data.get("track_default_gateway")
        clock = self.parse_clock(data)
        console_baud_rate = self.parse_console_baud_rate(data)
        gps_location = self.parse_gps_location(data)
        port_offset = data.get("port_offset")

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            track_default_gateway=track_default_gateway,
            clock=clock,
            console_baud_rate=console_baud_rate,
            gps_location=gps_location,
            port_offset=port_offset,
        )

        return BasicParcel(**payload)

    def parse_clock(self, data: Dict) -> Clock:
        timezone = data.get("timezone")
        if timezone:
            return Clock(timezone=Global[Timezone](value=timezone))
        return Clock()

    def parse_console_baud_rate(self, data: Dict) -> Optional[Global[ConsoleBaudRate]]:
        baud_rate = data.get("console_baud_rate")
        if not baud_rate:
            return None
        if baud_rate.option_type == OptionType.VARIABLE:
            return baud_rate
        return Global[ConsoleBaudRate](value=baud_rate.value)

    def parse_gps_location(self, data: Dict) -> GpsVariable:
        gps_location = data.get("gps_location")
        if not gps_location:
            return GpsVariable()

        payload = create_dict_without_none(
            longitude=gps_location.get("longitude"),
            latitude=gps_location.get("latitude"),
            geo_fencing=self.parse_geo_fencing(data),
        )

        return GpsVariable(**payload)

    def parse_geo_fencing(self, data: Dict) -> GeoFencing:
        mobile_number = data.get("mobile_number", [])
        if mobile_number:
            return GeoFencing(
                enable=as_global(True),
                range=data.get("range", as_default(100)),
                sms=Sms(
                    enable=as_global(True),
                    mobile_number=mobile_number,
                ),
            )
        return GeoFencing()
