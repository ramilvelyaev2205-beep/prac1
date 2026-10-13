"""Демонстрация работы слоя доступа к данным (вариант №7)."""

from __future__ import annotations

from src import repository as repo
from src.models import Storage


def _section(title: str) -> None:
    print(f"\n=== {title} ===")


def _demo_create(storage) -> None:
    _section("Создание записей")
    agent = repo.create_agent(storage, "127.0.0.1", "linux", "curl/8.0")
    print("Agent:", agent)
    message = repo.create_message(
        storage, "arg1", agent.key, "demo message", "demo", "new")
    print("Message:", message)
    reply = repo.create_reply(storage, "output1", "done", "", message.key)
    print("Reply:", reply)


def _demo_read(storage) -> None:
    _section("Чтение")
    print("get_agents:", repo.get_agents(storage))
    print("get_messages:", repo.get_messages(storage))
    print("get_replies:", repo.get_replies(storage))


def _demo_update(storage) -> None:
    _section("Редактирование")
    print("update_agent:", repo.update_agent(storage, 1, platform="windows"))
    print("update_message:", repo.update_message(storage, 1, stage="processed"))
    print("update_reply:", repo.update_reply(storage, 1, output="output2"))


def _demo_join(storage) -> None:
    _section("Соединение")
    print("join_agents_messages:", repo.join_agents_messages(storage))


def _demo_delete(storage) -> None:
    _section("Удаление")
    repo.delete_reply(storage, 1)
    repo.delete_message(storage, 1)
    repo.delete_agent(storage, 1)
    print("После удаления:",
          repo.get_agents(storage),
          repo.get_messages(storage),
          repo.get_replies(storage))


def _demo_errors(storage) -> None:
    _section("Обработка ошибок")
    try:
        repo.get_agent(storage, 999)
    except repo.NotFoundError as exc:
        print("NotFoundError:", exc)
    try:
        repo.create_message(storage, "a", 999, "d", "t", "s")
    except repo.NotFoundError as exc:
        print("NotFoundError (FK):", exc)


def main() -> None:
    storage = Storage.empty()
    _demo_create(storage)
    _demo_read(storage)
    _demo_update(storage)
    _demo_join(storage)
    _demo_delete(storage)
    _demo_errors(storage)


if __name__ == "__main__":
    main()