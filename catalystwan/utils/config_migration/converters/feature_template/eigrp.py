from copy import deepcopy

from catalystwan.models.configuration.feature_profile.sdwan.service import EigrpParcel


class EigrpTemplateConverter:
    supported_template_types = ("eigrp",)

    delete_keys = ("as_num",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> EigrpParcel:
        values = self.prepare_values(template_values)
        self.configure_as_number(values)
        self.cleanup_keys(values)
        return EigrpParcel(parcel_name=name, parcel_description=description, **values)

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)["eigrp"]

    def configure_as_number(self, values: dict) -> None:
        values["as_number"] = values.pop("as_num")

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
