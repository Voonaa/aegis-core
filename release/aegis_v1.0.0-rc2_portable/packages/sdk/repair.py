"""Active repair and maintenance wrapper class for Aegis SDK."""

from packages.core.container import ServiceContainer
from packages.core.jobs import JobManager
from packages.core.services.repair_service import RepairService
from packages.core.services.maintenance_service import MaintenanceService

class RepairSDK:
    """Interface to trigger active Windows repair and maintenance jobs asynchronously."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Repair SDK.
        
        Args:
            container: DI Service container reference.
        """
        self._container = container

    def _get_job_mgr(self) -> JobManager:
        return self._container.get("job_manager")

    def _get_repair_svc(self) -> RepairService:
        return self._container.get("repair_service")

    def _get_maint_svc(self) -> MaintenanceService:
        return self._container.get("maintenance_service")

    def sfc(self) -> str:
        """Submits SFC Scannow file verification job to background threads.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "SFC Scannow Verification",
            self._get_repair_svc().run_sfc
        )

    def dism(self) -> str:
        """Submits DISM RestoreHealth image scan job.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "DISM RestoreHealth Image Scan",
            self._get_repair_svc().run_dism
        )

    def chkdsk(self) -> str:
        """Submits CHKDSK disk diagnostic verification job.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "CHKDSK File System Verify",
            self._get_repair_svc().run_chkdsk
        )

    def flush_dns(self) -> str:
        """Submits DNS Resolver cache flushing task.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "DNS Cache Flush",
            self._get_maint_svc().flush_dns
        )

    def clean_temp(self) -> str:
        """Submits Temporary Files cleanups task.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "Temporary Files Cleanup",
            self._get_maint_svc().clean_temp_files
        )

    def clean_components(self) -> str:
        """Submits DISM StartComponentCleanup task.
        
        Returns:
            Background Job ID token.
        """
        return self._get_job_mgr().submit(
            "DISM Component Store Cleanup",
            self._get_maint_svc().clean_component_store
        )
