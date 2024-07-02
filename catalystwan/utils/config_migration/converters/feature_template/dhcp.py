import logging
from copy import deepcopy
from ipaddress import IPv4Address
from typing import Dict, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    AddressPool,
    LanVpnDhcpServerParcel,
    OptionCode,
    StaticLeaseItem,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none

from .base import FTConverter

logger = logging.getLogger(__name__)


class DhcpConverter(FTConverter):
    supported_template_types = ("dhcp", "cisco_dhcp_server", "dhcp-server")

    variable_address_pool = "{{dhcp_1_addressPool_networkAddress}}"
    variable_subnet_mask = "{{dhcp_1_addressPool_subnetMask}}"
    variable_mac_address = "{{{{dhcp_1_staticLease_{}_macAddress}}}}"
    variable_ip = "{{{{dhcp_1_staticLease_{}_ip}}}}"

    def create_parcel(self, name: str, description: str, template_values: dict) -> LanVpnDhcpServerParcel:
        """
        Create a LanVpnDhcpServerParcel object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): The template values used to populate the parcel.

        Returns:
            LanVpnDhcpServerParcel: The created LanVpnDhcpServerParcel object.

        """

        data = deepcopy(template_values)
        data.update(data.pop("options", {}))
        dns_servers = self.parse_str_list_to_ipv4_list(data.get("dns_servers", []))
        tftp_servers = self.parse_str_list_to_ipv4_list(data.get("tftp_servers", []))
        address_pool = self.parse_address_pool(data)
        static_lease = self.parse_static_lease(data)
        exclude = data.get("exclude")
        lease_time = data.get("lease_time")
        domain_name = data.get("domain_name")
        default_gateway = data.get("default_gateway")
        domain_name = data.get("domain_name")
        option_code = self.parse_option_code(data.get("option_code", []))
        interface_mtu = data.get("interface_mtu")

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            address_pool=address_pool,
            static_lease=static_lease,
            exclude=exclude,
            lease_time=lease_time,
            domain_name=domain_name,
            default_gateway=default_gateway,
            dns_servers=dns_servers,
            tftp_servers=tftp_servers,
            option_code=option_code,
            interface_mtu=interface_mtu,
        )

        return LanVpnDhcpServerParcel(**payload)

    def parse_address_pool(self, data: Dict) -> AddressPool:
        address_pool = data.get("address_pool")
        if not address_pool:
            raise CatalystwanConverterCantConvertException("No address pool specified for DHCP server parcel.")

        if isinstance(address_pool, Variable):
            return AddressPool(
                network_address=address_pool,
                subnet_mask=address_pool,
            )

        return AddressPool(
            network_address=as_global(address_pool.value.network.network_address),
            subnet_mask=as_global(str(address_pool.value.netmask), SubnetMask),
        )

    def parse_static_lease(self, data: Dict) -> Optional[List[StaticLeaseItem]]:
        return [
            StaticLeaseItem(
                mac_address=lease.get("mac_address"),
                ip=lease.get("ip"),
            )
            for lease in data.get("static_lease", [])
        ]

    def parse_str_list_to_ipv4_list(
        self, data: Global[List[str]]
    ) -> Optional[Union[Global[List[IPv4Address]], Variable]]:
        if not data:
            return None
        if isinstance(data, Variable):
            return data
        return Global[List[IPv4Address]](value=[IPv4Address(ip) for ip in data.value])

    def parse_option_code(self, data: List[Dict[str, str]]) -> List[OptionCode]:
        return [
            OptionCode(
                **create_dict_without_none(
                    code=entry.get("code"),
                    ip=self.parse_str_list_to_ipv4_list(entry.get("ip")),  # type: ignore
                    ascii=entry.get("ascii"),
                    hex=entry.get("hex"),
                )
            )
            for entry in data
        ]
