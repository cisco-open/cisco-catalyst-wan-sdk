# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import TLOCColor

DEFAULT_BFD_COLOR_MULTIPLIER = 7
DEFAULT_BFD_DSCP = 48
DEFAULT_BFD_HELLO_INTERVAL = 1000
DEFAULT_BFD_POLL_INTERVAL = 600000
DEFAULT_BFD_MULTIPLIER = 6


class Color(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    color: TLOCColor = Field(description="The color of the BFD session, representing various transport types")
    hello_interval: Optional[int] = Field(
        default=DEFAULT_BFD_HELLO_INTERVAL,
        json_schema_extra={"vmanage_key": "hello-interval"},
        description="The BFD hello interval in milliseconds",
    )
    multiplier: Optional[int] = Field(
        default=DEFAULT_BFD_COLOR_MULTIPLIER, description="The BFD multiplier for the color"
    )
    pmtu_discovery: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "pmtu-discovery"},
        description="Whether to enable Path MTU Discovery",
    )
    dscp: Optional[int] = Field(default=DEFAULT_BFD_DSCP, description="The DSCP value used for BFD packets")


class CiscoBFDModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco Bidirectional Forwarding Detection (BFD) configuration"

    multiplier: Optional[int] = Field(
        default=DEFAULT_BFD_MULTIPLIER,
        json_schema_extra={"data_path": ["app-route"]},
        description="The default BFD multiplier for all colors",
    )
    poll_interval: Optional[int] = Field(
        default=DEFAULT_BFD_POLL_INTERVAL,
        json_schema_extra={"vmanage_key": "poll-interval", "data_path": ["app-route"]},
        description="The BFD poll interval in milliseconds",
    )
    default_dscp: Optional[int] = Field(
        default=DEFAULT_BFD_DSCP,
        json_schema_extra={"vmanage_key": "default-dscp"},
        description="The default DSCP value for BFD packets",
    )
    color: Optional[List[Color]] = Field(default=None, description="List of color-specific BFD configurations")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bfd"
