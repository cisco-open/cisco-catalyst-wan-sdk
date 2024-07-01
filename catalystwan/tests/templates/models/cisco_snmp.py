# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_snmp_model import CiscoSNMPModel, Community, Group, Oid, Target, User, View

cisco_snmp_complex = CiscoSNMPModel(
    template_name="cisco_snmp_complex",
    template_description="Comprehensive Cisco SNMP Configuration",
    shutdown=False,
    contact="SNMP Admin",
    location="Data Center A",
    view=[
        View(name="SystemView", oid=[Oid(id="1.3.6.1.2.1.1", exclude=False), Oid(id="1.3.6.1.2.1.2", exclude=True)]),
        View(name="AllView", oid=[Oid(id="1.3.6.1", exclude=False)]),
    ],
    community=[
        Community(name="public", view="SystemView", authorization="read-only"),
        Community(name="private", view="AllView", authorization="read-only"),
    ],
    group=[Group(name="v3group", security_level="auth-priv", view="AllView")],
    user=[
        User(
            name="snmpuser",
            auth="md5",
            auth_password="authpass",  # pragma: allowlist secret
            priv="aes-cfb-128",
            priv_password="privpass",  # pragma: allowlist secret
            group="v3group",
        )
    ],
    target=[
        Target(
            vpn_id=10,
            ip="192.0.2.50",
            port=162,
            community_name="public",
            user="snmpuser",
            source_interface="GigabitEthernet0/0",
        )
    ],
)
