"""
Policy Models

Represents a versioned Guardrail Policy loaded from YAML.

This model is intentionally lightweight for the proof of concept
while demonstrating policy lifecycle concepts.

Future Enhancements
-------------------
- PII masking
- Tool access policies
- Output validation
- Team-specific overrides
- Policy inheritance
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PolicyStatus(str, Enum):
    """Policy lifecycle states."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    CANARY = "CANARY"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"


class SafetyPolicy(BaseModel):
    """Safety policy configuration."""

    # Metadata
    version: str
    description: Optional[str] = None
    status: PolicyStatus = PolicyStatus.DRAFT

    # Guardrails
    toxicity_threshold: float
    prompt_injection_detection: bool = False

    # Future rule examples
    # block_hate_speech: bool = True
    # max_tokens: int = 8000
    # pii_masking: bool = True