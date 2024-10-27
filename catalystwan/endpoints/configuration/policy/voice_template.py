# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put
from catalystwan.models.policy.voice import VoicePolicy, VoicePolicyEditResponse, VoicePolicyInfo
from catalystwan.typed_list import DataSequence


class ConfigurationVoiceTemplatePolicy(APIEndpoints):
    @post("/template/policy/voice")
    def create_voice_template(self, payload: VoicePolicy) -> None:
        ...

    @delete("/template/policy/voice/{id}")
    def delete_voice_template(self, id: UUID, payload: JSON = {}) -> None:
        ...

    @put("/template/policy/voice/{id}")
    def edit_voice_template(self, id: UUID, payload: VoicePolicy) -> VoicePolicyEditResponse:
        # PUT /template/policy/voice/{policyId}
        ...

    def generate_voice_policy_summary(self):
        # GET /template/policy/voice/summary
        ...

    @get("/template/policy/voice", "data")
    def generate_voice_template_list(self) -> DataSequence[VoicePolicyInfo]:
        ...

    @get("/template/policy/voice/definition/{id}")
    def get_voice_template(self, id: UUID) -> VoicePolicy:
        ...

    def get_voice_templates_for_device(self):
        # GET /template/policy/voice/{deviceModel}
        ...
