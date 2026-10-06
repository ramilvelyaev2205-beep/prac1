"""Модульные тесты слоя доступа к данным."""

import pytest

from src import repository as repo
from src.models import Storage


@pytest.fixture()
def storage() -> Storage:
    return Storage.empty()


def test_create_and_get_agent(storage: Storage) -> None:
    agent = repo.create_agent(storage, "127.0.0.1", "linux", "curl/8")
    assert repo.get_agent(storage, agent.key) == agent


def test_update_agent(storage: Storage) -> None:
    agent = repo.create_agent(storage, "127.0.0.1", "linux", "curl/8")
    updated = repo.update_agent(storage, agent.key, platform="windows")
    assert updated.platform == "windows"


def test_delete_agent(storage: Storage) -> None:
    agent = repo.create_agent(storage, "127.0.0.1", "linux", "curl/8")
    repo.delete_agent(storage, agent.key)
    assert repo.get_agents(storage) == []


def test_create_message_requires_agent(storage: Storage) -> None:
    with pytest.raises(repo.NotFoundError):
        repo.create_message(storage, "arg", 999, "d", "t", "s")


def test_create_reply_requires_message(storage: Storage) -> None:
    with pytest.raises(repo.NotFoundError):
        repo.create_reply(storage, "out", "stage", "", 999)


def test_not_found(storage: Storage) -> None:
    with pytest.raises(repo.NotFoundError):
        repo.get_agent(storage, 999)


def test_join_filters_old_messages(storage: Storage) -> None:
    agent = repo.create_agent(storage, "1.1.1.1", "linux", "ua")
    repo.create_message(storage, "arg", agent.key, "d", "t", "s")
    assert repo.join_agents_messages(storage) == [("1.1.1.1", "linux")]


def test_update_reply(storage: Storage) -> None:
    agent = repo.create_agent(storage, "1.1.1.1", "linux", "ua")
    message = repo.create_message(storage, "a", agent.key, "d", "t", "s")
    reply = repo.create_reply(storage, "o", "s", "", message.key)
    updated = repo.update_reply(storage, reply.key, output="new")
    assert updated.output == "new"


def test_delete_reply(storage: Storage) -> None:
    agent = repo.create_agent(storage, "1.1.1.1", "linux", "ua")
    message = repo.create_message(storage, "a", agent.key, "d", "t", "s")
    reply = repo.create_reply(storage, "o", "s", "", message.key)
    repo.delete_reply(storage, reply.key)
    assert repo.get_replies(storage) == []
