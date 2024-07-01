# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from copy import deepcopy
from ipaddress import IPv4Interface
from typing import Dict, List, Optional, Union
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.routing import RoutingBgpParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.bgp import (
    AddressFamily,
    AddressFamilyItem,
    AggregateAddres,
    Ipv6NeighborItem,
    NeighborItem,
    NetworkItem,
    RedistributeItem,
    RedistributeProtocol,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.config_migration.steps.constants import LAN_BGP, WAN_BGP

from .base import FTConverter

logger = logging.getLogger(__name__)


class BgpRoutingConverter(FTConverter):
    supported_template_types = (WAN_BGP, LAN_BGP)

    def create_parcel(self, name: str, description: str, template_values: dict) -> RoutingBgpParcel:
        """
        Creates a RoutingBgpParcel object based on the provided template values.

        Args:
            name (str): The name of the RoutingBgpParcel.
            description (str): The description of the RoutingBgpParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            RoutingBgpParcel: A RoutingBgpParcel object with the provided template values.
        """

        data = deepcopy(template_values)

        # Some templates have bgp in the root level
        # The templates values can have diffrent structure
        # we try to flatten the values to a single level

        bgp = data.pop("bgp", {})
        data = {**data, **bgp}

        distance = data.pop("distance", {})
        data = {**data, **distance}

        timers = data.pop("timers", {})
        data = {**data, **timers}

        best_path = data.pop("best_path", {})
        med = best_path.pop("med", {})
        as_path = best_path.pop("as_path", {})
        data = dict(**data, **best_path, **med, **as_path)

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            as_num=data.get("as_num"),
            router_id=data.get("router_id"),
            propagate_aspath=data.get("propagate_aspath"),
            propagate_community=data.get("propagate_community"),
            external=data.get("external"),
            internal=data.get("internal"),
            local=data.get("local"),
            holdtime=self.parse_holdtime(data.get("holdtime")),
            keepalive=data.get("keepalive"),
            always_compare=data.get("always_compare"),
            deterministic=data.get("deterministic"),
            missing_as_worst=data.get("missing_as_worst"),
            compare_router_id=data.get("compare_router_id"),
            multipath_relax=data.get("multipath_relax"),
            address_family=self.parse_address_family(data.get("address_family", [])),
            neighbor=self.parse_neighbor(data.get("neighbor", [])),
            ipv6_neighbor=self.parse_neighbor_ipv6(data.get("ipv6_neighbor", [])),
        )

        return RoutingBgpParcel(**payload)

    def parse_holdtime(
        self, holdtime: Optional[Union[Global[str], Variable]]
    ) -> Optional[Union[Global[int], Variable]]:
        if not holdtime:
            return None

        if isinstance(holdtime, Global):
            return Global[int](value=int(holdtime.value))
        return holdtime

    def parse_neighbor(self, neighbors: List[Dict]) -> Optional[List[NeighborItem]]:
        if not neighbors:
            return None

        items = []
        for neighbor in neighbors:
            address = neighbor.get("address")
            remote_as = neighbor.get("remote_as")
            if not address or not remote_as:
                # Skip to not lose whole conversion
                continue

            ni = NeighborItem(
                address=address,
                description=neighbor.get("description"),
                shutdown=neighbor.get("shutdown"),
                remote_as=remote_as,
                local_as=neighbor.get("local_as"),
                keepalive=neighbor.get("timers", {}).get("keepalive"),
                holdtime=neighbor.get("timers", {}).get("holdtime"),
                if_name=neighbor.get("if_name"),
                next_hop_self=neighbor.get("next_hop_self"),
                send_community=neighbor.get("send_community"),
                send_ext_community=neighbor.get("send_ext_community"),
                ebgp_multihop=neighbor.get("ebgp_multihop"),
                password=neighbor.get("password"),
                send_label=neighbor.get("send_label"),
                send_label_explicit=neighbor.get("send_label_explicit"),
                as_override=neighbor.get("as_override"),
                as_number=neighbor.get("as_number"),
                address_family=self.parse_address_family_item(neighbor.get("address_family", [])),
            )
            items.append(ni)
        return items

    def parse_address_family_item(self, address_family: List[Dict]) -> Optional[List[AddressFamilyItem]]:
        if not address_family:
            return None

        items = []
        for family in address_family:
            family_type = family.pop("type", None)
            if not family_type:
                continue

            family_type = as_global(family_type, RedistributeProtocol)
            items.append(
                AddressFamilyItem(
                    family_type=family_type,
                    **family,
                )
            )
        return items

    def parse_neighbor_ipv6(self, neighbors: List[Dict]) -> Optional[List[Ipv6NeighborItem]]:
        if not neighbors:
            return None

        items = []
        for neighbor in neighbors:
            address = neighbor.get("address")
            remote_as = neighbor.get("remote_as")
            if not address or not remote_as:
                # Skip to not lose whole conversion
                continue

            ni = Ipv6NeighborItem(
                address=address,
                description=neighbor.get("description"),
                shutdown=neighbor.get("shutdown"),
                remote_as=remote_as,
                local_as=neighbor.get("local_as"),
                keepalive=neighbor.get("timers", {}).get("keepalive"),
                holdtime=neighbor.get("holdtime"),
                if_name=neighbor.get("if_name"),
                next_hop_self=neighbor.get("next_hop_self"),
                send_community=neighbor.get("send_community"),
                send_ext_community=neighbor.get("send_ext_community"),
                ebgp_multihop=neighbor.get("ebgp_multihop"),
                password=neighbor.get("password"),
                as_override=neighbor.get("as_override"),
                as_number=neighbor.get("as_number"),
                address_family=self.parse_address_family_item(neighbor.get("address_family", [])),
            )
            items.append(ni)
        return items

    def parse_address_family(self, address_family: List[Dict]) -> Optional[AddressFamily]:
        if len(address_family) != 1:
            return None

        family = address_family[0]

        return AddressFamily(
            aggregate_address=self.parse_aggregate_address(family.get("aggregate_address", [])),
            network=self.parse_network_item(family.get("network", [])),
            paths=family.get("paths") if family.get("paths") else family.get("maximum_paths", {}).get("paths"),
            originate=family.get("originate"),
            name=family.get("name"),
            filter=family.get("filter"),
            redistribute=self.parse_redistribute(family.get("redistribute", [])),
        )

    def parse_redistribute(self, data: List[Dict]) -> Optional[List[RedistributeItem]]:
        if not data:
            return None

        items = []
        for item in data:
            protocol = item.get("protocol")
            if not protocol:
                continue
            if isinstance(protocol, Global):
                protocol = as_global(protocol.value, RedistributeProtocol)

            ri = RedistributeItem(
                protocol=protocol,
                route_policy=self.parse_route_policy(item.get("route_policy")),
            )
            items.append(ri)
        return items

    def parse_route_policy(self, route_policy: Optional[Dict]) -> Optional[RefIdItem]:
        if isinstance(route_policy, Global):
            try:
                UUID(route_policy.value)
                return RefIdItem(
                    ref_id=route_policy,
                )
            except ValueError:
                pass

        return None

    def parse_aggregate_address(self, data: List[Dict]) -> Optional[List[AggregateAddres]]:
        if not data:
            return None

        items = []
        for item in data:
            prefix = self.parse_prefix(item.get("prefix"))
            if not prefix:
                continue

            aa = AggregateAddres(
                prefix=prefix,
                as_set=item.get("as_set"),
                summary_only=item.get("summary_only"),
            )
            items.append(aa)
        return items

    def parse_network_item(self, data: List[Dict]) -> Optional[List[NetworkItem]]:
        if not data:
            return None

        items = []
        for item in data:
            prefix = self.parse_prefix(item.get("prefix"))
            if not prefix:
                continue
            ni = NetworkItem(
                prefix=prefix,
            )
            items.append(ni)
        return items

    def parse_prefix(self, address: Optional[Union[Variable, Global[IPv4Interface]]]) -> Optional[AddressWithMask]:
        if not address:
            return None

        if isinstance(address, Variable):
            return AddressWithMask(address=address, mask=address)

        return AddressWithMask(
            address=as_global(address.value.network.network_address),
            mask=as_global(str(address.value.netmask)),
        )
