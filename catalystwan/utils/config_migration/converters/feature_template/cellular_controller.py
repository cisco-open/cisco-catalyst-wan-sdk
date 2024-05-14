from copy import deepcopy
from typing import Dict

from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
    ControllerConfig,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


class CellularControllerTemplateConverter:
    supported_template_types = ("cellular-cedge-controller",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> CellularControllerParcel:
        """
        Creates an CellularControllerParcel object based on the provided template values.

        Returns:
            CellularControllerParcel: A CellularControllerParcel object with the provided template values.
        """
        data = deepcopy(template_values)
        return CellularControllerParcel(
            parcel_name=name, parcel_description=description, controller_config=self.parse_controller_config(data)
        )

    def parse_controller_config(self, data: Dict) -> ControllerConfig:
        _id = data.get("id")
        if not _id:
            raise CatalystwanConverterCantConvertException("Cellular ID is required")
        lte = data.get("lte", {})
        sim = lte.get("sim", {})
        primary = sim.get("primary", {})
        slot = primary.get("slot")
        max_retry = sim.get("max_retry")
        failovertimer = lte.get("failovertimer")

        return ControllerConfig(id=_id, slot=slot, max_retry=max_retry, failover_timer=failovertimer)
