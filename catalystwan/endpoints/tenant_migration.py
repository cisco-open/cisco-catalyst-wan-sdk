# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from pathlib import Path
from typing import List, Union
from urllib.parse import parse_qs, urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.endpoints import APIEndpoints, CustomPayloadType, PreparedPayload, get, post, versions, view
from catalystwan.models.tenant import TenantExport
from catalystwan.utils.session_type import ProviderView, SingleTenantView


class MigrationTokenQueryParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    migration_id: Union[List[str], str] = Field(serialization_alias="migrationId", validation_alias="migrationId")

    @field_validator("migration_id")
    @classmethod
    def single_migration_id_required(cls, value: Union[List[str], str]):
        if isinstance(value, list):
            return value[0]
        return value


class ExportInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    process_id: str = Field(serialization_alias="processId", validation_alias="processId")


class ImportInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    process_id: str = Field(serialization_alias="processId", validation_alias="processId")
    migration_token_url: str = Field(serialization_alias="migrationTokenURL", validation_alias="migrationTokenURL")

    @property
    def migration_token_query(self) -> str:
        return urlsplit(self.migration_token_url).query

    @property
    def migration_token_query_params(self) -> MigrationTokenQueryParams:
        query = self.migration_token_query
        return MigrationTokenQueryParams(**parse_qs(query))


class MigrationInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    process_id: str = Field(serialization_alias="processId", validation_alias="processId")


class MigrationFile(CustomPayloadType):
    def __init__(self, filename: Path):
        self.filename = filename

    def prepared(self) -> PreparedPayload:
        data = open(self.filename, "rb")
        return PreparedPayload(files={"file": (Path(data.name).name, data)})


class TenantMigration(APIEndpoints):
    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @get("/tenantmigration/download/{path}")
    def download_tenant_data(self, path: str = "default.tar.gz") -> bytes:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @post("/tenantmigration/export")
    def export_tenant_data(self, payload: TenantExport) -> ExportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @get("/tenantmigration/migrationToken")
    def get_migration_token(self, params: MigrationTokenQueryParams) -> str:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6,<20.13")
    @post("/tenantmigration/import")
    def import_tenant_data(self, payload: MigrationFile) -> ImportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.13")
    @post("/tenantmigration/import/{migration_key}")
    def import_tenant_data_with_key(self, payload: MigrationFile, migration_key: str) -> ImportInfo:
        ...

    @view({SingleTenantView, ProviderView})
    @versions(">=20.6")
    @post("/tenantmigration/networkMigration")
    def migrate_network(self, payload: str) -> MigrationInfo:
        ...

    def retrigger_network_migration(self):
        # GET /tenantmigration/networkMigration
        ...
