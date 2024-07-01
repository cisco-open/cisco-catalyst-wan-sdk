# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.security_vsmart_model import SecurityvSmart

security_vsmart_complex = SecurityvSmart(
    template_name="security_vsmart_complex",
    template_description="Apply Security settings for vSmart controller",
    device_models=["vsmart"],
    protocol="dtls",
    tls_port=120,
)
