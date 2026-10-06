"""Слой доступа к данным (вариант №7)."""

from __future__ import annotations

import time

from src.models import Agent, Message, Reply, Storage

MINUTE = 60
WINDOW_MINUTES = 7


class NotFoundError(LookupError):
    """Запись не найдена."""


def _now() -> int:
    return int(time.time())


def _find(records, key: int):
    for record in records:
        if record.key == key:
            return record
    raise NotFoundError(f"Запись с key={key} не найдена")


def _replace(record, **changes):
    return record._replace(**{
        k: v if v is not None else getattr(record, k)
        for k, v in changes.items()
    })


def create_agent(storage: Storage, ip: str, platform: str,
                 user_agent: str) -> Agent:
    agent = Agent(
        key=storage.next_id("agents"),
        time=_now(),
        ip=ip,
        platform=platform,
        user_agent=user_agent,
    )
    storage.agents.append(agent)
    return agent


def get_agents(storage: Storage) -> list:
    return list(storage.agents)


def get_agent(storage: Storage, key: int) -> Agent:
    return _find(storage.agents, key)


def update_agent(storage: Storage, key: int, *, ip=None, platform=None,
                 user_agent=None) -> Agent:
    current = get_agent(storage, key)
    updated = _replace(
        current, ip=ip, platform=platform, user_agent=user_agent,
    )
    storage.agents[storage.agents.index(current)] = updated
    return updated


def delete_agent(storage: Storage, key: int) -> None:
    storage.agents.remove(get_agent(storage, key))


def create_message(storage: Storage, arg: str, agent: int, description: str,
                   tags: str, stage: str) -> Message:
    get_agent(storage, agent)
    message = Message(
        key=storage.next_id("messages"),
        time=_now(),
        arg=arg,
        agent=agent,
        description=description,
        tags=tags,
        stage=stage,
    )
    storage.messages.append(message)
    return message


def get_messages(storage: Storage) -> list:
    return list(storage.messages)


def get_message(storage: Storage, key: int) -> Message:
    return _find(storage.messages, key)


def update_message(storage: Storage, key: int, *, arg=None, description=None,
                   tags=None, stage=None) -> Message:
    current = get_message(storage, key)
    updated = _replace(
        current, arg=arg, description=description, tags=tags, stage=stage,
    )
    storage.messages[storage.messages.index(current)] = updated
    return updated


def delete_message(storage: Storage, key: int) -> None:
    storage.messages.remove(get_message(storage, key))


def create_reply(storage: Storage, output: str, stage: str, exception: str,
                 message: int) -> Reply:
    get_message(storage, message)
    reply = Reply(
        key=storage.next_id("replies"),
        time=_now(),
        output=output,
        stage=stage,
        exception=exception,
        message=message,
    )
    storage.replies.append(reply)
    return reply


def get_replies(storage: Storage) -> list:
    return list(storage.replies)


def get_reply(storage: Storage, key: int) -> Reply:
    return _find(storage.replies, key)


def update_reply(storage: Storage, key: int, *, output=None, stage=None,
                 exception=None) -> Reply:
    current = get_reply(storage, key)
    updated = _replace(
        current, output=output, stage=stage, exception=exception,
    )
    storage.replies[storage.replies.index(current)] = updated
    return updated


def delete_reply(storage: Storage, key: int) -> None:
    storage.replies.remove(get_reply(storage, key))


def join_agents_messages(storage: Storage,
                         window_minutes: int = WINDOW_MINUTES) -> list:
    threshold = _now() - window_minutes * MINUTE
    result = []
    for message in storage.messages:
        if message.time < threshold:
            continue
        agent = _find(storage.agents, message.agent)
        result.append((agent.ip, agent.platform))
    return result
