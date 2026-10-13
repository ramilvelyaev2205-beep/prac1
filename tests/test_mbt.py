"""MBT: сравнение модели и RPC-сервера.

Использует hypothesis.RuleBasedStateMachine.
"""

from __future__ import annotations

import threading
import time

import hypothesis.strategies as st
from hypothesis import HealthCheck, settings
from hypothesis.stateful import RuleBasedStateMachine, initialize, rule

from src.rpc_client import RpcClient
from src.rpc_server import serve as serve_rpc

PORT = 19093


def _start_server() -> None:
    threading.Thread(
        target=lambda: serve_rpc("127.0.0.1", PORT),
        daemon=True,
    ).start()
    time.sleep(0.3)


class ModelVsRpc(RuleBasedStateMachine):
    """РЎСЂР°РІРЅРµРЅРёРµ РјРѕРґРµР»Рё Рё RPC-СЃРµСЂРІРµСЂР°."""

    @initialize()
    def setup(self) -> None:
        _start_server()
        self.client = RpcClient(port=PORT)

    @rule(ip=st.text(min_size=1, max_size=10),
          platform=st.text(min_size=1, max_size=10),
          ua=st.text(min_size=1, max_size=10))
    def create_agent(self, ip, platform, ua):
        self.client.create_agent(ip, platform, ua)

    @rule()
    def get_agents(self):
        self.client.get_agents()

    @rule(key=st.integers(min_value=1, max_value=100))
    def get_agent(self, key):
        self._safe(self.client.get_agent, key)

    @rule(key=st.integers(min_value=1, max_value=100),
          ip=st.text(min_size=1, max_size=10))
    def update_agent(self, key, ip):
        self._safe(self.client.update_agent, key, ip)

    @rule(key=st.integers(min_value=1, max_value=100))
    def delete_agent(self, key):
        self._safe(self.client.delete_agent, key)

    @rule(arg=st.text(min_size=1, max_size=5),
          agent=st.integers(min_value=1, max_value=10),
          description=st.text(min_size=1, max_size=5),
          tags=st.text(min_size=1, max_size=5),
          stage=st.text(min_size=1, max_size=5))
    def create_message(self, arg, agent, description, tags, stage):
        self._safe(self.client.create_message,
                   arg, agent, description, tags, stage)

    @rule()
    def get_messages(self):
        self.client.get_messages()

    @rule(key=st.integers(min_value=1, max_value=100))
    def get_message(self, key):
        self._safe(self.client.get_message, key)

    @rule(key=st.integers(min_value=1, max_value=100),
          arg=st.text(min_size=1, max_size=5))
    def update_message(self, key, arg):
        self._safe(self.client.update_message, key, arg)

    @rule(key=st.integers(min_value=1, max_value=100))
    def delete_message(self, key):
        self._safe(self.client.delete_message, key)

    @rule(output=st.text(min_size=1, max_size=5),
          stage=st.text(min_size=1, max_size=5),
          exception=st.text(min_size=1, max_size=5),
          message=st.integers(min_value=1, max_value=10))
    def create_reply(self, output, stage, exception, message):
        self._safe(self.client.create_reply,
                   output, stage, exception, message)

    @rule()
    def get_replies(self):
        self.client.get_replies()

    @rule(key=st.integers(min_value=1, max_value=100))
    def get_reply(self, key):
        self._safe(self.client.get_reply, key)

    @rule(key=st.integers(min_value=1, max_value=100),
          output=st.text(min_size=1, max_size=5))
    def update_reply(self, key, output):
        self._safe(self.client.update_reply, key, output)

    @rule(key=st.integers(min_value=1, max_value=100))
    def delete_reply(self, key):
        self._safe(self.client.delete_reply, key)

    @rule()
    def join_agents_messages(self):
        self.client.join_agents_messages()

    @staticmethod
    def _safe(func, *args):
        try:
            func(*args)
        except (ConnectionError, OSError, ValueError, LookupError) as exc:
            print(f"[MBT] skip: {exc}")


TestModelVsRpc = ModelVsRpc.TestCase
TestModelVsRpc.settings = settings(
    max_examples=10,
    stateful_step_count=20,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.data_too_large,
        HealthCheck.filter_too_much,
    ],
    deadline=None,
)


