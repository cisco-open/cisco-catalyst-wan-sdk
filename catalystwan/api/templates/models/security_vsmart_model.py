# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate

Protocol = Literal["dtls", "tls"]


class SecurityvSmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Security settings for vSmart controller"

    protocol: Optional[Protocol] = Field(
        default=None,
        json_schema_extra={"data_path": ["control"]},
        description="The security protocol used for control plane communication",
    )
    tls_port: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tls-port", "data_path": ["control"]},
        description="The port used for TLS communications",
    )
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "security-vsmart"
