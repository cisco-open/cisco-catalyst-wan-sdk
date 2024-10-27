# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.models.policy.policy import AssemblyItemBase, PolicyCreationPayload, PolicyDefinition, PolicyInfo
from catalystwan.models.policy.policy_definition import VoicePortType

VoiceAssemblyItemType = Literal[
    "dialPeer",
    "fxoPort",
    "fxsDidPort",
    "fxsPort",
    "priIsdnPort",
    "srstPhoneProfile",
]


class VoiceAssemblyItem(AssemblyItemBase):
    model_config = ConfigDict(populate_by_name=True)
    type: VoiceAssemblyItemType
    port_type: VoicePortType = Field(serialization_alias="portType", validation_alias="portType")


class VoicePolicyDefinition(PolicyDefinition):
    model_config = ConfigDict(populate_by_name=True)
    assembly: List[VoiceAssemblyItem] = Field(default_factory=list)

    def find_assembly_item_by_definition_id(self, definition_id: UUID) -> Optional[VoiceAssemblyItem]:
        for item in self.assembly:
            if item.definition_id == definition_id:
                return item
        return None


class VoicePolicy(PolicyCreationPayload):
    model_config = ConfigDict(populate_by_name=True)
    policy_type: Literal["feature"] = Field(
        default="feature", serialization_alias="policyType", validation_alias="policyType"
    )
    policy_definition: VoicePolicyDefinition = Field(
        serialization_alias="policyDefinition",
        validation_alias="policyDefinition",
    )

    @model_validator(mode="before")
    @classmethod
    def try_parse_policy_definition_string(cls, values):
        # this is needed because GET /template/policy/vsmart contains string in policyDefinition field
        # while POST /template/policy/vsmart requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if not isinstance(values, dict):
            return values
        json_policy_type = values.get("policyType")
        json_policy_definition = values.get("policyDefinition")
        if json_policy_type == "feature" and isinstance(json_policy_definition, str):
            values["policyDefinition"] = VoicePolicyDefinition.model_validate_json(json_policy_definition)
        return values


class VoicePolicyEditResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    master_templates_affected: List[str] = Field(
        default_factory=list, serialization_alias="masterTemplatesAffected", validation_alias="masterTemplatesAffected"
    )


class VoicePolicyInfo(PolicyInfo, VoicePolicy):
    pass
