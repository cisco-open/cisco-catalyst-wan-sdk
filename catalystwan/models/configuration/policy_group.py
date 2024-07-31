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
    """Payload for creating a policy group.
    Policy Object Profile is required to create a policy group."""

    model_config = ConfigDict(populate_by_name=True)
    description: str = Field(
        description="description of the policy group. Max length is ulimited. (>500 000 for 20.12)"
    )
    name: str = Field(pattern='^[^&<>! "]+$', max_length=128)
    from_policy_group: Optional[FromPolicyGroup] = Field(
        default=None, validation_alias="fromPolicyGroup", serialization_alias="fromPolicyGroup"
    )
    profiles: Optional[List[Profile]] = Field(
        default=None, description="list of profile ids that belongs to the policy group"
    )
    solution: Optional[Solution] = Field(default=None)

    def add_profile(self, profile_uuid: UUID) -> None:
        if self.profiles is None:
            self.profiles = []
        self.profiles.append(Profile(id=profile_uuid))


class ProfileInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field()
    profile_type: Optional[Literal["global"]] = Field(
        default=None, validation_alias="profileType", serialization_alias="profileType"
    )
    name: str


class PolicyGroupId(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID
    profiles: Optional[List[ProfileInfo]] = Field(
        default=None,
        description="(Optional - only applicable for AON) List of profile ids that belongs to the policy group",
    )

    def get_profile_by_name(self, name: str) -> Optional[ProfileInfo]:
        if self.profiles is None:
            return None

        for profile in self.profiles:
            if profile.name == name:
                return profile
        return None


class PolicyGroupInfo(PolicyGroupId):
    name: str
