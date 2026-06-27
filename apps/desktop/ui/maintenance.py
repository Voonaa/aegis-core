"""Maintenance frame displaying active repair operations for Aegis Core Platform."""

import customtkinter as ctk
import packages.core.constants.events as events
from typing import Callable
from apps.desktop.ui.base_page import BasePage
from apps.desktop.ui.theme import ThemeManager
from packages.core.container import ServiceContainer
from packages.core.jobs import JobManager, JobStatus
from packages.core.services.repair_service import RepairService
from packages.core.services.maintenance_service import MaintenanceService
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class MaintenancePage(BasePage):
    """Maintenance and Repair viewport page mapping DISM, SFC, CHKDSK, and flushing triggers."""

    def __init__(self, master: any, theme: ThemeManager, log_callback: Callable[[str, str], None] | None = None) -> None:
        """Initialize the Maintenance Page.
        
        Args:
            master: Viewport router parent frame.
            theme: Active style theme manager.
            log_callback: Console log piping callback.
        """
        super().__init__(master=master)
        self.theme = theme
        self.log_callback = log_callback
        self.active_job_id: str | None = None

        # Fetch services from Singleton Container
        container = ServiceContainer()
        self.event_bus = container.get("event_bus")
        self.job_mgr: JobManager = container.get("job_manager")
        self.rep_svc: RepairService = container.get("repair_service")
        self.maint_svc: MaintenanceService = container.get("maintenance_service")

        # Grid structures configuration
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Action Grid
        self.grid_rowconfigure(2, weight=0)  # Active Progress display bar
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_action_grid()
        self._build_progress_bar()

    def _build_header(self) -> None:
        """Render page headers."""
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=spacing_xl, pady=(spacing_xl, spacing_md), sticky="ew")

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="SYSTEM MAINTENANCE & REPAIRS",
            font=self.theme.get_font("font_size_lg", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        title_lbl.pack(side="left", anchor="w")

    def _build_action_grid(self) -> None:
        """Draw action buttons categorized by systems."""
        spacing_xs = self.theme.get_spacing("spacing_xs")
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_lg = self.theme.get_spacing("spacing_lg")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        grid_frame = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_lg"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        grid_frame.grid(row=1, column=0, padx=spacing_xl, pady=(0, spacing_md), sticky="nsew")
        grid_frame.grid_columnconfigure((0, 1), weight=1)

        # Category 1: Windows OS Integrity Repairs
        os_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        os_frame.grid(row=0, column=0, padx=spacing_lg, pady=spacing_lg, sticky="nsew")
        
        os_lbl = ctk.CTkLabel(
            os_frame,
            text="OS Integrity Checks",
            font=self.theme.get_font("font_size_md", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        os_lbl.pack(anchor="w", pady=(0, spacing_md))

        sfc_btn = ctk.CTkButton(
            os_frame,
            text="Run System File Check (SFC)",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("SFC Scannow Verification", self.rep_svc.run_sfc)
        )
        sfc_btn.pack(fill="x", pady=spacing_xs)

        dism_btn = ctk.CTkButton(
            os_frame,
            text="Run Image Restore (DISM)",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("DISM RestoreHealth Image Scan", self.rep_svc.run_dism)
        )
        dism_btn.pack(fill="x", pady=spacing_xs)

        # Category 2: Disk & Storage Optimization
        disk_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        disk_frame.grid(row=0, column=1, padx=spacing_lg, pady=spacing_lg, sticky="nsew")

        disk_lbl = ctk.CTkLabel(
            disk_frame,
            text="Storage Operations",
            font=self.theme.get_font("font_size_md", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        disk_lbl.pack(anchor="w", pady=(0, spacing_md))

        chkdsk_btn = ctk.CTkButton(
            disk_frame,
            text="Check File System (CHKDSK)",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("CHKDSK File System Verify", self.rep_svc.run_chkdsk)
        )
        chkdsk_btn.pack(fill="x", pady=spacing_xs)

        trim_btn = ctk.CTkButton(
            disk_frame,
            text="Clean Component Store (DISM)",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("DISM Component Store Cleanup", self.maint_svc.clean_component_store)
        )
        trim_btn.pack(fill="x", pady=spacing_xs)

        # Category 3: Network Automation Tweak panel
        net_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        net_frame.grid(row=1, column=0, columnspan=2, padx=spacing_lg, pady=(0, spacing_lg), sticky="nsew")

        net_lbl = ctk.CTkLabel(
            net_frame,
            text="Network & Temporary Cache cleanups",
            font=self.theme.get_font("font_size_md", "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        net_lbl.pack(anchor="w", pady=(0, spacing_md))

        btn_row = ctk.CTkFrame(net_frame, fg_color="transparent")
        btn_row.pack(fill="x")

        dns_btn = ctk.CTkButton(
            btn_row,
            text="Flush DNS Resolvers Cache",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("DNS Cache Flush", self.maint_svc.flush_dns)
        )
        dns_btn.pack(side="left", fill="x", expand=True, padx=(0, spacing_sm))

        temp_btn = ctk.CTkButton(
            btn_row,
            text="Clean Temporary Cache Files",
            height=36,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("accent_primary"),
            hover_color=self.theme.get_color("border"),
            command=lambda: self._trigger_task("Temporary Files Cleanup", self.maint_svc.clean_temp_files)
        )
        temp_btn.pack(side="left", fill="x", expand=True, padx=(spacing_sm, 0))

    def _build_progress_bar(self) -> None:
        """Render the bottom progress panel."""
        spacing_sm = self.theme.get_spacing("spacing_sm")
        spacing_md = self.theme.get_spacing("spacing_md")
        spacing_xl = self.theme.get_spacing("spacing_xl")

        self.progress_frame = ctk.CTkFrame(
            self,
            corner_radius=self.theme.get_radius("corner_radius_md"),
            fg_color=self.theme.get_color("bg_card"),
            border_width=1,
            border_color=self.theme.get_color("border")
        )
        self.progress_frame.grid(row=2, column=0, padx=spacing_xl, pady=(0, spacing_xl), sticky="ew")

        self.progress_lbl = ctk.CTkLabel(
            self.progress_frame,
            text="Task Idle: No active repairs running...",
            font=self.theme.get_font("font_size_sm"),
            text_color=self.theme.get_color("text_muted")
        )
        self.progress_lbl.pack(padx=spacing_md, pady=(spacing_sm, spacing_xs := self.theme.get_spacing("spacing_xs")), anchor="w")

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            progress_color=self.theme.get_color("accent_primary")
        )
        self.progress_bar.pack(padx=spacing_md, pady=(spacing_xs, spacing_md), fill="x")
        self.progress_bar.set(0.0)

    def _trigger_task(self, name: str, task_fn: any) -> None:
        """Submits a target routine to the background JobManager thread loop."""
        if self.active_job_id:
            job = self.job_mgr.get_job(self.active_job_id)
            if job and job.status == JobStatus.RUNNING:
                if self.log_callback:
                    self.log_callback("An active diagnostic repair job is already running.", "WARNING")
                return

        try:
            # Submit asynchronous task
            job_id = self.job_mgr.submit(name, task_fn)
            self.active_job_id = job_id
            
            if self.log_callback:
                self.log_callback(f"Background job '{name}' triggered. ID: {job_id}", "INFO")

        except Exception as ex:
            if self.log_callback:
                self.log_callback(f"Failed to schedule job '{name}': {ex}", "ERROR")

    def on_resume(self) -> None:
        """Subscribes view listeners on displays."""
        logger.info("MaintenancePage: Resuming UI and binding EventBus job listeners.")
        self.event_bus.subscribe(events.JOB_PROGRESS_UPDATED, self._on_job_progress)
        self.event_bus.subscribe(events.JOB_STATUS_CHANGED, self._on_job_status_changed)

    def on_pause(self) -> None:
        """Unsubscribes listeners on hides."""
        logger.info("MaintenancePage: Pausing view, freeing event subscriptions.")
        self.event_bus.unsubscribe(events.JOB_PROGRESS_UPDATED, self._on_job_progress)
        self.event_bus.unsubscribe(events.JOB_STATUS_CHANGED, self._on_job_status_changed)

    def _on_job_progress(self, job_id: str, progress: float) -> None:
        """Reacts to background progress updates."""
        if job_id != self.active_job_id:
            return

        job = self.job_mgr.get_job(job_id)
        if job:
            pct = int(progress * 100)
            self.progress_lbl.configure(
                text=f"Active Job: '{job.name}' ({job_id}) - {pct}% complete",
                text_color=self.theme.get_color("text_primary")
            )
            self.progress_bar.set(progress)

            if self.log_callback and pct % 25 == 0:
                self.log_callback(f"Job '{job.name}' execution: {pct}% complete.", "INFO")

    def _on_job_status_changed(self, job_id: str, status: JobStatus) -> None:
        """Reacts to background status transition hooks."""
        if job_id != self.active_job_id:
            return

        job = self.job_mgr.get_job(job_id)
        if job:
            if status == JobStatus.COMPLETED:
                self.progress_lbl.configure(
                    text=f"Task Completed: '{job.name}' successfully finished!",
                    text_color=self.theme.get_color("status_success")
                )
                self.progress_bar.set(1.0)
                if self.log_callback:
                    self.log_callback(f"Success: Background job '{job.name}' completed.", "INFO")
                self.active_job_id = None
                
            elif status == JobStatus.FAILED:
                self.progress_lbl.configure(
                    text=f"Task Failed: '{job.name}' error: {job.error_message}",
                    text_color=self.theme.get_color("status_danger")
                )
                self.progress_bar.set(0.0)
                if self.log_callback:
                    self.log_callback(f"Failed: Job '{job.name}' error details: {job.error_message}", "ERROR")
                self.active_job_id = None
                
            elif status == JobStatus.RUNNING:
                self.progress_lbl.configure(
                    text=f"Task Starting: '{job.name}' executing...",
                    text_color=self.theme.get_color("text_primary")
                )
                self.progress_bar.set(0.0)
