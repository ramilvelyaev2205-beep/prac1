"""Клиент RPC (вариант 7)."""

from __future__ import annotations

import socket

from src.protocol import pack_request, read_response

OPCODES = {
    "create_agent": 1, "get_agents": 2, "get_agent": 3,
    "update_agent": 4, "delete_agent": 5,
    "create_message": 6, "get_messages": 7, "get_message": 8,
    "update_message": 9, "delete_message": 10,
    "create_reply": 11, "get_replies": 12, "get_reply": 13,
    "update_reply": 14, "delete_reply": 15,
    "join_agents_messages": 16,
}


class RpcClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 9090) -> None:
        self.host = host
        self.port = port

    def _call(self, method: str, body: str) -> str:
        with socket.create_connection((self.host, self.port)) as sock:
            sock.sendall(pack_request(OPCODES[method], body))
            _op, response = read_response(sock)
        return response

    def create_agent(self, ip, platform, user_agent):
        body = (f"<request><ip>{ip}</ip><platform>{platform}</platform>"
                f"<user_agent>{user_agent}</user_agent></request>")
        return self._call("create_agent", body)

    def get_agents(self):
        return self._call("get_agents", "<request/>")

    def get_agent(self, key):
        return self._call("get_agent", f"<request><key>{key}</key></request>")

    def update_agent(self, key, ip=None):
        tag = f"<ip>{ip}</ip>" if ip else ""
        body = f"<request><key>{key}</key>{tag}</request>"
        return self._call("update_agent", body)

    def delete_agent(self, key):
        body = f"<request><key>{key}</key></request>"
        return self._call("delete_agent", body)

    def create_message(self, arg, agent, description, tags, stage):
        body = (f"<request><arg>{arg}</arg><agent>{agent}</agent>"
                f"<description>{description}</description><tags>{tags}</tags>"
                f"<stage>{stage}</stage></request>")
        return self._call("create_message", body)

    def get_messages(self):
        return self._call("get_messages", "<request/>")

    def get_message(self, key):
        return self._call("get_message", f"<request><key>{key}</key></request>")

    def update_message(self, key, arg=None):
        tag = f"<arg>{arg}</arg>" if arg else ""
        body = f"<request><key>{key}</key>{tag}</request>"
        return self._call("update_message", body)

    def delete_message(self, key):
        body = f"<request><key>{key}</key></request>"
        return self._call("delete_message", body)

    def create_reply(self, output, stage, exception, message):
        body = (f"<request><output>{output}</output><stage>{stage}</stage>"
                f"<exception>{exception}</exception>"
                f"<message>{message}</message></request>")
        return self._call("create_reply", body)

    def get_replies(self):
        return self._call("get_replies", "<request/>")

    def get_reply(self, key):
        return self._call("get_reply", f"<request><key>{key}</key></request>")

    def update_reply(self, key, output=None):
        tag = f"<output>{output}</output>" if output else ""
        body = f"<request><key>{key}</key>{tag}</request>"
        return self._call("update_reply", body)

    def delete_reply(self, key):
        body = f"<request><key>{key}</key></request>"
        return self._call("delete_reply", body)

    def join_agents_messages(self):
        return self._call("join_agents_messages", "<request/>")
