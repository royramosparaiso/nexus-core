"""Bootstrap request/response tests."""

from uuid import uuid4

from nexus_core.contracts.bootstrap import (
    BootstrapRequest, BootstrapResponse, BootstrapStatus,
)
from nexus_core.jwt import ConsoleKeypair
from nexus_core.models import (
    AreasConfig, DeploymentConfig, GovernanceConfig, InstanceManifest,
    LlmConfig, LlmRoleAssignment, MemoryConfig, PersonaConfig,
)


def _manifest():
    return InstanceManifest(
        name="test",
        persona=PersonaConfig(display_name="Test"),
        deployment=DeploymentConfig(modality="local"),
        llms=LlmConfig(
            enabled_providers=["ollama"],
            roles=LlmRoleAssignment(
                planner="llama3.1:70b", coordinator="llama3.1:8b",
                worker="llama3.1:8b", embeddings="nomic-embed-text",
            ),
        ),
        memory=MemoryConfig(),
        areas=AreasConfig(enabled=["personal_organization"]),
        governance=GovernanceConfig(),
    )


def test_bootstrap_request_roundtrip():
    kp = ConsoleKeypair.generate()
    req = BootstrapRequest(
        instance_id=uuid4(),
        console_public_key_pem=kp.public_pem(),
        console_webhook_url="https://console.local/callbacks",
        manifest=_manifest(),
    )
    data = req.model_dump(mode="json")
    restored = BootstrapRequest.model_validate(data)
    assert restored.instance_id == req.instance_id
    assert restored.manifest.name == "test"


def test_bootstrap_response_variants():
    ok = BootstrapResponse(
        status=BootstrapStatus.OK,
        platform_public_key_pem="---BEGIN...",
        platform_version="0.1.0",
        applied_areas=["personal_organization"],
    )
    assert ok.status == BootstrapStatus.OK

    fail = BootstrapResponse(
        status=BootstrapStatus.INVALID_TOKEN,
        error_detail="bad bootstrap token",
    )
    assert fail.platform_public_key_pem is None
