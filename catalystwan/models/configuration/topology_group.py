from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Profile(BaseModel):
    id: UUID


class FromTopologyGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    copy_: UUID = Field(validation_alias="copy", serialization_alias="copy")


class TopologyGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    description: str
    name: str = Field(pattern='^[^&<>! "]+$')
    from_topology_group: Optional[FromTopologyGroup] = Field(
        default=None, validation_alias="fromTopologyGroup", serialization_alias="fromTopologyGroup"
    )
    profiles: Optional[List[Profile]] = Field(
        default=None, description="list of profile ids that belongs to the topology group"
    )
    solution: Optional[Literal["sdwan"]] = Field(default=None)

    def add_profiles(self, ids: List[UUID]):
        if self.profiles is None:
            self.profiles = []
        self.profiles.extend([Profile(id=i) for i in ids])


class ActivateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    deactivate_topology: bool = Field(validation_alias="deactivateTopology", serialization_alias="deactivateTopology")


class DeployResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parent_task_id: str = Field(validation_alias="parentTaskId", serialization_alias="parentTaskId")


class Preview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    existing_config: str = Field(validation_alias="existingConfig", serialization_alias="existingConfig")
    new_config: str = Field(validation_alias="newConfig", serialization_alias="newConfig")


class TopologyGroupId(BaseModel):
    id: UUID
