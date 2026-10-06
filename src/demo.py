"""Демонстрация работы слоя доступа к данным (вариант №7)."""

from __future__ import annotations

from src import repository as repo
from src.models import Storage


def _section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    storage = Storage.empty()

    _section("Создание записей")
    agent = repo.create_agent(storage, "127.0.0.1", "linux", "curl/8.0")
    print("Agent:", agent)
    message = repo.create_message(
        storage, "arg1", agent.key, "demo message", "demo", "new")
    print("Message:", message)
    reply = repo.create_reply(storage, "output1", "done", "", message.key)
    print("Reply:", reply)

    _section("Чтение")
    print("get_agents:", repo.get_agents(storage))
    print("get_agent:", repo.get_agent(storage, agent.key))
    print("get_messages:", repo.get_messages(storage))
    print("get_message:", repo.get_message(storage, message.key))
    print("get_replies:", repo.get_replies(storage))
    print("get_reply:", repo.get_reply(storage, reply.key))

    _section("Редактирование")
    print("update_agent:", repo.update_agent(
        storage, agent.key, platform="windows"))
    print("update_message:", repo.update_message(
        storage, message.key, stage="processed"))
    print("update_reply:", repo.update_reply(
        storage, reply.key, output="output2"))

    _section("Соединение")
    print("join_agents_messages:", repo.join_agents_messages(storage))

    _section("Удаление")
    repo.delete_reply(storage, reply.key)
    repo.delete_message(storage, message.key)
    repo.delete_agent(storage, agent.key)
    print("После удаления:",
          repo.get_agents(storage),
          repo.get_messages(storage),
          repo.get_replies(storage))

    _section("Обработка ошибок")
    try:
        repo.get_agent(storage, 999)
    except repo.NotFoundError as exc:
        print("NotFoundError:", exc)
    try:
        repo.create_message(storage, "a", 999, "d", "t", "s")
    except repo.NotFoundError as exc:
        print("NotFoundError (FK):", exc)


if __name__ == "__main__":
    main()
