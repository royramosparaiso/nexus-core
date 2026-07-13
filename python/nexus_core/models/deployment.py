"""Deployment modality — where a Platform runs."""

from typing import Literal

from pydantic import BaseModel

Modality = Literal["local", "fly", "k8s", "onprem", "saas"]

# Agent runtime backend. See ADR-001 in nexus-platform.
# v0.6: only `in_process` is functional. `redis_workers` reserved for v0.7.
AgentRuntime = Literal["in_process", "redis_workers"]


class DeploymentConfig(BaseModel):
    modality: Modality
    domain: str | None = None
    region: str | None = None
    tls: bool = True
    autoscale: bool = False
    runtime: AgentRuntime = "in_process"
    worker_replicas: int = 1  # only used when runtime = redis_workers
