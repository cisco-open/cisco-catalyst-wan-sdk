# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional
from uuid import UUID

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


def str_to_uuid(s: str) -> Optional[UUID]:
    try:
        return UUID(s)
    except ValueError:
        return None


class GeneralTemplate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = ""
    subTemplates: List[GeneralTemplate] = []

    templateId: str = ""
    templateType: str = ""


class DeviceTemplate(BaseModel):
    """
    ## Example:

    >>> templates = [
            "default_system", # Cisco System
            "default_logging", # Cisco Logging
            "default_banner", # Banner
        ]
    >>> device_template = DeviceTemplate(
            template_name="python",
            template_description="python",
            general_templates=templates
        )
    >>> session.api.templates.create(device_template)
    """

    template_name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    template_description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")
    general_templates: List[GeneralTemplate] = Field(
        default=[], serialization_alias="generalTemplates", validation_alias="generalTemplates"
    )
    device_role: str = Field(default="sdwan-edge", serialization_alias="deviceRole", validation_alias="deviceRole")
    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    security_policy_id: str = Field(
        default="", serialization_alias="securityPolicyId", validation_alias="securityPolicyId"
    )
    policy_id: str = Field(default="", serialization_alias="policyId", validation_alias="policyId")

    def get_security_policy_uuid(self) -> Optional[UUID]:
        return str_to_uuid(self.security_policy_id)

    def get_policy_uuid(self) -> Optional[UUID]:
        return str_to_uuid(self.policy_id)

    def generate_payload(self) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        template = env.get_template(self.payload_path.name)
        output = template.render(self.model_dump())

        ast = env.parse(output)
        if meta.find_undeclared_variables(ast):
            logger.info(meta.find_undeclared_variables(ast))
            raise Exception("There are undeclared variables.")
        return output

    @field_validator("general_templates", mode="before")
    @classmethod
    def parse_templates(cls, value):
        output = []
        for template in value:
            if isinstance(template, str):
                output.append(GeneralTemplate(name=template))
            else:
                output.append(template)
        return output

    payload_path: ClassVar[Path] = Path(__file__).parent / "device_template_payload.json.j2"

    @classmethod
    def get(self, name: str, session: ManagerSession) -> DeviceTemplate:
        device_template = session.api.templates.get(DeviceTemplate).filter(name=name).single_or_default()
        resp = session.get(f"dataservice/template/device/object/{device_template.id}").json()
        return DeviceTemplate(**resp)

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class DeviceSpecificValue(BaseModel):
    property: str
