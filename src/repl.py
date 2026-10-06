"""REPL для модели слоя доступа к данным (вариант №7)."""

from __future__ import annotations

from src import repository as repo
from src.models import Storage

HELP = """Доступные команды:
  help
  create_agent <ip> <platform> <user_agent>
  get_agents
  get_agent <key>
  update_agent <key> <ip> <platform> <user_agent>
  delete_agent <key>
  create_message <arg> <agent> <description> <tags> <stage>
  get_messages
  get_message <key>
  update_message <key> <arg> <description> <tags> <stage>
  delete_message <key>
  create_reply <output> <stage> <exception> <message>
  get_replies
  get_reply <key>
  update_reply <key> <output> <stage> <exception>
  delete_reply <key>
  join
  exit
"""


def _print(items) -> None:
    for item in items:
        print(item)


def _dispatch(storage, command, args) -> None:
    handlers = {
        "create_agent": lambda: print(repo.create_agent(
            storage, args[0], args[1], args[2])),
        "get_agents": lambda: _print(repo.get_agents(storage)),
        "get_agent": lambda: print(repo.get_agent(storage, int(args[0]))),
        "update_agent": lambda: print(repo.update_agent(
            storage, int(args[0]), ip=args[1],
            platform=args[2], user_agent=args[3])),
        "delete_agent": lambda: repo.delete_agent(storage, int(args[0])),
        "create_message": lambda: print(repo.create_message(
            storage, args[0], int(args[1]), args[2], args[3], args[4])),
        "get_messages": lambda: _print(repo.get_messages(storage)),
        "get_message": lambda: print(repo.get_message(storage, int(args[0]))),
        "update_message": lambda: print(repo.update_message(
            storage, int(args[0]), arg=args[1],
            description=args[2], tags=args[3], stage=args[4])),
        "delete_message": lambda: repo.delete_message(storage, int(args[0])),
        "create_reply": lambda: print(repo.create_reply(
            storage, args[0], args[1], args[2], int(args[3]))),
        "get_replies": lambda: _print(repo.get_replies(storage)),
        "get_reply": lambda: print(repo.get_reply(storage, int(args[0]))),
        "update_reply": lambda: print(repo.update_reply(
            storage, int(args[0]), output=args[1],
            stage=args[2], exception=args[3])),
        "delete_reply": lambda: repo.delete_reply(storage, int(args[0])),
        "join": lambda: _print(repo.join_agents_messages(storage)),
    }
    handler = handlers.get(command)
    if handler is None:
        print(f"Неизвестная команда: {command}")
        return
    handler()


def run(storage=None) -> None:
    storage = storage or Storage.empty()
    print(HELP)
    while True:
        try:
            raw = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not raw:
            continue
        if raw in {"exit", "quit"}:
            return
        if raw == "help":
            print(HELP)
            continue
        parts = raw.split()
        try:
            _dispatch(storage, parts[0], parts[1:])
        except (ValueError, TypeError, repo.NotFoundError) as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run()
