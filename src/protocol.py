"""Кодеки RPC-протокола (TCP, вариант 7).

Запрос: версия(1) + код(1) + размер(5) + XML.
Ответ:  размер(5) + код(2) + XML.
Порядок байт: от младшего к старшему.
"""

from __future__ import annotations

import struct

PROTOCOL_VERSION = 1
HEADER_REQ = struct.Struct("<BB5s")
HEADER_RESP = struct.Struct("<5sH")


def pack_request(opcode: int, body: str) -> bytes:
    payload = body.encode("utf-8")
    size = len(payload).to_bytes(5, "little")
    return HEADER_REQ.pack(PROTOCOL_VERSION, opcode, size) + payload


def pack_response(opcode: int, body: str) -> bytes:
    payload = body.encode("utf-8")
    size = len(payload).to_bytes(5, "little")
    return HEADER_RESP.pack(size, opcode) + payload


def read_request(sock) -> tuple:
    header = _read_exact(sock, HEADER_REQ.size)
    _v, op, sz = HEADER_REQ.unpack(header)
    return op, _read_exact(sock, int.from_bytes(sz, "little")).decode("utf-8")


def read_response(sock) -> tuple:
    header = _read_exact(sock, HEADER_RESP.size)
    sz, op = HEADER_RESP.unpack(header)
    return op, _read_exact(sock, int.from_bytes(sz, "little")).decode("utf-8")


def _read_exact(sock, size: int) -> bytes:
    chunks = []
    while size > 0:
        chunk = sock.recv(size)
        if not chunk:
            raise ConnectionError("Соединение закрыто")
        chunks.append(chunk)
        size -= len(chunk)
    return b"".join(chunks)
