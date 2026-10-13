from __future__ import annotations

import socket
from xml.sax.saxutils import escape

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


def _clean(text) -> str:
    """Удалить control-символы, недопустимые в XML."""
    s = str(text)
    return "".join(c for c in s if c in "\t\n\r" or c.isprintable())


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
        body = (f"<request><ip>{escape(_clean(ip))}</ip>"
                f"<platform>{escape(_clean(platform))}</platform>"
                f"<user_agent>{escape(_clean(user_agent))}</user_agent>"
                f"</request>")
        return self._call("create_agent", body)

    def get_agents(self):
        return self._call("get_agents", "<request/>")

    def get_agent(self, key):
        return self._call("get_agent",
                          f"<request><key>{int(key)}</key></request>")

    def update_agent(self, key, ip=None):
        tag = f"<ip>{escape(_clean(ip))}</ip>" if ip else ""
        return self._call("update_agent",
                          f"<request><key>{int(key)}</key>{tag}</request>")

    def delete_agent(self, key):
        return self._call("delete_agent",
                          f"<request><key>{int(key)}</key></request>")

    def create_message(self, arg, agent, description, tags, stage):
        body = (f"<request><arg>{escape(_clean(arg))}</arg>"
                f"<agent>{int(agent)}</agent>"
                f"<description>{escape(_clean(description))}</description>"
                f"<tags>{escape(_clean(tags))}</tags>"
                f"<stage>{escape(_clean(stage))}</stage></request>")
        return self._call("create_message", body)

    def get_messages(self):
        return self._call("get_messages", "<request/>")

    def get_message(self, key):
        return self._call("get_message",
                          f"<request><key>{int(key)}</key></request>")

    def update_message(self, key, arg=None):
        tag = f"<arg>{escape(_clean(arg))}</arg>" if arg else ""
        return self._call("update_message",
                          f"<request><key>{int(key)}</key>{tag}</request>")

    def delete_message(self, key):
        return self._call("delete_message",
                          f"<request><key>{int(key)}</key></request>")

    def create_reply(self, output, stage, exception, message):
        body = (f"<request><output>{escape(_clean(output))}</output>"
                f"<stage>{escape(_clean(stage))}</stage>"
                f"<exception>{escape(_clean(exception))}</exception>"
                f"<message>{int(message)}</message></request>")
        return self._call("create_reply", body)

    def get_replies(self):
        return self._call("get_replies", "<request/>")

    def get_reply(self, key):
        return self._call("get_reply",
                          f"<request><key>{int(key)}</key></request>")

    def update_reply(self, key, output=None):
        tag = f"<output>{escape(_clean(output))}</output>" if output else ""
        return self._call("update_reply",
                          f"<request><key>{int(key)}</key>{tag}</request>")

    def delete_reply(self, key):
        return self._call("delete_reply",
                          f"<request><key>{int(key)}</key></request>")

    def join_agents_messages(self):
        return self._call("join_agents_messages", "<request/>")