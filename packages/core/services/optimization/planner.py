"""Optimization Planner mapping modes and presets to safe actionable run lists."""

from enum import Enum
from typing import NamedTuple, Optional
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class OptimizationMode(Enum):
    """Primary system optimization mode tiers."""
    BALANCED = "BALANCED"
    PERFORMANCE = "PERFORMANCE"
    POWER_SAVER = "POWER_SAVER"


class OptimizationPreset(Enum):
    """Optional performance target presets under PERFORMANCE mode."""
    GAMING = "GAMING"
    RENDERING = "RENDERING"
    BENCHMARK = "BENCHMARK"


class OptimizationAction(NamedTuple):
    """Representation of a safe planned system tuning task."""
    type: str  # e.g., 'power_plan', 'maintenance_job'
    target: str  # target GUID or service action
    params: dict


class OptimizationPlan:
    """Planned sequence of optimization tasks to execute."""

    def __init__(self, mode: OptimizationMode, preset: Optional[OptimizationPreset] = None) -> None:
        """Initialize the Optimization Plan.
        
        Args:
            mode: Target optimization mode.
            preset: Optional target sub-preset.
        """
        self.mode = mode
        self.preset = preset
        self.actions: list[OptimizationAction] = []


class OptimizationPlanner:
    """Computes and validates target optimization strategies based on safety constraints."""

    def __init__(self) -> None:
        """Initialize the Optimization Planner."""
        # Standard power plan GUIDs
        self.power_plans = {
            OptimizationMode.BALANCED: "381b4222-f694-41f0-9685-ff5bb260df2e",
            OptimizationMode.PERFORMANCE: "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            OptimizationMode.POWER_SAVER: "a1841308-3541-4fab-bc81-f71556f20b4a"
        }
        logger.info("Optimization Planner initialized.")

    def create_plan(self, mode: OptimizationMode, preset: Optional[OptimizationPreset] = None) -> OptimizationPlan:
        """Generates an action sequence for the targeted optimization profile.
        
        Args:
            mode: Main power plan mode tier.
            preset: Optional optimization sub-preset.
            
        Returns:
            OptimizationPlan sequence object.
        """
        plan = OptimizationPlan(mode, preset)
        guid = self.power_plans.get(mode, self.power_plans[OptimizationMode.BALANCED])
        
        # 1. Register main power plan switch action
        plan.actions.append(OptimizationAction(
            type="power_plan",
            target=guid,
            params={"mode_name": mode.value}
        ))

        # 2. Register maintenance cleanup for performance-oriented modes
        if mode == OptimizationMode.PERFORMANCE:
            plan.actions.append(OptimizationAction(
                type="maintenance_job",
                target="temp_cleanup",
                params={"depth": "thorough"}
            ))
            plan.actions.append(OptimizationAction(
                type="maintenance_job",
                target="dns_flush",
                params={}
            ))
            
            # Preset-specific scaling
            if preset == OptimizationPreset.GAMING:
                # Add networking/game preset tags
                plan.actions.append(OptimizationAction(
                    type="preset_hint",
                    target="gaming_priority",
                    params={"tcp_tuning_suggested": True}
                ))
            elif preset == OptimizationPreset.RENDERING:
                plan.actions.append(OptimizationAction(
                    type="preset_hint",
                    target="rendering_affinity",
                    params={"cpu_boost": True}
                ))

        elif mode == OptimizationMode.BALANCED:
            # Safe minor optimization for Balanced
            plan.actions.append(OptimizationAction(
                type="maintenance_job",
                target="dns_flush",
                params={}
            ))

        logger.info(f"Planned {len(plan.actions)} safe actions for {mode.value} (Preset: {preset.value if preset else 'None'})")
        return plan
