from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class Target(BaseModel):
    vpn: Global[List[str]] = as_global([])


class MeshParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["mesh"] = Field(default="mesh", exclude=True)
    target: Target = Field(default=Target(), validation_alias=AliasPath("data", "target"), description="Target Vpn")
    sites: Global[List[str]] = Field(default=as_global([]), validation_alias=AliasPath("data", "sites"))

    def add_target_vpn(self, vpn: str) -> None:
        self.target.vpn.value.append(vpn)

    def add_site(self, site: str) -> None:
        self.sites.value.append(site)
