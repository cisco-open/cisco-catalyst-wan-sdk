# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_bfd_model import CiscoBFDModel, Color

cisco_bfd = CiscoBFDModel(  # type: ignore
    template_name="cisco_bfd",
    template_description="na",
    multiplier=100,
    poll_interval=50,
    default_dscp=50,
    color=[
        Color(color="biz-internet", hello_interval=50, multipler=100, pmtu_discovery=False, dscp=100),  # type: ignore
        Color(color="silver", hello_interval=150, multipler=10, dscp=20),  # type: ignore
    ],
)
