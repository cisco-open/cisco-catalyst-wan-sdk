# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate


class OMPvSmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Overlay Management Protocol (OMP) settings for vSmart controller"

    graceful_restart: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "graceful-restart"},
        description="Enable or disable graceful restart for the OMP session",
    )
    send_path_limit: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "send-path-limit"},
        description="The maximum number of paths that can be sent to a TLOC",
    )
    send_backup_paths: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "send-backup-paths"},
        description="Enable or disable sending additional backup paths",
    )
    discard_rejected: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "discard-rejected"},
        description="Discard routes that are rejected by policy instead of marking them as rejected",
    )
    shutdown: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "shutdown"},
        description="Enable or disable the shutdown of the OMP session",
    )
    graceful_restart_timer: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "graceful-restart-timer", "data_path": ["timers"]},
        description="The time interval for graceful restart of OMP sessions",
    )
    eor_timer: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "eor-timer", "data_path": ["timers"]},
        description="The End of Routes (EOR) timer value",
    )
    holdtime: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "holdtime", "data_path": ["timers"]},
        description="The hold time interval for OMP sessions",
    )
    affinity_group_preference: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "affinity-group-preference", "data_path": ["filter-route", "outbound"]},
        description="Filter routes based on affinity preference list",
    )
    advertisement_interval: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "advertisement-interval", "data_path": ["timers"]},
        description="Interval between sending OMP route advertisements",
    )
    tloc_color: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "tloc-color", "data_path": ["filter-route", "outbound"]},
        description="Filter routes based on TLOC color",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "omp-vsmart"
