# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from typing import Dict
from uuid import UUID, uuid4

from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.aip import (
    AdvancedInspectionProfileParcel,
)
from catalystwan.utils.config_migration.creators.references_updater import update_parcel_references


class TestReferencesUpdater(unittest.TestCase):
    def test_update_parcel_references(self):
        intrusion_prevention_origin_ref = uuid4()
        amp_origin_ref = uuid4()
        url_filtering_origin_ref = uuid4()

        pushed_objects: Dict[UUID, UUID] = {
            intrusion_prevention_origin_ref: uuid4(),
            amp_origin_ref: uuid4(),
            url_filtering_origin_ref: uuid4(),
        }

        aip_parcel = AdvancedInspectionProfileParcel.create(
            "aip1",
            "description1",
            intrusion_prevention=intrusion_prevention_origin_ref,
            advanced_malware_protection=amp_origin_ref,
            url_filtering=url_filtering_origin_ref,
        )

        updated_parcel = update_parcel_references(aip_parcel, pushed_objects)

        assert updated_parcel is not aip_parcel
        assert updated_parcel.intrusion_prevention.ref_id.value == str(pushed_objects[intrusion_prevention_origin_ref])
        assert updated_parcel.advanced_malware_protection.ref_id.value == str(pushed_objects[amp_origin_ref])
        assert updated_parcel.url_filtering.ref_id.value == str(pushed_objects[url_filtering_origin_ref])
        assert updated_parcel.ssl_decryption_profile is None
        assert updated_parcel.tls_decryption_action == aip_parcel.tls_decryption_action
        assert updated_parcel.parcel_name == aip_parcel.parcel_name
        assert updated_parcel.parcel_description == aip_parcel.parcel_description

    def test_not_update_parcel_references(self):
        intrusion_prevention_origin_ref = uuid4()
        amp_origin_ref = uuid4()
        url_filtering_origin_ref = uuid4()

        pushed_objects: Dict[UUID, UUID] = {}

        aip_parcel = AdvancedInspectionProfileParcel.create(
            "aip1",
            "description1",
            intrusion_prevention=intrusion_prevention_origin_ref,
            advanced_malware_protection=amp_origin_ref,
            url_filtering=url_filtering_origin_ref,
        )

        updated_parcel = update_parcel_references(aip_parcel, pushed_objects)

        assert updated_parcel.model_dump_json() == aip_parcel.model_dump_json()
