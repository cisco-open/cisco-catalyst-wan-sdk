from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Profile(BaseModel):
    id: UUID


Solution = Literal[
    "sd-routing",
    "sdwan",
]


class FromPolicyGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    copy_: UUID = Field(validation_alias="copy", serialization_alias="copy")


class PolicyGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    description: str = Field()
    name: str = Field(pattern='^[^&<>! "]+$')
    from_policy_group: Optional[FromPolicyGroup] = Field(
        default=None, validation_alias="fromPolicyGroup", serialization_alias="fromPolicyGroup"
    )
    profiles: Optional[List[Profile]] = Field(
        default=None, description="list of profile ids that belongs to the policy group"
    )
    solution: Optional[Solution] = Field(default=None)


class ProfileInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field()
    profile_type: Optional[Literal["global"]] = Field(
        default=None, validation_alias="profileType", serialization_alias="profileType"
    )


class PolicyGroupId(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID
    profiles: Optional[List[ProfileInfo]] = Field(
        default=None,
        description="(Optional - only applicable for AON) List of profile ids that belongs to the policy group",
    )
