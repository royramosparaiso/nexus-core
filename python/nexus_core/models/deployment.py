"""Deployment modality — where a Platform runs."""

from typing import Literal

from pydantic import BaseModel

Modality = Literal["local", "fly", "k8s", "onprem", "saas"]


class DeploymentConfig(BaseModel):
    modality: Modality
    domain: str | None = None
    region: str | None = None
    tls: bool = True
    autoscale: bool = False
