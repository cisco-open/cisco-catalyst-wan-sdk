from dataclasses import dataclass
from json import dumps
from pathlib import Path
from typing import Callable, cast
from uuid import UUID

from catalystwan.models.configuration.config_migration import ConfigTransformResult, UX1Config, UX2ConfigPushResult
from catalystwan.models.configuration.feature_profile.parcel import Parcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.session import ManagerSession
from catalystwan.typed_list import DataSequence
from catalystwan.utils.config_migration.creators.groups_of_interests_pusher import get_parcel_ordering_value
from catalystwan.workflows.config_migration import (
    collect_ux1_config,
    log_progress,
    push_ux2_config,
    rollback_ux2_config,
    transform,
)

DEFAULT_ARTIFACT_DIR = "artifacts"


@dataclass
class ConfigMigrationRunner:
    session: ManagerSession
    collect: bool = True
    push: bool = True
    rollback: bool = False
    artifact_dir = Path(DEFAULT_ARTIFACT_DIR)
    progress: Callable[[str, int, int], None] = log_progress

    def __post_init__(self) -> None:
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        self.ux1_dump: Path = self.artifact_dir / Path("ux1.json")
        self.ux2_dump: Path = self.artifact_dir / Path("ux2.json")
        self.ux2_push_dump: Path = self.artifact_dir / Path("ux2-push-result.json")
        self.ux1_schema_dump: Path = self.artifact_dir / Path("ux1-schema.json")
        self.transform_schema_dump: Path = self.artifact_dir / Path("transform-result-schema.json")
        self.push_schema_dump: Path = self.artifact_dir / Path("push-result-schema.json")

    @staticmethod
    def collect_only(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=True, push=False, rollback=False)

    @staticmethod
    def collect_and_push(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=True, push=True, rollback=False)

    @staticmethod
    def rollback_only(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=False, push=False, rollback=True)

    @staticmethod
    def transform_only(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=False, push=False, rollback=False)

    @staticmethod
    def push_only(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=False, push=True, rollback=False)

    @staticmethod
    def push_and_rollback(session: ManagerSession) -> "ConfigMigrationRunner":
        return ConfigMigrationRunner(session=session, collect=False, push=True, rollback=True)

    def dump_schemas(self):
        with open(self.ux1_schema_dump, "w") as f:
            f.write(dumps(UX1Config.model_json_schema(by_alias=True), indent=4))
        with open(self.transform_schema_dump, "w") as f:
            f.write(dumps(ConfigTransformResult.model_json_schema(by_alias=True), indent=4))
        with open(self.push_schema_dump, "w") as f:
            f.write(dumps(UX2ConfigPushResult.model_json_schema(by_alias=True), indent=4))

    def clear_ux2(self) -> None:
        with self.session.login() as session:
            # GROUPS
            self.progress("deleting config groups...", 1, 12)
            session.api.config_group.delete_all()

            self.progress("deleting topology groups...", 2, 12)
            tg_api = session.endpoints.configuration.topology_group
            for tg in tg_api.get_all():
                tg_api.delete(tg.id)

            self.progress("deleting policy groups...", 2, 12)
            pg_api = session.endpoints.configuration.policy_group
            for pg in pg_api.get_all():
                pg_api.delete(pg.id)

            # PROFILES
            fp_api = session.api.sdwan_feature_profiles

            self.progress("deleting application priority profiles...", 3, 12)
            fp_api.application_priority.delete_all_profiles()

            self.progress("deleting cli profiles...", 4, 12)
            fp_api.cli.delete_all_profiles()

            self.progress("deleting dns security profiles...", 5, 12)
            fp_api.dns_security.delete_all_profiles()

            self.progress("deleting embedded security profiles...", 5, 12)
            fp_api.embedded_security.delete_all_profiles()

            self.progress("deleting other profiles...", 6, 12)
            fp_api.other.delete_all_profiles()

            self.progress("deleting service profiles...", 7, 12)
            fp_api.service.delete_all_profiles()

            self.progress("deleting sig security profiles...", 8, 12)
            fp_api.sig_security.delete_all_profiles()

            self.progress("deleting system profiles...", 9, 12)
            fp_api.system.delete_all_profiles()

            self.progress("deleting transport profiles...", 10, 12)
            fp_api.transport.delete_all_profiles()

            self.progress("deleting topology profiles...", 11, 12)
            fp_api.topology.delete_all_profiles()

            self.progress("deleting default policy object profile parcels...", 12, 12)
            po_profiles = fp_api.policy_object.get_profiles()
            if len(po_profiles) > 1:
                print("WARNING! MORE THAN ONE DEFAULT POLICY OBJECT PROFILE DETECTED")

            for po_profile in po_profiles:
                sorted_parcel_types = sorted(
                    list_types(AnyPolicyObjectParcel), key=lambda x: get_parcel_ordering_value(x), reverse=True
                )

                for dpo_parcel_type in sorted_parcel_types:
                    for parcel in cast(
                        DataSequence[Parcel[AnyPolicyObjectParcel]],
                        fp_api.policy_object.get(po_profile.profile_id, dpo_parcel_type),
                    ):
                        if parcel.created_by != "system":
                            parcel_uuid = UUID(str(parcel.parcel_id))
                            fp_api.policy_object.delete(po_profile.profile_id, type(parcel.payload), parcel_uuid)

    def run(self):
        with self.session.login() as session:
            # collext and dump ux1 to json file
            if self.collect:
                ux1 = collect_ux1_config(session, self.progress)
                # ux1.templates = UX1Templates()
                with open(self.ux1_dump, "w") as f:
                    f.write(ux1.model_dump_json(exclude_none=True, by_alias=True, indent=4, warnings=False))

            # transform to ux2 and dump to json file
            _transform_result = transform(UX1Config.model_validate_json(open(self.ux1_dump).read()), True)
            with open(self.ux2_dump, "w") as f:
                f.write(_transform_result.model_dump_json(exclude_none=True, by_alias=True, indent=4, warnings=False))

            # push ux2 to remote and dump push result
            if self.push:
                transform_result = ConfigTransformResult.model_validate_json(open(self.ux2_dump).read())
                ux2_push_result = push_ux2_config(session, transform_result.ux2_config, self.progress)
                with open(self.ux2_push_dump, "w") as f:
                    f.write(ux2_push_result.model_dump_json(exclude_none=True, by_alias=True, indent=4, warnings=False))

            # rollback
            if self.rollback:
                ux2_push_result = UX2ConfigPushResult.model_validate_json(open(self.ux2_push_dump).read())
                rollback_ux2_config(session, ux2_push_result.rollback, self.progress)
