"""TCP RPC-СЃРµСЂРІРµСЂ (РІР°СЂРёР°РЅС‚ 7).

Р–СѓСЂРЅР°Р»РёСЂРѕРІР°РЅРёРµ: РєР°Р¶РґС‹Р№ РѕС‚РІРµС‚ РїРёС€РµС‚СЃСЏ РІ stdout.
"""

from __future__ import annotations

import socketserver
import xml.etree.ElementTree as xml_et

from src import repository as repo
from src.models import Storage
from src.protocol import pack_response, read_request

OPCODES = {
    1: "create_agent",
    2: "get_agents",
    3: "get_agent",
    4: "update_agent",
    5: "delete_agent",
    6: "create_message",
    7: "get_messages",
    8: "get_message",
    9: "update_message",
    10: "delete_message",
    11: "create_reply",
    12: "get_replies",
    13: "get_reply",
    14: "update_reply",
    15: "delete_reply",
    16: "join_agents_messages",
}

class RpcHandler(socketserver.BaseRequestHandler):
    storage: Storage

    def handle(self) -> None:
        while True:
            try:
                opcode, body = read_request(self.request)
            except (ConnectionError, OSError):
                return
            if opcode == 0:
                return
            try:
                result = self._dispatch(opcode, body)
            except (LookupError, ValueError, TypeError, KeyError) as exc:
                result = f"<error>{type(exc).__name__}: {exc}</error>"
            print(f"[RPC] opcode={opcode} -> {result[:60]}...")
            self.request.sendall(pack_response(opcode, result))

    def _dispatch(self, opcode: int, body: str) -> str:
        name = OPCODES.get(opcode)
        if name is None:
            return f"<error>unknown opcode {opcode}</error>"
        handler = getattr(self, f"_op_{name}", None)
        if handler is None:
            return f"<error>no handler for {name}</error>"
        return handler(body)

    def _op_create_agent(self, body: str) -> str:
        n = xml_et.fromstring(body)
        a = repo.create_agent(self.storage, n.findtext("ip", ""),
                              n.findtext("platform", ""),
                              n.findtext("user_agent", ""))
        return f"<agent><key>{a.key}</key></agent>"

    def _op_get_agents(self, _b: str) -> str:
        items = "".join(
            f"<agent><key>{a.key}</key><ip>{a.ip}</ip></agent>"
            for a in repo.get_agents(self.storage))
        return f"<agents>{items}</agents>"

    def _op_get_agent(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        a = repo.get_agent(self.storage, key)
        return f"<agent><key>{a.key}</key><ip>{a.ip}</ip></agent>"

    def _op_update_agent(self, body: str) -> str:
        n = xml_et.fromstring(body)
        a = repo.update_agent(self.storage, int(n.findtext("key", "0")),
                              ip=n.findtext("ip"),
                              platform=n.findtext("platform"),
                              user_agent=n.findtext("user_agent"))
        return f"<agent><key>{a.key}</key></agent>"

    def _op_delete_agent(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        repo.delete_agent(self.storage, key)
        return "<ok/>"

    def _op_create_message(self, body: str) -> str:
        n = xml_et.fromstring(body)
        m = repo.create_message(self.storage, n.findtext("arg", ""),
                                int(n.findtext("agent", "0")),
                                n.findtext("description", ""),
                                n.findtext("tags", ""),
                                n.findtext("stage", ""))
        return f"<message><key>{m.key}</key></message>"

    def _op_get_messages(self, _b: str) -> str:
        items = "".join(
            f"<message><key>{m.key}</key></message>"
            for m in repo.get_messages(self.storage))
        return f"<messages>{items}</messages>"

    def _op_get_message(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        m = repo.get_message(self.storage, key)
        return f"<message><key>{m.key}</key></message>"

    def _op_update_message(self, body: str) -> str:
        n = xml_et.fromstring(body)
        m = repo.update_message(self.storage, int(n.findtext("key", "0")),
                                arg=n.findtext("arg"),
                                description=n.findtext("description"),
                                tags=n.findtext("tags"),
                                stage=n.findtext("stage"))
        return f"<message><key>{m.key}</key></message>"

    def _op_delete_message(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        repo.delete_message(self.storage, key)
        return "<ok/>"

    def _op_create_reply(self, body: str) -> str:
        n = xml_et.fromstring(body)
        r = repo.create_reply(self.storage, n.findtext("output", ""),
                              n.findtext("stage", ""),
                              n.findtext("exception", ""),
                              int(n.findtext("message", "0")))
        return f"<reply><key>{r.key}</key></reply>"

    def _op_get_replies(self, _b: str) -> str:
        items = "".join(
            f"<reply><key>{r.key}</key></reply>"
            for r in repo.get_replies(self.storage))
        return f"<replies>{items}</replies>"

    def _op_get_reply(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        r = repo.get_reply(self.storage, key)
        return f"<reply><key>{r.key}</key></reply>"

    def _op_update_reply(self, body: str) -> str:
        n = xml_et.fromstring(body)
        r = repo.update_reply(self.storage, int(n.findtext("key", "0")),
                              output=n.findtext("output"),
                              stage=n.findtext("stage"),
                              exception=n.findtext("exception"))
        return f"<reply><key>{r.key}</key></reply>"

    def _op_delete_reply(self, body: str) -> str:
        key = int(xml_et.fromstring(body).findtext("key", "0"))
        repo.delete_reply(self.storage, key)
        return "<ok/>"

    def _op_join_agents_messages(self, _b: str) -> str:
        pairs = repo.join_agents_messages(self.storage)
        items = "".join(
            f"<row><ip>{ip}</ip><platform>{p}</platform></row>"
            for ip, p in pairs)
        return f"<rows>{items}</rows>"


def serve(host: str = "127.0.0.1", port: int = 9090) -> None:
    RpcHandler.storage = Storage.empty()
    with socketserver.ThreadingTCPServer((host, port), RpcHandler) as server:
        print(f"RPC-СЃРµСЂРІРµСЂ Р·Р°РїСѓС‰РµРЅ РЅР° {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    serve()

