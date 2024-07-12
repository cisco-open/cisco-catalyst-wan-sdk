# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_banner_model import CiscoBannerModel

cisco_banner = CiscoBannerModel(  # type: ignore
    template_name="cisco_banner", template_description="na", login_banner="login banner", motd_banner="motd_bnanner"
)
