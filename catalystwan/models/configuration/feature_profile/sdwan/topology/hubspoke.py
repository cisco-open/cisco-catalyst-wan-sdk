from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class Target(BaseModel):
    vpn: Global[List[str]] = as_global([])


class HubSite(BaseModel):
    sites: Global[List[str]]
    preference: Global[int]


class Spoke(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: Global[str]
    spoke_sites: Global[List[str]] = Field(
        default=as_global([]), validation_alias="spokeSites", serialization_alias="spokeSites"
    )
    hub_sites: Optional[List[HubSite]] = Field(
        default=None, validation_alias="hubSites", serialization_alias="hubSites"
    )

    @staticmethod
    def create(name: str, spoke_sites: List[str]) -> "Spoke":
        return Spoke(name=as_global(name), spoke_sites=Global[List[str]](value=spoke_sites))

    def add_hub_site(self, sites: List[str], preference: int) -> HubSite:
        hub_site = HubSite(sites=Global[List[str]](value=sites), preference=as_global(preference))
        if self.hub_sites is None:
            self.hub_sites = [hub_site]
        else:
            self.hub_sites.append(hub_site)
        return hub_site

    def add_spoke_site(self, site: str):
        self.spoke_sites.value.append(site)


class HubSpokeParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["hubspoke"] = Field(default="hubspoke", exclude=True)
    target: Target = Field(default=Target(), validation_alias=AliasPath("data", "target"))
    selected_hubs: Global[List[str]] = Field(default=as_global([]), validation_alias=AliasPath("data", "selectedHubs"))
    spokes: List[Spoke] = Field(default=[], validation_alias=AliasPath("data", "spokes"))

    def add_spoke(self, name: str, spoke_sites: List[str]) -> Spoke:
        spoke = Spoke.create(name=name, spoke_sites=spoke_sites)
        self.spokes.append(spoke)
        return spoke

    def add_target_vpn(self, vpn: str) -> None:
        self.target.vpn.value.append(vpn)

    def add_selected_hub(self, hub: str) -> None:
        self.selected_hubs.value.append(hub)
