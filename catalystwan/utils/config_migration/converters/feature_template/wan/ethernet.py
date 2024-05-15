from copy import deepcopy
from typing import Dict, List

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.common import EncapType
from catalystwan.models.configuration.feature_profile.common import Encapsulation
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    InterfaceEthernetParcel,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.config_migration.steps.constants import WAN_VPN_ETHERNET


class WanInterfaceEthernetTemplateConverter:
    supported_template_types = (WAN_VPN_ETHERNET,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthernetParcel:
        data = deepcopy(template_values)
        print(data)

        encapsulation = self.parse_encapsulations(data.get("tunnel_interface", {}).get("encapsulation", []))

        payload = create_dict_without_none(
            name=name,
            description=description,
            encapsulation=encapsulation,
        )

        return InterfaceEthernetParcel(**payload)

    def parse_encapsulations(self, encapsulation: List[Dict]) -> List[Encapsulation]:
        return [self.create_encapsulation(encap) for encap in encapsulation]

    def create_encapsulation(self, encapsulation: Dict) -> Encapsulation:
        if encap := encapsulation.get("encap"):
            encap = as_global(encap.value, EncapType)
        return Encapsulation(
            preference=encapsulation.get("preference"),
            weight=encapsulation.get("weight"),
            encap=encap,
        )
