from copy import deepcopy
from ipaddress import IPv4Address
from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Global, OptionType, as_default, as_global
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    AutoRpAttributes,
    BsrCandidateAttributes,
    IgmpAttributes,
    IgmpInterfaceParameters,
    LocalConfig,
    MulticastBasicAttributes,
    MulticastParcel,
    PimAttributes,
    PimBsrAttributes,
    PimInterfaceParameters,
    RPAnnounce,
    RpDiscoveryScope,
    SptThreshold,
    SsmAttributes,
    SsmFlag,
    StaticJoin,
    StaticRpAddress,
)

from .base import FTConverter


class MulticastToMulticastConverter(FTConverter):
    """This is corner case.
    Multicast Parcel is not a direct conversion from template.
    It is a combination of multiple templates.
    Feature Templates: Multicast, IGMP, PIM.
    """

    supported_template_types = ("cedge_multicast", "cisco_multicast", "multicast")

    delete_keys = ("multicast", "multicast_replicator")

    def create_parcel(self, name: str, description: str, template_values: dict) -> MulticastParcel:
        values = self.prepare_values(template_values)
        self.configure_basic_attributes(values)
        self.cleanup_keys(values)
        return MulticastParcel(parcel_name=name, parcel_description=description, **values)

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)

    def configure_basic_attributes(self, values: dict) -> None:
        values["basic"] = MulticastBasicAttributes(
            spt_only=values.get("multicast", {}).get("spt_only", as_default(False)),
            local_config=LocalConfig(
                local=values.get("multicast_replicator", {}).get("local", as_default(False)),
                threshold=values.get("multicast_replicator", {}).get("threshold", as_default(False)),
            ),
        )

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)

    def get_example_payload(self):
        return {
            "multicast_replicator": {
                "local": Global[bool](value=False),
                "threshold": Global[int](value=11),
            },
            "multicast": {"spt_only": Global[bool](value=True)},
        }


class PimToMulticastConverter(FTConverter):
    """This is corner case.
    Multicast Parcel is not a direct conversion from template.
    It is a combination of multiple templates.
    Feature Templates: Multicast, IGMP, PIM.
    """

    supported_template_types = ("cedge_pim", "cisco_pim", "pim")

    def create_parcel(self, name: str, description: str, template_values: dict) -> MulticastParcel:
        values = self.prepare_values(template_values)
        return MulticastParcel(
            parcel_name=name,
            parcel_description=description,
            pim=self.configure_pim(values),
        )

    def configure_pim(self, values: dict) -> PimAttributes:
        return PimAttributes(
            ssm=self._set_ssm_attributes(values),
            interface=self._set_interface(values),
            rp_address=self._set_rp_address(values),
            auto_rp=self._set_auto_rp(values),
            pim_bsr=self._set_pim_bsr(values),
        )

    def _set_ssm_attributes(self, values: dict) -> SsmAttributes:
        spt_threshold = values.get("spt_threshold", as_default("0", SptThreshold))
        if spt_threshold.option_type == OptionType.GLOBAL:
            spt_threshold = as_global(spt_threshold.value, SptThreshold)

        return SsmAttributes(
            ssm_range_config=SsmFlag(range=values.get("ssm", {}).get("range", as_default("eqw"))),
            spt_threshold=spt_threshold,
        )

    def _set_interface(self, values: dict) -> Optional[List[PimInterfaceParameters]]:
        interfaces = values.get("interface", [])
        interface_list = []
        for interface in interfaces:
            interface_list.append(
                PimInterfaceParameters(
                    interface_name=interface.get("name"),
                    query_interval=interface.get("query_interval", as_default(30)),
                    join_prune_interval=interface.get("join_prune_interval", as_default(60)),
                )
            )
        return interface_list

    def _set_rp_address(self, values: dict) -> Optional[List[StaticRpAddress]]:
        rp_addresses = values.get("rp_addr", [])
        rp_address_list = []
        for rp_address in rp_addresses:
            rp_address_list.append(
                StaticRpAddress(
                    address=rp_address.get("address"),
                    access_list=rp_address.get("access_list"),
                    override=rp_address.get("override", as_default(False)),
                )
            )
        return rp_address_list

    def _set_auto_rp(self, values: dict) -> AutoRpAttributes:
        return AutoRpAttributes(
            enable_auto_rp_flag=values.get("auto_rp", as_default(False)),
            send_rp_discovery=self._set_rp_discovery(values),
        )

    def _set_rp_discovery(self, values: dict) -> Optional[List[RPAnnounce]]:
        interface_name = values.get("send_rp_discovery", {}).get("if_name")
        scope = values.get("send_rp_discovery", {}).get("scope")
        if interface_name is None or scope is None:
            return None
        return [
            RPAnnounce(
                interface_name=interface_name,
                scope=scope,
            )
        ]

    def _set_pim_bsr(self, values: dict) -> Optional[PimBsrAttributes]:
        return PimBsrAttributes(
            rp_candidate=self._set_rp_candidate(values),
            bsr_candidate=self._set_bsr_candidate(values),
        )

    def _set_rp_candidate(self, values: dict) -> Optional[List[RpDiscoveryScope]]:
        rp_candidate = values.get("rp_candidate", [])
        if not rp_candidate:
            return None
        rp_candidate_list = []
        for candidate in rp_candidate:
            rp_candidate_list.append(
                RpDiscoveryScope(
                    interface_name=candidate.get("pim_interface_name"),
                    group_list=candidate.get("group_list"),
                    interval=candidate.get("interval"),
                    priority=candidate.get("priority"),
                )
            )
        return rp_candidate_list

    def _set_bsr_candidate(self, values: dict) -> Optional[List[BsrCandidateAttributes]]:
        bsr_candidate = values.get("bsr_candidate", {})
        if not bsr_candidate:
            return None
        mask = bsr_candidate.get("mask")
        if mask.option_type == OptionType.GLOBAL:
            mask = as_global(int(mask.value))
        candidate = BsrCandidateAttributes(
            interface_name=bsr_candidate.get("bsr_interface_name"),
            mask=mask,
            priority=bsr_candidate.get("priority"),
            accept_rp_candidate=bsr_candidate.get("accept_rp_candidate"),
        )
        return [candidate]

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values).get("pim", {})

    def get_example_payload(self):
        return {
            "pim": {
                "send_rp_discovery": {
                    "if_name": Global[str](value="qeq"),
                    "scope": Global[int](value=2),
                },
                "auto_rp": Global[bool](value=True),
                "spt_threshold": Global[str](value="infinity"),
                "ssm": {"range": Global[str](value="eqw")},
                "bsr_candidate": {
                    "bsr_interface_name": Global[str](value="33311"),
                    "mask": Global[str](value="2"),
                    "priority": Global[int](value=3),
                    "accept_rp_candidate": Global[str](value="12"),
                },
                "interface": [
                    {
                        "name": Global[str](value="232"),
                        "query_interval": Global[int](value=23),
                        "join_prune_interval": Global[int](value=12),
                    },
                    {
                        "name": Global[str](value="33311"),
                        "query_interval": Global[int](value=33),
                        "join_prune_interval": Global[int](value=111),
                    },
                ],
                "rp_addr": [
                    {
                        "address": Global[IPv4Address](value=IPv4Address("1.1.1.1")),
                        "access_list": Global[str](value="323"),
                        "override": Global[bool](value=True),
                    },
                    {
                        "address": Global[IPv4Address](value=IPv4Address("2.2.2.2")),
                        "access_list": Global[str](value="333"),
                        "override": Global[bool](value=False),
                    },
                ],
                "rp_candidate": [
                    {
                        "pim_interface_name": Global[str](value="232"),
                        "group_list": Global[str](value="234"),
                        "interval": Global[int](value=23),
                        "priority": Global[int](value=44),
                    },
                    {
                        "pim_interface_name": Global[str](value="33311"),
                        "group_list": Global[str](value="23"),
                        "interval": Global[int](value=1112),
                        "priority": Global[int](value=33),
                    },
                ],
            }
        }


class IgmpToMulticastConverter(FTConverter):
    """This is corner case.
    Multicast Parcel is not a direct conversion from template.
    It is a combination of multiple templates.
    Feature Templates: Multicast, IGMP, PIM.
    """

    supported_template_types = ("cedge_igmp", "cisco_IGMP", "igmp")

    def create_parcel(self, name: str, description: str, template_values: dict) -> MulticastParcel:
        values = self.prepare_values(template_values)
        return MulticastParcel(
            parcel_name=name,
            parcel_description=description,
            igmp=self.configure_igmp(values),
        )

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)["igmp"]

    def configure_igmp(self, values: dict) -> Optional[IgmpAttributes]:
        interface = (self._set_interface(values),)
        if not interface:
            return None
        return IgmpAttributes(
            interface=self._set_interface(values),
        )

    def _set_interface(self, values: dict) -> List[IgmpInterfaceParameters]:
        interfaces = values.get("interface", [])
        interface_list = []
        for interface in interfaces:
            interface_list.append(
                IgmpInterfaceParameters(
                    interface_name=interface.get("name"),
                    join_group=self._set_join_group(interface),
                )
            )
        return interface_list

    def _set_join_group(self, interface: dict) -> Optional[List[StaticJoin]]:
        join_group = interface.get("join_group", [])
        if not join_group:
            return None
        join_group_list = []
        for group in join_group:
            join_group_list.append(
                StaticJoin(
                    group_address=group.get("group_address"),
                    source_address=group.get("source"),
                )
            )
        return join_group_list

    def get_example_payload(self):
        return {
            "igmp": {
                "interface": [
                    {
                        "name": Global[str](value="321213"),
                        "join_group": [
                            {
                                "group_address": Global[IPv4Address](value=IPv4Address("33.2.2.1")),
                                "source": Global[IPv4Address](value=IPv4Address("3.3.3.3")),
                            },
                            {
                                "group_address": Global[IPv4Address](value=IPv4Address("2.1.2.3")),
                                "source": Global[IPv4Address](value=IPv4Address("1.1.1.1")),
                            },
                            {
                                "group_address": Global[IPv4Address](value=IPv4Address("4.65.2.4")),
                                "source": Global[IPv4Address](value=IPv4Address("23.3.3.1")),
                            },
                        ],
                    },
                    {
                        "name": Global[str](value="33"),
                        "join_group": [
                            {
                                "group_address": Global[IPv4Address](value=IPv4Address("4.2.3.2")),
                                "source": Global[IPv4Address](value=IPv4Address("33.2.1.2")),
                            }
                        ],
                    },
                ]
            }
        }
