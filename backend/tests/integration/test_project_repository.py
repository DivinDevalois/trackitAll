import pytest

from app.repositories.project_repository import ProjectRepository


@pytest.fixture()
def repo(db_session):
    return ProjectRepository(db_session)


def test_create_persists_project(repo):
    project = repo.create(name="TrackItAll")

    assert project.id is not None
    assert project.name == "TrackItAll"
    assert project.description is None


def test_get_returns_existing_project(repo):
    created = repo.create(name="Find me")

    found = repo.get(created.id)

    assert found is not None
    assert found.id == created.id


def test_get_returns_none_for_unknown_id(repo):
    assert repo.get(999) is None


def test_list_returns_all_projects_ordered_by_id(repo):
    first = repo.create(name="First")
    second = repo.create(name="Second")

    projects = repo.list()

    assert [p.id for p in projects] == [first.id, second.id]


def test_update_changes_fields(repo):
    created = repo.create(name="Old name", description="Old description")

    updated = repo.update(created.id, name="New name")

    assert updated is not None
    assert updated.name == "New name"
    assert updated.description == "Old description"


def test_update_returns_none_for_unknown_id(repo):
    assert repo.update(999, name="Whatever") is None


def test_delete_removes_project(repo):
    created = repo.create(name="To delete")

    deleted = repo.delete(created.id)

    assert deleted is True
    assert repo.get(created.id) is None


def test_delete_returns_false_for_unknown_id(repo):
    assert repo.delete(999) is False
