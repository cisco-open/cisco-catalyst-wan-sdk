from copy import deepcopy

from catalystwan.models.configuration.feature_profile.sdwan.cli.config import ConfigParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

from .base import FTConverter


class CliConverter(FTConverter):
    supported_template_types = ("cli-template",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> ConfigParcel:
        data = deepcopy(template_values)
        config = data.get("config")
        if not config:
            raise CatalystwanConverterCantConvertException("Config is required")
        config = config.value
        return ConfigParcel(
            parcel_name=name,
            parcel_description=description,
            config=config,
        )
