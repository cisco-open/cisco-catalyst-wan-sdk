from copy import deepcopy

from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import T1E1SerialParcel


class T1E1SerialTemplateConverter:
    supported_template_types = ("vpn-interface-t1-e1",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> T1E1SerialParcel:
        values = deepcopy(template_values)
        print(values)
        return T1E1SerialParcel(parcel_name=name, parcel_description=description, **values)
