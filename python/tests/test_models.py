"""Smoke tests for shared models."""

import pytest
from pydantic import ValidationError

from nexus_core.models import (
    AreasConfig, AVAILABLE_AREAS, DeploymentConfig, GovernanceConfig,
    InstanceManifest, LlmConfig, LlmRoleAssignment, MemoryConfig, PersonaConfig,
)


def test_available_areas_all_have_slugs():
    slugs = {a.slug for a in AVAILABLE_AREAS}
    assert len(slugs) == 10
    assert "personal_organization" in slugs
    assert "operations" in slugs


def test_areas_config_rejects_unknown_slug():
    with pytest.raises(ValidationError):
        AreasConfig(enabled=["personal_organization", "not_a_real_area"])


def test_persona_locale_pattern():
    with pytest.raises(ValidationError):
        PersonaConfig(display_name="X", default_locale="not-a-locale")


def test_instance_manifest_roundtrip():
    manifest = InstanceManifest(
        name="test",
        persona=PersonaConfig(display_name="Test"),
        deployment=DeploymentConfig(modality="local"),
        llms=LlmConfig(
            enabled_providers=["ollama"],
            roles=LlmRoleAssignment(
                planner="llama3.1:70b",
                coordinator="llama3.1:8b",
                worker="llama3.1:8b",
                embeddings="nomic-embed-text",
            ),
        ),
        memory=MemoryConfig(),
        areas=AreasConfig(enabled=["personal_organization"]),
        governance=GovernanceConfig(),
    )
    data = manifest.model_dump(mode="json", by_alias=True)
    assert data["apiVersion"] == "nexus.v0.6"
    restored = InstanceManifest.model_validate(data)
    assert restored.name == "test"
