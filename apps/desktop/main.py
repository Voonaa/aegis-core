import sys
import traceback
import datetime
from pathlib import Path
from tkinter import messagebox

from packages.core.container import ServiceContainer
from packages.core.config_manager import ConfigManager
from packages.core.event_bus import EventBus
from packages.core.services.health_service import HealthService as HealthEngine
from packages.core.profile_manager import ProfileManager
from packages.core.command_registry import CommandRegistry
from packages.core.plugins.loader import PluginLoader
from apps.desktop.ui.theme import ThemeManager
from packages.core.services.hardware_service import HardwareService
from packages.core.services.report_service import ReportService
from packages.core.services.privilege_service import PrivilegeService
from packages.core.services.repair_service import RepairService
from packages.core.services.maintenance_service import MaintenanceService
from packages.core.services.recommendation import RecommendationService
from packages.core.jobs import JobManager
from apps.desktop.app import AegisApp, DEFAULT_SETTINGS

from packages.core.constants.paths import PROJECT_ROOT
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

def handle_crash(exctype: type[BaseException], value: BaseException, tb: any) -> None:
    """Intercepts unhandled critical exceptions, logs tracebacks, and pops tkinter errors."""
    crash_dir = PROJECT_ROOT / "logs" / "crash"
    try:
        crash_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    crash_file = crash_dir / f"crash_{timestamp}.log"
    try:
        with open(crash_file, "w", encoding="utf-8") as f:
            f.write(f"AEGIS CORE CRASH REPORT - {datetime.datetime.now()}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Exception Type: {exctype.__name__}\n")
            f.write(f"Exception Value: {value}\n\n")
            f.write("Traceback:\n")
            traceback.print_exception(exctype, value, tb, file=f)
    except Exception:
        pass

    try:
        logger.critical(f"Unhandled critical crash! Details written to: {crash_file}", exc_info=(exctype, value, tb))
    except Exception:
        pass

    try:
        messagebox.showerror(
            "Aegis Core Platform Crash",
            f"An unexpected critical error occurred:\n\n{value}\n\nDetails have been logged to:\n{crash_file}"
        )
    except Exception:
        pass

    sys.__excepthook__(exctype, value, tb)

# Bind custom excepthook handler
sys.excepthook = handle_crash

def register_default_cli_commands(registry: CommandRegistry, container: ServiceContainer) -> None:
    """Pre-registers core commands inside the Developer Console CLI engine.
    
    Args:
        registry: The active CommandRegistry.
        container: Service container reference.
    """
    # 1. 'help' command
    def cmd_help() -> str:
        help_info = registry.get_help_list()
        lines = ["Available CLI Commands:"]
        for name, txt in help_info.items():
            lines.append(f"  - {name:<10} : {txt}")
        return "\n".join(lines)
    registry.register("help", cmd_help, "Displays available commands checklist.")

    # 2. 'status' command
    def cmd_status() -> str:
        profile_mgr: ProfileManager = container.get("profile_manager")
        detected = profile_mgr.detect_profile()
        health_eng: HealthEngine = container.get("health_engine")
        score = health_eng.calculate_score()
        return (
            f"Aegis status report:\n"
            f"  - Target Profile : {detected}\n"
            f"  - Health Rating  : {score}/100\n"
            f"  - OS Status      : Operational\n"
            f"  - Virtualization : Hyper-V Active"
        )
    registry.register("status", cmd_status, "Queries current system status indicators.")

    # 3. 'repair' command
    def cmd_repair(*args: str) -> str:
        if not args:
            return "Usage: repair <sfc | dism | chkdsk>"
        sub = args[0].lower()
        
        rep_svc = container.get("repair_service")
        job_mgr = container.get("job_manager")

        if sub == "sfc":
            job_id = job_mgr.submit("SFC Scannow Verification", rep_svc.run_sfc)
            return f"SFC scan job submitted in background. Job ID: {job_id}"
        elif sub == "dism":
            job_id = job_mgr.submit("DISM RestoreHealth Image Scan", rep_svc.run_dism)
            return f"DISM restore job submitted in background. Job ID: {job_id}"
        elif sub == "chkdsk":
            job_id = job_mgr.submit("CHKDSK File System Verify", rep_svc.run_chkdsk)
            return f"CHKDSK verify job submitted in background. Job ID: {job_id}"
            
        return f"Unknown repair subsystem directive: '{sub}'"
    registry.register("repair", cmd_repair, "Executes system repair tasks: repair sfc, repair dism, repair chkdsk")

    # 4. 'report' command
    def cmd_report() -> str:
        rep_svc = container.get("report_service")
        return rep_svc.generate_report()
    registry.register("report", cmd_report, "Compiles and writes system diagnostics files to temp/")

    # 5. 'optimize' command
    def cmd_optimize(*args: str) -> str:
        if not args:
            return "Usage: optimize <performance [gaming|rendering] | balanced | saver | restore | status>"
        sub = args[0].lower()
        opt_svc = container.get("optimization_service")
        
        from packages.core.services.optimization.planner import OptimizationMode, OptimizationPreset
        
        if sub == "performance":
            preset = None
            if len(args) > 1:
                p_arg = args[1].lower()
                if p_arg == "gaming":
                    preset = OptimizationPreset.GAMING
                elif p_arg == "rendering":
                    preset = OptimizationPreset.RENDERING
            
            res = opt_svc.apply_optimization(OptimizationMode.PERFORMANCE, preset)
            preset_str = f" with preset {preset.value}" if preset else ""
            return f"Performance optimization{preset_str} applied. Status: {res['status']}. Active Power Plan: {res['power_plan']}."
            
        elif sub == "balanced":
            res = opt_svc.apply_optimization(OptimizationMode.BALANCED)
            return f"Balanced optimization applied. Status: {res['status']}. Active Power Plan: {res['power_plan']}."
            
        elif sub == "saver":
            res = opt_svc.apply_optimization(OptimizationMode.POWER_SAVER)
            return f"Power Saver optimization applied. Status: {res['status']}. Active Power Plan: {res['power_plan']}."
            
        elif sub == "restore":
            res = opt_svc.rollback()
            return f"Rollback operation executed. Status: {res['status']}. Details: {res.get('restored_file', res.get('reason'))}."
            
        elif sub == "status":
            state = opt_svc.capture_current_state()
            return (
                f"Current Optimization State:\n"
                f"  - Power Plan Scheme GUID: {state.get('power_plan')}\n"
                f"  - CPU Utilization:        {state.get('cpu_utilization')}%\n"
                f"  - Free Memory:            {state.get('free_ram_gb')} GB"
            )
            
        return f"Unknown optimize parameter directive: '{sub}'"
    registry.register("optimize", cmd_optimize, "Executes system optimization profiles: optimize performance [gaming|rendering], optimize balanced, optimize saver, optimize restore, optimize status")

    # 6. 'telemetry' command
    def cmd_telemetry(*args: str) -> str:
        if not args:
            return "Usage: telemetry <stats | export <csv|json|md|html> | clean>"
        
        sub = args[0].lower()
        history_svc = container.get("telemetry_history_service")
        
        if sub == "stats":
            logs = history_svc.get_history(limit_hours=168)
            if not logs:
                return "Telemetry History database is empty. No stats available."
                
            cpu_utils = [l["cpu_utilization"] for l in logs]
            cpu_temps = [l["cpu_temperature"] for l in logs]
            ram_pcts = [l["ram_percentage"] for l in logs]
            pings = [l["network_latency_ms"] for l in logs if l["network_latency_ms"] > 0]
            scores = [l["health_score"] for l in logs]
            
            avg_cpu = sum(cpu_utils) / len(cpu_utils)
            avg_temp = sum(cpu_temps) / len(cpu_temps)
            max_ram = max(ram_pcts) * 100.0 if ram_pcts else 0.0
            avg_ping = sum(pings) / len(pings) if pings else 0.0
            avg_score = sum(scores) / len(scores) if scores else 0.0

            # Query TrendAnalysisService analytics
            trend_svc = container.get("trend_analysis_service")
            trends = trend_svc.analyze_trends(limit_hours=168)
            compare = trend_svc.compare_yesterday_vs_today()

            output = [
                f"Aegis Telemetry History Stats (Last 7 Days - {len(logs)} records):",
                f"  - Average CPU Utilization : {avg_cpu:.1f}%",
                f"  - Average CPU Temperature : {avg_temp:.1f} C",
                f"  - Max RAM Footprint Peak  : {max_ram:.1f}%",
                f"  - Average Ping Latency    : {avg_ping:.1f} ms",
                f"  - Average System Health   : {avg_score:.1f}/100"
            ]

            if trends.get("status") == "SUCCESS":
                grads = trends.get("gradients", {})
                output.append("\nPerformance Trend Slopes (Gradients):")
                output.append(f"  - CPU Temp Gradient     : {grads.get('cpu_temperature'):+.3f}°C / record")
                output.append(f"  - RAM Peak Gradient     : {grads.get('ram_percentage')*100.0:+.3f}% / record")
                output.append(f"  - Battery Degradation   : {grads.get('battery_health'):+.4f}% / record")
                output.append(f"  - Battery Forecast      : {trends.get('battery_forecast')}")
                
                if trends.get("alerts"):
                    output.append("\nAnomaly Detection Alerts:")
                    for alert in trends.get("alerts", []):
                        output.append(f"  - [{alert.get('severity')}] {alert.get('metric')}: {alert.get('message')}")

            if compare.get("status") == "SUCCESS":
                cpu_c = compare.get("cpu_utilization", {})
                score_c = compare.get("health_score", {})
                output.append("\nYesterday vs. Today Comparison Delta:")
                output.append(f"  - CPU Avg Load          : {cpu_c.get('yesterday')}% -> {cpu_c.get('today')}% (Delta: {cpu_c.get('delta'):+.1f}%)")
                output.append(f"  - Health Rating Score   : {score_c.get('yesterday')} -> {score_c.get('today')} (Delta: {score_c.get('delta'):+.1f})")

            return "\n".join(output)
            
        elif sub == "export":
            if len(args) < 2:
                return "Usage: telemetry export <csv | json | md | html>"
            fmt = args[1].lower()
            logs = history_svc.get_history(limit_hours=168)
            export_svc = container.get("export_service")
            
            try:
                filename = f"telemetry_export.{fmt}"
                out_path = export_svc.export_data(fmt, logs, filename)
            except Exception as ex:
                return f"Export Error: {ex}"
                
            return f"Telemetry history successfully exported to: {out_path.resolve()}"
            
        elif sub == "clean":
            deleted = history_svc.clean_old_records(days=0)  # clean all
            return f"Telemetry history clean up executed. Removed {deleted} logs."
            
        return f"Unknown telemetry command directive: '{sub}'"
        
    registry.register("telemetry", cmd_telemetry, "Queries and exports telemetry logs database: telemetry stats, telemetry export <csv|json|md|html>, telemetry clean")

def main() -> None:
    """Main execution bootstrap function."""
    # Resolve root directories (writable LOCALAPPDATA paths — safe for Program Files installs)
    from packages.core.constants.paths import CONFIG_DIR, PROFILES_DIR, INSTALL_DIR
    config_file = CONFIG_DIR / "settings.json"
    profiles_dir = PROFILES_DIR
    plugins_dir = INSTALL_DIR / "plugins"

    # Instantiate Singleton Service Container
    container = ServiceContainer()

    # Bootstrap all registered system services
    from packages.core.bootstrap import bootstrap_services
    bootstrap_services(
        container=container,
        profiles_dir=profiles_dir,
        plugins_dir=plugins_dir,
        config_file=config_file,
        default_settings=DEFAULT_SETTINGS
    )

    # Resolve necessary references
    cmd_registry = container.get("command_registry")
    hardware_service = container.get("hardware_service")
    plugin_loader = container.get("plugin_loader")

    # Pre-register default console scripts
    register_default_cli_commands(cmd_registry, container)

    # Discover and load external plugins
    plugin_loader.load_all_plugins(container)

    # Launch main application GUI window
    app = AegisApp(container)

    # Start telemetry polling loop
    hardware_service.start(app)

    app.mainloop()

if __name__ == "__main__":
    main()
