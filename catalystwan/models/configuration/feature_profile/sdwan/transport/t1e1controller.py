from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_global

ControllerType = Literal[
    "e1",
    "t1",
]


T1Framing = Literal[
    "esf",
    "sf",
]

T1Linecode = Literal[
    "ami",
    "b8zs",
]

T1Name = Literal[
    "T1",
    # By default, the name is T1
]


class T1(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    framing: Optional[Union[Global[T1Framing], Variable, Default[None]]] = Field(default=None)
    linecode: Optional[Union[Global[T1Linecode], Variable, Default[None]]] = Field(default=None)
    name: Optional[Global[T1Name]] = Field(default=as_global("T1", T1Name))


class T1Basic(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    t1: T1 = Field(validation_alias="T1", serialization_alias="T1")


E1Framing = Literal[
    "crc4",
    "no-crc4",
]

E1Linecode = Literal[
    "ami",
    "hdb3",
]

E1Name = Literal[
    "E1",
    # By default, the name is E1
]


class E1(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    framing: Optional[Union[Global[E1Framing], Variable, Default[None]]] = Field(default=None)
    linecode: Optional[Union[Global[E1Linecode], Variable, Default[None]]] = Field(default=None)
    name: Optional[Global[E1Name]] = Field(default=as_global("E1", E1Name))


class E1Basic(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    e1: E1 = Field(validation_alias="E1", serialization_alias="E1")


class CableLength(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cable_length: Optional[Default[None]] = Field(
        default=None, validation_alias="cableLength", serialization_alias="cableLength"
    )


LengthShort = Literal[
    "110ft",
    "220ft",
    "330ft",
    "440ft",
    "550ft",
    "660ft",
]


class CableLengthShort(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cable_length: Optional[Global[Literal["short"]]] = Field(
        default=None, validation_alias="cableLength", serialization_alias="cableLength"
    )
    length_short: Optional[Union[Global[LengthShort], Variable]] = Field(
        default=None, validation_alias="lengthShort", serialization_alias="lengthShort"
    )


Long = Literal["long"]

LengthLong = Literal[
    "-15db",
    "-22.5db",
    "-7.5db",
    "0db",
]


class CableLengthLong(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cable_length: Optional[Global[Long]] = Field(
        default=as_global("long", Long), validation_alias="cableLength", serialization_alias="cableLength"
    )
    length_long: Optional[Union[Global[LengthLong], Variable]] = Field(
        default=None, validation_alias="lengthLong", serialization_alias="lengthLong"
    )


ClockSource = Literal[
    "internal",
    "line",
    "loop-timed",
    "network",
]

LineMode = Literal[
    "primary",
    "secondary",
]


class ChannelGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    number: Union[Global[int], Variable] = Field()
    timeslots: Union[Global[str], Variable] = Field()


class ControllerTxExList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    basic: Union[T1Basic, E1Basic]
    cable: Optional[Union[CableLength, CableLengthShort, CableLengthLong]] = Field(default=None)
    channel_group: Optional[List[ChannelGroup]] = Field(
        default=None,
        validation_alias="channelGroup",
        serialization_alias="channelGroup",
        description="Channel Group List",
    )
    clock_source: Optional[Union[Global[ClockSource], Default[None]]] = Field(
        default=None, validation_alias="clockSource", serialization_alias="clockSource"
    )
    description: Optional[Union[Global[str], Variable, Default[None]]] = Field(default=None)
    line_mode: Optional[Union[Global[LineMode], Variable, Default[None]]] = Field(
        default=None, validation_alias="lineMode", serialization_alias="lineMode"
    )


class T1E1ControllerParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["t1-e1-controller"] = Field(default="t1-e1-controller", exclude=True)
    controller_tx_ex_list: List[ControllerTxExList] = Field(
        validation_alias=AliasPath("data", "controllerTxExList"), description="Controller tx-ex List"
    )
    slot: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "slot"))
    type: Optional[Global[ControllerType]] = Field(default=None, validation_alias=AliasPath("data", "type"))
