from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_optional_global


class ScalableGroupTagEntries(BaseModel):
    sgt_name: Optional[Global[str]] = Field(default=None, validation_alias="sgtName", serialization_alias="sgtName")
    tag: Optional[Global[str]] = Field(default=None)


class ScalableGroupTagParcel(_ParcelBase):
    entries: List[ScalableGroupTagEntries] = Field(validation_alias=AliasPath("data", "entries"), default_factory=list)

    def add_entry(self, sgt_name: Optional[str] = None, tag: Optional[str] = None):
        self.entries.append(
            ScalableGroupTagEntries(
                sgt_name=as_optional_global(sgt_name),
                tag=as_optional_global(tag),
            )
        )
