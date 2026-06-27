"""Intelligence alert data models for Aegis Core Platform."""

from dataclasses import dataclass
from typing import Literal

# Severity tiers for Windows Intelligence alerts
Severity = Literal["INFO", "WARNING", "CRITICAL"]

# Category tiers for Windows Intelligence alerts
Category = Literal["VIRTUALIZATION", "SECURITY", "POWER", "STORAGE", "PERFORMANCE", "SYSTEM"]


@dataclass(frozen=True)
class IntelligenceAlert:
    """Represents a single Windows Intelligence detection alert."""
    title: str
    message: str
    severity: Severity
    category: Category
    action: str = ""
