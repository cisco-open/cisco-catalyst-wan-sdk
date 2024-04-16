from unittest.mock import patch
from uuid import uuid4

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.configuration.config_migration import TransformedParcel, TransformHeader, UX2Config
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    IgmpAttributes,
    IgmpInterfaceParameters,
    LocalConfig,
    MulticastBasicAttributes,
    MulticastParcel,
    PimAttributes,
    SsmAttributes,
    SsmFlag,
)
from catalystwan.utils.config_migration.steps.transform import merge_parcels


def test_when_more_than_one_multicast_parcel_assigned_to_vpn_expect_expect_merge():
    # Arrange
    pim_uuid = uuid4()
    igmp_uuid = uuid4()
    multicast_uuid = uuid4()
    ux2_before = UX2Config(
        profile_parcels=[
            TransformedParcel(
                header=TransformHeader(
                    type="lan/vpn",
                    origin=uuid4(),
                    subelements=[pim_uuid, igmp_uuid, multicast_uuid],
                ),
                parcel=LanVpnParcel(
                    parcel_name="Service_VPN_3",
                    description="VPN Service",
                    vpn_id=as_global(3),
                ),
            ),
            TransformedParcel(
                header=TransformHeader(
                    type="routing/multicast",
                    origin=pim_uuid,
                ),
                parcel=MulticastParcel(
                    parcel_name="Service_PIM",
                    description="PIM Service",
                    pim=PimAttributes(ssm=SsmAttributes(ssm_range_config=SsmFlag())),
                ),
            ),
            TransformedParcel(
                header=TransformHeader(
                    type="routing/multicast",
                    origin=igmp_uuid,
                ),
                parcel=MulticastParcel(
                    parcel_name="Service_IGMP",
                    description="IGMP Service",
                    igmp=IgmpAttributes(
                        interface=[
                            IgmpInterfaceParameters(interface_name=as_global("GigabitEthernet0"), version=as_global(2))
                        ]
                    ),
                ),
            ),
            TransformedParcel(
                header=TransformHeader(
                    type="routing/multicast",
                    origin=multicast_uuid,
                ),
                parcel=MulticastParcel(
                    parcel_name="Service_Multicast",
                    description="Multicast Service",
                    basic=MulticastBasicAttributes(
                        spt_only=as_global(False),
                        local_config=LocalConfig(
                            threshold=as_global(13),
                        ),
                    ),
                ),
            ),
        ]
    )
    merged_uuid = uuid4()
    merged_parcel = TransformedParcel(
        header=TransformHeader(
            type="routing/multicast",
            origin=merged_uuid,
        ),
        parcel=MulticastParcel(
            parcel_name="Merged_Service_Multicast",
            parcel_description="Merged from: Service_IGMP, Service_Multicast, Service_PIM",
            basic=MulticastBasicAttributes(
                spt_only=as_global(False),
                local_config=LocalConfig(
                    threshold=as_global(13),
                ),
            ),
            igmp=IgmpAttributes(
                interface=[IgmpInterfaceParameters(interface_name=as_global("GigabitEthernet0"), version=as_global(2))]
            ),
            pim=PimAttributes(ssm=SsmAttributes(ssm_range_config=SsmFlag())),
        ),
    )
    # Act
    with patch("catalystwan.utils.config_migration.steps.transform.uuid4", return_value=merged_uuid):
        result = merge_parcels(ux2_before)
    # Assert
    assert len(result.profile_parcels) == 5
    assert result.profile_parcels[0].header.subelements == {merged_uuid}
    assert result.profile_parcels[-1] == merged_parcel


def test_when_one_multicast_parcel_assigned_to_vpn_expect_not_merge():
    # Arrange
    multicast_uuid = uuid4()
    ux2_before = UX2Config(
        profile_parcels=[
            TransformedParcel(
                header=TransformHeader(
                    type="lan/vpn",
                    origin=uuid4(),
                    subelements=[multicast_uuid],
                ),
                parcel=LanVpnParcel(
                    parcel_name="Service_VPN_3",
                    description="VPN Service",
                    vpn_id=as_global(3),
                ),
            ),
            TransformedParcel(
                header=TransformHeader(
                    type="routing/multicast",
                    origin=multicast_uuid,
                ),
                parcel=MulticastParcel(
                    parcel_name="Service_Multicast",
                    description="Multicast Service",
                    basic=MulticastBasicAttributes(
                        spt_only=as_global(False),
                        local_config=LocalConfig(
                            threshold=as_global(13),
                        ),
                    ),
                ),
            ),
        ]
    )
    # Act
    result = merge_parcels(ux2_before)
    # Assert
    assert len(result.profile_parcels) == 2


def test_when_no_multicast_parcel_assigned_to_vpn_expect_not_merge():
    # Arrange
    ux2_before = UX2Config(
        profile_parcels=[
            TransformedParcel(
                header=TransformHeader(
                    type="lan/vpn",
                    origin=uuid4(),
                    subelements=[],
                ),
                parcel=LanVpnParcel(
                    parcel_name="Service_VPN_3",
                    description="VPN Service",
                    vpn_id=as_global(3),
                ),
            ),
        ]
    )
    # Act
    result = merge_parcels(ux2_before)
    # Assert
    assert len(result.profile_parcels) == 1
