# Copyright 2024 Cisco Systems, Inc. and its affiliates
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import as_optional_global
from catalystwan.models.configuration.config_migration import ConvertResult, PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.policy_settings import (
    PolicySettingsParcel,
)
from catalystwan.models.policy.localized import LocalizedPolicyInfo


def convert_localized_policy_settings(
    policy: LocalizedPolicyInfo, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[PolicySettingsParcel]:
    if isinstance(policy.policy_definition, str):
        return ConvertResult(
            output=None,
            status="unsupported",
            info=[
                f"Localized policy {policy.policy_name} has a string settings definition. "
                "This is not supported by the converter."
            ],
        )
    settings = policy.policy_definition.settings
    if settings is None:
        parcel = PolicySettingsParcel(
            parcel_name=f"{policy.policy_name}_Settings",
            parcel_description=policy.policy_description,
        )
        return ConvertResult(output=parcel, status="complete")
    parcel = PolicySettingsParcel(
        parcel_name=f"{policy.policy_name}_Settings",
        parcel_description=policy.policy_description,
        app_visibility=as_optional_global(settings.app_visibility),
        app_visibility_ipv6=as_optional_global(settings.app_visibility_ipv6),
        flow_visibility=as_optional_global(settings.flow_visibility),
        flow_visibility_ipv6=as_optional_global(settings.app_visibility_ipv6),
    )
    return ConvertResult(output=parcel, status="partial", info=["cflowd is not supported yet"])
