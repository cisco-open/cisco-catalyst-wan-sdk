from catalystwan.api.templates.models.aaa_model import (
    AAAModel,
    RadiusServer,
    TacacsServer,
    TaskPermissions,
    User,
    UserGroup,
)

aaa_basic = AAAModel(
    template_name="aaa_basic",
    template_description="zyx",
    device_models=["vsmart"],
)

aaa_complex_template = AAAModel(
    template_name="aaa_complex",
    template_description="zyx",
    device_models=["vsmart"],
    accounting=True,
    admin_auth_order=True,
    audit_disable=True,
    auth_fallback=True,
    auth_order=["local", "radius"],
    cisco_tac_ro_user=False,
    cisco_tac_rw_user=False,
    netconf_disable=True,
    radius_retransmit=4,
    radius_server=[
        RadiusServer(
            address="1.1.1.1",
            acct_port=1000,
            auth_port=2000,
            tag="complex1",
            vpn="0",
            source_interface="eth1",
            priority=1,
            key="example-key",  # pragma: allowlist secret
            secret_key="example-secret",  # pragma: allowlist secret
        ),
    ],
    radius_server_list=["nonexisiting", "second"],
    radius_timeout=6,
    tacacs_authentication="ascii",
    tacacs_server=[
        TacacsServer(
            address="2.2.2.2",
            auth_port=20,
            vpn="0",
            source_interface="eth12",
            priority=5,
            secret_key="secret-example",  # pragma: allowlist secret
        ),
    ],
    tacacs_timeout=10,
    # task=[
    #     Task(
    #       name="exampletask1",
    #       config_accept_action=[Command("cac"), Command("com2")],
    #       config_default_action="accept",
    #       config_deny_action=[Command("cda")],
    #       oper_exec_accept_action=[Command("oxaa")],
    #       oper_exec_default_action="accept",
    #       oper_exec_deny_action=[Command("oeda")],
    #       password="examplepass",  # pragma: allowlist secret
    #       privilege="1"
    #     ),
    #     Task(
    #       name="exampletask2",
    #       password="examplepass",  # pragma: allowlist secret
    #       privilege="1",
    #       config_default_action="accept",
    #       oper_exec_default_action="accept"
    #       ),
    # ],
    user=[
        User(
            name="example-user",
            password="example-pass",  # pragma: allowlist secret
            secret="user-secret",  # pragma: allowlist secret
            description="user-desc",
            group=["netadmin"],
        ),
    ],
    usergroup=[
        UserGroup(name="netadmin"),  #
        UserGroup(
            name="basic",
            task=[
                TaskPermissions(mode="system", permission=["read"]),
                TaskPermissions(mode="interface", permission=["read"]),
            ],
        ),
        UserGroup(
            name="operator",
            task=[
                TaskPermissions(mode="system", permission=["read"]),
                TaskPermissions(mode="interface", permission=["read"]),
                TaskPermissions(mode="policy", permission=["read"]),
                TaskPermissions(mode="routing", permission=["read"]),
                TaskPermissions(mode="security", permission=["read"]),
            ],
        ),
    ],
)
