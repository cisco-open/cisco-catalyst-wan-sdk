# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
import datetime

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get


class WebServerCertificateInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    org_unit: str
    org: str
    location: str
    state: str
    country: str
    company_name: str
    not_before: datetime.datetime = Field(serialization_alias="notBefore", validation_alias="notBefore")
    not_after: datetime.datetime = Field(serialization_alias="notAfter", validation_alias="notAfter")
    certificate_details: str = Field(serialization_alias="certificateDetails", validation_alias="certificateDetails")
    validity: str


class CertificateManagementVManage(APIEndpoints):
    def dump_certificate(self):
        # GET /setting/configuration/webserver/certificate/certificate
        ...

    def get_certificate(self):
        # GET /setting/configuration/webserver/certificate/getcertificate
        ...

    def get_csr(self):
        # POST /setting/configuration/webserver/certificate
        ...

    def import_certificate(self):
        # PUT /setting/configuration/webserver/certificate
        ...

    def rollback(self):
        # GET /setting/configuration/webserver/certificate/rollback
        ...

    @get("/setting/configuration/webserver/certificate")
    def show_info(self) -> WebServerCertificateInfo:
        ...
