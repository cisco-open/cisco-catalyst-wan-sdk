# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_ntp_model import Authentication, CiscoNTPModel, Server

cisco_ntp_complex = CiscoNTPModel(
    template_name="cisco_ntp_complex",
    template_description="cisco_ntp_complex",
    server=[
        Server(name="0.pool.ntp.org", key=1, vpn=10, version=4, source_interface="GigabitEthernet0/0", prefer=True),
        Server(name="1.pool.ntp.org", key=2, vpn=20, version=4, source_interface="GigabitEthernet0/1", prefer=False),
    ],
    authentication=[Authentication(number=1, md5="md5key1"), Authentication(number=2, md5="md5key2")],
    trusted=[1, 2],
    enable=True,
    stratum=2,
    source="Loopback0",
)
