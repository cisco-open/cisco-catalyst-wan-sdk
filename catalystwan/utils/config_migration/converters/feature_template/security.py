# Copyright 2024 Cisco Systems, Inc. and its affiliates
from copy import deepcopy
from typing import List, Optional, Type, TypeVar, Union

from catalystwan.api.configuration_groups.parcel import Global, Variable
from catalystwan.models.configuration.feature_profile.sdwan.system import SecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.security import (
    AcceptLifetime,
    IntegrityType,
    KeychainItem,
    KeyItem,
    OneOfendChoice1,
    OneOfendChoice2,
    OneOfendChoice3,
    ReplayWindow,
    SendLifetime,
    Tcp,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import (
    create_dict_without_none,
    return_global_variable_or_none,
)

from .base import FTConverter

Lifetime = TypeVar("Lifetime", SendLifetime, AcceptLifetime)


class SecurityConverter(FTConverter):
    """
    A class for converting template values into a SecurityParcel object.

    Attributes:
        supported_template_types (tuple): A tuple of supported template types.
    """

    supported_template_types = (
        "cisco_security",
        "security",
        "security-vsmart",
        "security-vedge",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> SecurityParcel:
        """
        Creates a SecurityParcel object based on the provided template values.

        Args:
            name (str): The name of the SecurityParcel.
            description (str): The description of the SecurityParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            SecurityParcel: A SecurityParcel object with the provided template values.
        """
        data = deepcopy(template_values)
        data_ipsec = data.get("ipsec", {})
        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            # data ipsec
            rekey=data_ipsec.get("rekey"),
            replay_window=return_global_variable_or_none(data_ipsec, "replay_window", Global[ReplayWindow]),
            extended_ar_window=data_ipsec.get("extended_ar_window"),
            integrity_type=self.parse_integrity(data_ipsec),
            # data
            pairwise_keying=data.get("pairwise-keying"),
            keychain=self.parse_keychain(data),
            key=self.parse_key(data),
        )

        return SecurityParcel(**payload)

    def parse_integrity(self, data_ipsec: dict) -> Union[Global[List[IntegrityType]], Variable]:
        integrity_type = return_global_variable_or_none(data_ipsec, "integrity_type", Global[List[IntegrityType]])
        if integrity_type is None:
            self._convert_result.update_status(
                "partial",
                "Required 'Integrity type' data is missing. Setting default value to 'esp', 'ip-udp-esp' as in UI.",
            )
            integrity_type = Global[List[IntegrityType]](value=["esp", "ip-udp-esp"])
        return integrity_type

    def parse_keychain(self, data: dict) -> List[KeychainItem]:
        keychains = data.get("trustsec", {}).get("keychain", [])
        items = []
        for kc in keychains:
            name = kc.get("name")
            keyid = kc.get("keyid")
            if not name or not keyid:
                self._convert_result.update_status(
                    "partial", "Required 'Keychain' data is missing. Skipping this keychain."
                )
                continue
            items.append(
                KeychainItem(
                    name=name,
                    id=keyid,
                )
            )
        return items

    def parse_key(self, data: dict) -> List[KeyItem]:
        keyitems = data.get("key", [])
        items = []
        self._convert_result.update_status(
            "partial", "Key Strings are encrypted. Please update the key strings manually."
        )
        for ki in keyitems:
            tcp = return_global_variable_or_none(ki.get("cryptographic_algorithm_choice"), "tcp", Global[Tcp])
            if not tcp or not isinstance(tcp, Global):
                self._convert_result.update_status(
                    "partial", "Required 'TCP' data is missing. Setting default value to 'hmac-sha-1' as in UI."
                )
                tcp = Global[Tcp](value="hmac-sha-1")

            items.append(
                KeyItem(
                    id=ki.get("id"),
                    name=ki.get("chain_name"),
                    send_id=ki.get("send_id"),
                    recv_id=ki.get("recv_id"),
                    include_tcp_options=ki.get("include_tcp_options"),
                    accept_ao_mismatch=ki.get("accept_ao_mismatch"),
                    tcp=tcp,
                    key_string=ki.get("key_string"),
                    send_lifetime=self.parse_send_lifetime(ki),
                    accept_lifetime=self.parse_accept_lifetime(ki),
                )
            )
        return items

    def parse_send_lifetime(self, data: dict) -> Optional[SendLifetime]:
        sendlifetime = data.get("send_lifetime", {}).get("lifetime_group_v1")
        return self._parse_lifetime(sendlifetime, SendLifetime)

    def parse_accept_lifetime(self, data: dict) -> Optional[AcceptLifetime]:
        acceptlifetime = data.get("accept_lifetime", {}).get("lifetime_group_v1")
        return self._parse_lifetime(acceptlifetime, AcceptLifetime)

    def _parse_lifetime(self, data: Optional[dict], lifetime: Type[Lifetime]) -> Optional[Lifetime]:
        if not data:
            return None
        start_epoch = data.get("start_epoch")
        if not start_epoch or not isinstance(start_epoch, Global):
            self._convert_result.update_status(
                "partial", "Required 'Start Epoch' data is missing. Setting default value to '0' as in UI."
            )
            return None
        return lifetime(
            local=data.get("local"),
            start_epoch=start_epoch,
            one_ofend_choice=self.parse_one_ofend_choice(data),
        )

    def parse_one_ofend_choice(self, data: dict) -> Optional[Union[OneOfendChoice1, OneOfendChoice2, OneOfendChoice3]]:
        end_choice = data.get("end_choice")
        if not end_choice:
            return None
        if end_choice.value == "end-epoch":
            extact = data.get("end_epoch")
            if not extact or not isinstance(extact, Global):
                self._convert_result.update_status(
                    "partial", "Required 'End Epoch' data is missing. Setting value to None."
                )
                return None
            return OneOfendChoice3(exact=extact)
        elif end_choice.value == "duration":
            duration = data.get("duration")
            if not duration or not isinstance(duration, Global):
                self._convert_result.update_status(
                    "partial", "Required 'Duration' data is missing. Setting value to None."
                )
                return None
            return OneOfendChoice2(duration=duration)
        return OneOfendChoice1()
