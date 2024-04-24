# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate


class CliTemplateModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "CLI Template Feature configuration for applying command-line settings."

    config: str = Field(description="The CLI configuration commands to be applied as a template.")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cli-template"
