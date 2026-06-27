"""Unit tests for the JobManager background task orchestration system."""

import time
import pytest
from packages.core.container import ServiceContainer
from packages.core.event_bus import EventBus
from packages.core.jobs import JobManager, JobStatus


@pytest.fixture(autouse=True)
def reset_singleton() -> None:
    """Reset ServiceContainer singleton between tests."""
    ServiceContainer._instance = None
    yield
    ServiceContainer._instance = None


@pytest.fixture
def job_manager() -> JobManager:
    """Returns a JobManager with a minimal container setup."""
    container = ServiceContainer()
    container.register("event_bus", EventBus())
    return JobManager(container=container)


def _noop_task(progress_cb: object) -> None:
    """A task that completes immediately without doing anything."""
    pass  # pragma: no cover


def _failing_task(progress_cb: object) -> None:
    """A task that always raises an exception."""
    raise ValueError("Deliberate test failure")  # pragma: no cover


def test_submit_returns_job_id(job_manager: JobManager) -> None:
    """submit() must return a non-empty string job ID."""
    job_id = job_manager.submit("test-job", _noop_task)

    assert isinstance(job_id, str)
    assert len(job_id) > 0


def test_job_is_registered_after_submit(job_manager: JobManager) -> None:
    """After submit(), the job must appear in get_job() before it completes."""
    job_id = job_manager.submit("test-job", _noop_task)

    # The job should exist immediately after submit
    job = job_manager.get_job(job_id)
    assert job is not None
    assert job.id == job_id
    assert job.name == "test-job"


def test_job_completed_on_success(job_manager: JobManager) -> None:
    """A successfully completing task must reach COMPLETED status."""
    job_id = job_manager.submit("success-job", _noop_task)

    # Wait for the daemon thread to finish
    time.sleep(0.3)

    job = job_manager.get_job(job_id)
    assert job is not None
    assert job.status == JobStatus.COMPLETED


def test_job_failed_on_exception(job_manager: JobManager) -> None:
    """A task that raises must reach FAILED status with a non-empty error message."""
    job_id = job_manager.submit("failing-job", _failing_task)

    time.sleep(0.3)

    job = job_manager.get_job(job_id)
    assert job is not None
    assert job.status == JobStatus.FAILED
    assert len(job.error_message) > 0


def test_get_job_unknown_returns_none(job_manager: JobManager) -> None:
    """`get_job()` on an unknown ID must return None without raising."""
    result = job_manager.get_job("nonexistent-id-xyz")
    assert result is None


def test_get_active_jobs_returns_list(job_manager: JobManager) -> None:
    """`get_active_jobs()` must return a list (possibly empty)."""
    result = job_manager.get_active_jobs()
    assert isinstance(result, list)


def test_multiple_jobs_tracked_independently(job_manager: JobManager) -> None:
    """Multiple submitted jobs must each have their own ID and record."""
    id_a = job_manager.submit("job-a", _noop_task)
    id_b = job_manager.submit("job-b", _noop_task)

    assert id_a != id_b

    time.sleep(0.3)

    job_a = job_manager.get_job(id_a)
    job_b = job_manager.get_job(id_b)
    assert job_a is not None
    assert job_b is not None
    assert job_a.name == "job-a"
    assert job_b.name == "job-b"
