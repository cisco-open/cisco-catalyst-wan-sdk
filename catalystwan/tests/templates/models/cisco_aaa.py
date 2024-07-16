# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
from catalystwan.api.templates.models.cisco_aaa_model import (
    AccountingRule,
    AuthorizationRules,
    CiscoAAAModel,
    PubkeyChain,
    RadiusClient,
    RadiusGroup,
    RadiusServer,
    RadiusVPN,
    TacacsGroup,
    TacacsServer,
    User,
)

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),  # pragma: allowlist secret
    User(name="user", password="rnd", secret="dnr", privilege="1"),  # pragma: allowlist secret
]


# CiscoAAAModel(domain-stripping="?")
cisco_aaa = CiscoAAAModel(
    template_name="cisco_aaa",
    template_description="zyx",
    device_models=["vedge-C8000V"],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(  # type: ignore
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping="no",
)

EXAMPLE_KEY_STRING = "AAAAB3NzaC1yc2EAAAADAQABAAABAQC3myRj5L6ZFLdRnOEZdUd+4Qq0XPLW9RfO6qD7DJ2t4ZzLh6Oz+IUJg8d8bJDfxO9zGKs5uUQ9f2H5yTGX5G8Z5kKp8QDp1MkDVqwGJ4UM7JqH8s8kD7xcl8SyPc5TjzK4s4W+8LPNOPXmIKtHh1Qlvkp5N7w3M/Rm5ZVX5/3+Hk8Ib5syigQQd/5u5xJj9k3i2x3m3LZ7v5e7YlCpRdCQGf6ZCwvbVQHdJp5nlU0HxJbqjOTL4IcDj09G3Dq2C5JnohKJb7E7HVCUl7F5vYpC/4iNjges65GgdzaFJsT9qA8CgxyF+7J3PpLk5qPAQDT5OjArJj4x9Bw3j3lZdH example@example.com"  # noqa: E501

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),  # pragma: allowlist secret
    User(
        name="user",
        password="rnd",  # pragma: allowlist secret
        secret="dnr",  # pragma: allowlist secret
        privilege="1",
        pubkey_chain=[PubkeyChain(key_type="ssh-rsa", key_string=EXAMPLE_KEY_STRING)],
    ),
]

cisco_aaa_complex = CiscoAAAModel(
    template_name="cisco_aaa_complex",
    template_description="cisco_aaa_complex",
    device_models=["vedge-C8000V"],
    user=[
        User(
            name="example_user",
            password="secure_password",  # pragma: allowlist secret
            secret="secure_secret",  # pragma: allowlist secret
            privilege="15",
        ),
    ],
    tacacs=[
        TacacsGroup(
            server=[
                TacacsServer(
                    address="2.2.2.2",
                    key="tacacs_key",
                    port=49,
                    timeout=5,
                    secret_key="secret_tacacs_key,",
                )
            ],
            group_name="tacacs-5",
            vpn=5,
            source_interface="GigabitEthernet0/0",
        )
    ],
    radius=[
        RadiusGroup(
            server=[
                RadiusServer(
                    address="1.1.1.1",
                    auth_port=1000,
                    timeout=10,
                    retransmit=5,
                    key="radius_key",  # pragma: allowlist secret
                    secret_key="secret_radius_key",  # pragma: allowlist secret
                )
            ],
            group_name="radius-4",
            vpn=4,
            source_interface="FortyGigabitEthernet0/",
        )
    ],
    radius_client=[
        RadiusClient(ip="10.1.1.1", vpn=[RadiusVPN(name="radiuscoa_vpn_name", server_key="secure_radius_server_key")])
    ],
    domain_stripping="right-to-left",
    authentication_type="any",
    port=1163,
    server_key_password="secure_server_key_password",  # pragma: allowlist secret
    cts_authorization_list="example_element",
    radius_trustsec_group="radius-4",
    authentication_group=True,
    accounting_group=True,
    accounting_rules=[
        AccountingRule(
            rule_id="1111",
            method="commands",
            level="1",
            start_stop=False,
            group="radius-4,tacacs-5",
        )
    ],
    authorization_console=True,
    authorization_config_commands=True,
    authorization_rules=[
        AuthorizationRules(rule_id="12", method="commands", level="15", group="radius-4,tacacs-5", authenticated=True)
    ],
    server_auth_order="local,radius-4,tacacs-5",
)
