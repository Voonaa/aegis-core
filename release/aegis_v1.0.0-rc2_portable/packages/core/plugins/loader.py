"""Dynamic Plugin Loader engine loading dynamic plugin manifests and lifecycles."""

import json
import sys
import importlib.util
from pathlib import Path
from packages.core.container import ServiceContainer
from packages.core.services.privilege_service import PrivilegeService
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("PLUGIN")

class PluginLoader:
    """Manages discovery, permission checks, and dynamic lifecycle execution of plugins."""

    def __init__(self, plugins_dir: Path) -> None:
        """Initialize the Plugin Loader.
        
        Args:
            plugins_dir: Path to root plugins/ directory.
        """
        self.plugins_dir = plugins_dir
        self.loaded_plugins: dict[str, dict] = {}
        logger.info(f"Plugin Loader initialized at: {plugins_dir}")

    def load_all_plugins(self, container: ServiceContainer) -> list[str]:
        """Discovers, validates, and loads active plugin manifests from folder.
        
        Args:
            container: DI Service container reference.
            
        Returns:
            List of successfully loaded plugin names.
        """
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory missing at {self.plugins_dir}. Creating folders.")
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            return []

        priv_svc: PrivilegeService = container.get("privilege_service")
        is_host_admin = priv_svc.is_admin()
        success_names = []

        logger.info("Scanning for external plugin folders...")
        for sub in self.plugins_dir.iterdir():
            if sub.is_dir():
                manifest_file = sub / "manifest.json"
                if not manifest_file.exists():
                    continue

                try:
                    # 1. Parse manifest file
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    
                    p_name = manifest.get("name", sub.name)
                    p_version = manifest.get("version", "1.0.0")
                    p_permissions = manifest.get("permissions", [])
                    entry_file = manifest.get("entry_point", "main.py")

                    logger.info(f"Discovered plugin '{p_name}' v{p_version} inside {sub.name}")

                    # 2. Check Admin privileges requirements
                    if "admin" in p_permissions and not is_host_admin:
                        logger.warning(
                            f"Plugin '{p_name}' skipped: requires Administrator privileges, "
                            f"but current host process is running in user-mode."
                        )
                        continue

                    # 3. Resolve entry point path
                    entry_path = sub / entry_file
                    if not entry_path.exists():
                        logger.error(f"Plugin entry file missing: {entry_path}")
                        continue

                    # 4. Load module dynamically
                    spec = importlib.util.spec_from_file_location(
                        f"aegis_plugin_{sub.name}",
                        str(entry_path)
                    )
                    if spec is None or spec.loader is None:
                        logger.error(f"Failed to build spec loader details for: {entry_path}")
                        continue
                        
                    module = importlib.util.module_from_spec(spec)
                    
                    # Inject module into active sys modules map
                    sys.modules[f"aegis_plugin_{sub.name}"] = module
                    spec.loader.exec_module(module)

                    # 5. Trigger standard lifecycles
                    if hasattr(module, "initialize"):
                        module.initialize(container)
                        logger.debug(f"Plugin '{p_name}': triggered initialize() hook.")

                    if hasattr(module, "start"):
                        module.start()
                        logger.debug(f"Plugin '{p_name}': triggered start() hook.")

                    self.loaded_plugins[p_name] = {
                        "module": module,
                        "manifest": manifest,
                        "path": sub
                    }

                    success_names.append(p_name)
                    logger.info(f"Plugin '{p_name}' loaded successfully.")

                except Exception as ex:
                    logger.error(f"Failed to load plugin inside folder {sub.name}: {ex}", exc_info=True)

        return success_names

    def unload_all_plugins(self) -> None:
        """Triggers teardown dispose hooks for all loaded plugins."""
        for p_name, details in list(self.loaded_plugins.items()):
            module = details["module"]
            try:
                if hasattr(module, "dispose"):
                    module.dispose()
                    logger.debug(f"Plugin '{p_name}': triggered dispose() hook.")
                elif hasattr(module, "stop"): # Fallback lifecycle
                    module.stop()
                    logger.debug(f"Plugin '{p_name}': triggered stop() hook.")
            except Exception as ex:
                logger.error(f"Plugin '{p_name}' teardown failed: {ex}", exc_info=True)

        self.loaded_plugins.clear()
        logger.info("All plugins unloaded successfully.")
