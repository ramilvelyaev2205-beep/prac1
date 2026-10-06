"""Модели данных (вариант №7)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple


class Agent(NamedTuple):
    """Запись таблицы Agent."""

    key: int
    time: int
    ip: str
    platform: str
    user_agent: str


class Message(NamedTuple):
    """Запись таблицы Message."""

    key: int
    time: int
    arg: str
    agent: int
    description: str
    tags: str
    stage: str


class Reply(NamedTuple):
    """Запись таблицы Reply."""

    key: int
    time: int
    output: str
    stage: str
    exception: str
    message: int


@dataclass
class Storage:
    """In-memory хранилище трёх таблиц."""

    agents: list
    messages: list
    replies: list
    autoincrement: dict

    @classmethod
    def empty(cls) -> "Storage":
        return cls([], [], [], {"agents": 1, "messages": 1, "replies": 1})

    def next_id(self, table: str) -> int:
        value = self.autoincrement[table]
        self.autoincrement[table] = value + 1
        return value
