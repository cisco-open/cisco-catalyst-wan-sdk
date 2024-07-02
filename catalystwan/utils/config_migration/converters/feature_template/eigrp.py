from copy import deepcopy
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Default, as_default, as_global, as_variable
from catalystwan.models.configuration.feature_profile.common import AddressWithMask
from catalystwan.models.configuration.feature_profile.sdwan.service import EigrpParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.eigrp import (
    AddressFamily,
    EigrpAuthentication,
    IPv4StaticRoute,
    RedistributeIntoEigrp,
    RedistributeProtocol,
    SummaryAddress,
    TableMap,
)

from .base import FTConverter


class EigrpConverter(FTConverter):
    supported_template_types = ("eigrp",)

    delete_keys = ("as_num",)

    # Default values
    lan_eigrp_auto_syst_id = "{{lan_eigrp_auto_syst_id}}"
    lan_eigrp_addr_fami_netw_1_ip = "{{lan_eigrp_addr_fami_netw_1_ip}}"
    lan_eigrp_addr_fami_netw_1_mask = "{{lan_eigrp_addr_fami_netw_1_mask}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> EigrpParcel:
        values = self.prepare_values(template_values)
        self.configure_as_number(values)
        self.configure_address_family_interface(values)
        self.configure_address_family(values)
        self.configure_authentication(values)
        self.configure_table_map(values)
        self.cleanup_keys(values)
        return EigrpParcel(parcel_name=name, parcel_description=description, **values)

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)["eigrp"]

    def configure_as_number(self, values: dict) -> None:
        values["as_number"] = values.pop("as_num", as_variable(self.lan_eigrp_auto_syst_id))

    def configure_address_family(self, values: dict) -> None:
        address_family = values.get("address_family", [])  # feature template sends list instead of dict
        if not address_family:
            return
        address_family = address_family[0]
        values["address_family"] = AddressFamily(
            redistribute=self._set_redistribute(address_family),
            network=self._set_adress_family_addresses(address_family),
        )

    def _set_adress_family_addresses(self, values: dict) -> List[SummaryAddress]:
        summary_address = values.get("network", [])
        if not summary_address:
            return [
                SummaryAddress(
                    prefix=AddressWithMask(
                        address=as_variable(self.lan_eigrp_addr_fami_netw_1_ip),
                        mask=as_variable(self.lan_eigrp_addr_fami_netw_1_mask),
                    )
                )
            ]
        return [self._set_summary_address(addr) for addr in summary_address]

    def _set_redistribute(self, values: dict) -> Optional[List[RedistributeIntoEigrp]]:
        redistributes = values.get("topology", {}).get("base", {}).get("redistribute", [])
        if not redistributes:
            return None
        return [
            RedistributeIntoEigrp(
                protocol=as_global(redistribute["protocol"].value, RedistributeProtocol),
                # route_policy=redistribute.get("route_policy", None),
                # route polict is represented as a string in feature template and as UUID in model
            )
            for redistribute in redistributes
        ]

    def configure_address_family_interface(self, values: dict) -> None:
        interfaces = values.get("af_interface", [])
        if not interfaces:
            return
        interfaces_list = []
        for interface in interfaces:
            interfaces_list.append(
                IPv4StaticRoute(
                    name=interface["name"],
                    shutdown=interface.get("shutdown", as_default(False)),
                    summary_address=self._set_summary_addresses(interface),
                )
            )
        values["af_interface"] = interfaces_list

    def _set_summary_addresses(self, values: dict) -> List[SummaryAddress]:
        summary_address = values.get("summary_address", [])
        return [self._set_summary_address(addr) for addr in summary_address]

    def _set_summary_address(self, addr: dict) -> SummaryAddress:
        return SummaryAddress(
            prefix=AddressWithMask(
                address=as_global(addr["prefix"].value.network.network_address),
                mask=as_global(str(addr["prefix"].value.netmask)),
            )
        )

    def configure_authentication(self, values: dict) -> None:
        auth = values.get("authentication", None)
        if not auth:
            return
        values["authentication"] = EigrpAuthentication(
            auth_type=auth.get("type", Default[None](value=None)),
            auth_key=auth.get("key", Default[None](value=None)),
            key=auth.get("keychain", {}).get("key", None),
            # There should be more keys
        )

    def configure_table_map(self, values: dict) -> None:
        table_map = values.get("table_map", None)
        if not table_map:
            return
        values["table_map"] = TableMap(
            # name=table_map.get("name", Default[None](value=None)), this should be Global[UUID] not Global[int]
            filter=table_map.get("filter", as_default(False)),
        )

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
