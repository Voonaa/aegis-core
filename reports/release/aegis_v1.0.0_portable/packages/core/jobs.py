"""Background Job Manager orchestrating asynchronous threads for Aegis Toolkit."""

import uuid
import threading
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus
import packages.core.constants.events as events
from packages.core.logger import get_subsystem_logger

logger = get_subsystem_logger("SYSTEM")

class JobStatus(Enum):
    """Execution status definitions for background jobs."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Job:
    """Encapsulates a thread job record details."""
    id: str
    name: str
    status: JobStatus
    progress: float
    error_message: str = ""


class JobManager:
    """Orchestrates threading workers preventing GUI UI locks on long running tasks."""

    def __init__(self, container: ServiceContainer) -> None:
        """Initialize the Job Manager.
        
        Args:
            container: DI Service container reference.
        """
        self.container = container
        self.event_bus: EventBus = container.get("event_bus")
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        logger.info("Job Manager initialized.")

    def submit(self, name: str, task_fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
        """Submit a task to run in a background worker thread.
        
        Args:
            name: Human-readable name of the task.
            task_fn: Function to execute. Must accept progress_callback (Callable[[float]]) as first parameter.
            args: Positional arguments for task.
            kwargs: Keyword arguments for task.
            
        Returns:
            Unique job_id token.
        """
        job_id = str(uuid.uuid4())[:8]
        job = Job(id=job_id, name=name, status=JobStatus.PENDING, progress=0.0)

        with self._lock:
            self._jobs[job_id] = job

        logger.info(f"Background job '{name}' submitted. Assigned ID: {job_id}")
        self.event_bus.publish(events.JOB_STATUS_CHANGED, job_id, JobStatus.PENDING)

        # Spawn daemon thread to prevent process hanging on app exits
        t = threading.Thread(
            target=self._run_job,
            args=(job_id, task_fn, args, kwargs),
            daemon=True,
            name=f"AegisJob-{job_id}"
        )
        t.start()
        
        return job_id

    def _run_job(self, job_id: str, task_fn: Callable[..., Any], args: tuple, kwargs: dict) -> None:
        """Background thread worker execution wrapper."""
        with self._lock:
            job = self._jobs[job_id]
            job.status = JobStatus.RUNNING
        
        logger.info(f"Running background task job '{job.name}' ({job_id})")
        self.event_bus.publish(events.JOB_STATUS_CHANGED, job_id, JobStatus.RUNNING)

        def progress_callback(progress_fraction: float) -> None:
            """Callable progress update channel inside task loops."""
            self._update_progress(job_id, progress_fraction)

        try:
            # Trigger task function
            task_fn(progress_callback, *args, **kwargs)
            
            with self._lock:
                job.status = JobStatus.COMPLETED
                job.progress = 1.0
            
            logger.info(f"Background task job completed: '{job.name}' ({job_id})")
            self.event_bus.publish(events.JOB_STATUS_CHANGED, job_id, JobStatus.COMPLETED)
            self.event_bus.publish(events.NOTIFICATION_TRIGGERED, f"Task '{job.name}' Completed!", "success")

        except Exception as ex:
            error_str = str(ex)
            with self._lock:
                job.status = JobStatus.FAILED
                job.error_message = error_str
            
            logger.error(f"Background task job failed: '{job.name}' ({job_id}) - {error_str}", exc_info=True)
            self.event_bus.publish(events.JOB_STATUS_CHANGED, job_id, JobStatus.FAILED)
            self.event_bus.publish(events.NOTIFICATION_TRIGGERED, f"Task '{job.name}' Failed: {error_str}", "danger")

    def _update_progress(self, job_id: str, progress_fraction: float) -> None:
        """Update job progress record and emit updates to the EventBus."""
        progress_clamped = max(0.0, min(1.0, progress_fraction))
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id].progress = progress_clamped

        self.event_bus.publish(events.JOB_PROGRESS_UPDATED, job_id, progress_clamped)

    def get_job(self, job_id: str) -> Job | None:
        """Gets detailed stats for specific job."""
        with self._lock:
            return self._jobs.get(job_id)

    def get_active_jobs(self) -> list[Job]:
        """Gets all cached jobs."""
        with self._lock:
            return list(self._jobs.values())
