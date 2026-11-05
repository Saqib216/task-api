from app.models import TaskStatus

ALLOWED_TRANSITIONS: dict[TaskStatus, list[TaskStatus]] = {
    TaskStatus.NEW: [TaskStatus.ACTIVE],
    TaskStatus.ACTIVE: [TaskStatus.COMPLETED, TaskStatus.FAILED],
    TaskStatus.COMPLETED: [],
    TaskStatus.FAILED: [],
}
