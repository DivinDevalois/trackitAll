import pytest

from app.models.task import TaskPriority, TaskStatus
from app.repositories.task_repository import TaskRepository


@pytest.fixture()
def repo(db_session):
    return TaskRepository(db_session)


def test_create_sets_defaults_and_persists(repo):
    task = repo.create(title="Write the backlog")

    assert task.id is not None
    assert task.title == "Write the backlog"
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM


def test_create_accepts_explicit_fields(repo):
    task = repo.create(
        title="Ship TIA-7",
        description="Task repository CRUD",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
    )

    assert task.description == "Task repository CRUD"
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.HIGH


def test_get_returns_existing_task(repo):
    created = repo.create(title="Find me")

    found = repo.get(created.id)

    assert found is not None
    assert found.id == created.id


def test_get_returns_none_for_unknown_id(repo):
    assert repo.get(999) is None


def test_list_returns_all_tasks_ordered_by_id(repo):
    first = repo.create(title="First")
    second = repo.create(title="Second")

    tasks = repo.list()

    assert [t.id for t in tasks] == [first.id, second.id]


def test_update_status_changes_and_persists(repo):
    created = repo.create(title="To be updated")

    updated = repo.update_status(created.id, TaskStatus.DONE)

    assert updated is not None
    assert updated.status == TaskStatus.DONE
    assert repo.get(created.id).status == TaskStatus.DONE


def test_update_status_returns_none_for_unknown_id(repo):
    assert repo.update_status(999, TaskStatus.DONE) is None
