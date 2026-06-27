"""Trend Analysis Service calculating temperature slopes, battery degradations, and period comparisons."""

import time
from typing import Optional
from packages.core.container import ServiceContainer
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")


class TrendAnalysisService:
    """Computes trends, anomaly alerts, degradation projections, and period differences."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Trend Analysis Service.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        logger.info("Trend Analysis Service initialized.")

    def calculate_gradient(self, values: list[float]) -> float:
        """Calculates a simple linear regression slope coefficient (gradient) for data trend.
        
        Args:
            values: List of numeric values over time.
            
        Returns:
            The gradient slope value. Positive indicates upward trend.
        """
        n = len(values)
        if n < 2:
            return 0.0
            
        x = list(range(n))
        mean_x = sum(x) / n
        mean_y = sum(values) / n
        
        num = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        den = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        if den == 0:
            return 0.0
        return num / den

    def analyze_trends(self, limit_hours: int = 168) -> dict:
        """Analyzes active telemetry trends for temperatures, RAM, and battery forecast.
        
        Args:
            limit_hours: Database lookup scope. Default is 168 (7 days).
            
        Returns:
            Analytics summary report dictionary.
        """
        history_svc = self.container.get("telemetry_history_service")
        logs = history_svc.get_history(limit_hours=limit_hours)
        
        if not logs or len(logs) < 3:
            return {
                "status": "INSUFFICIENT_DATA",
                "message": "Need at least 3 historical records to calculate linear gradients."
            }

        cpu_temps = [l["cpu_temperature"] for l in logs if l.get("cpu_temperature") is not None]
        ram_pcts = [l["ram_percentage"] for l in logs if l.get("ram_percentage") is not None]
        bat_pcts = [l["battery_health_percent"] for l in logs if l.get("battery_health_percent") is not None]

        cpu_grad = self.calculate_gradient(cpu_temps) if cpu_temps else 0.0
        ram_grad = self.calculate_gradient(ram_pcts) if ram_pcts else 0.0
        bat_grad = self.calculate_gradient(bat_pcts) if bat_pcts else 0.0

        # Anomaly trigger alerts
        alerts = []
        if cpu_grad > 0.5:
            alerts.append({
                "metric": "CPU Temperature",
                "severity": "WARNING",
                "message": f"Elevated thermal build-up detected. Gradient +{cpu_grad:.2f}°C per record."
            })
        if ram_grad > 0.02:
            alerts.append({
                "metric": "RAM Allocation",
                "severity": "WARNING",
                "message": f"Active memory leakage pattern detected. Gradient +{ram_grad*100.0:.2f}% RAM allocation rate."
            })

        # Battery health degradation forecast projection
        battery_forecast = "Stable"
        if bat_grad < 0.0:
            # How many records to hit 80% health
            current_health = bat_pcts[-1]
            if current_health > 80:
                needed_degrade = current_health - 80
                degrade_rate = abs(bat_grad)
                records_to_limit = needed_degrade / degrade_rate
                # Assuming 1 log per hour in production context, map records to months
                projected_months = max(1.0, (records_to_limit * 1.0) / (24 * 30))
                battery_forecast = f"Degrading. Target limit (80% health) projected in {projected_months:.1f} months."
            else:
                battery_forecast = "Critical. Battery health is already below 80%."

        return {
            "status": "SUCCESS",
            "gradients": {
                "cpu_temperature": round(cpu_grad, 3),
                "ram_percentage": round(ram_grad, 4),
                "battery_health": round(bat_grad, 4)
            },
            "alerts": alerts,
            "battery_forecast": battery_forecast
        }

    def compare_yesterday_vs_today(self) -> dict:
        """Compares past 24h stats vs previous 24-48h stats."""
        history_svc = self.container.get("telemetry_history_service")
        logs = history_svc.get_history(limit_hours=48)
        
        if not logs or len(logs) < 2:
            return {"status": "INSUFFICIENT_DATA"}

        cutoff = time.time() - (24 * 3600)
        today_logs = [l for l in logs if l["timestamp"] >= cutoff]
        yesterday_logs = [l for l in logs if l["timestamp"] < cutoff]

        if not today_logs or not yesterday_logs:
            return {"status": "INSUFFICIENT_DATA"}

        today_cpu = sum(l["cpu_utilization"] for l in today_logs) / len(today_logs)
        yesterday_cpu = sum(l["cpu_utilization"] for l in yesterday_logs) / len(yesterday_logs)

        today_score = sum(l["health_score"] for l in today_logs) / len(today_logs)
        yesterday_score = sum(l["health_score"] for l in yesterday_logs) / len(yesterday_logs)

        return {
            "status": "SUCCESS",
            "cpu_utilization": {
                "yesterday": round(yesterday_cpu, 1),
                "today": round(today_cpu, 1),
                "delta": round(today_cpu - yesterday_cpu, 1)
            },
            "health_score": {
                "yesterday": round(yesterday_score, 1),
                "today": round(today_score, 1),
                "delta": round(today_score - yesterday_score, 1)
            }
        }
