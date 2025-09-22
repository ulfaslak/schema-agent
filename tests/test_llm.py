import json
from typing import Any

import pytest
from pydantic import BaseModel, Field

from langchain_core.messages import ToolMessage
from schema_agent.errors import UnexpectedToolcallError
from schema_agent.llm import generate_with_schema


class DummyAgent:
    def __init__(self, scripted_messages_per_call: list[list[Any]]):
        self.scripted_messages_per_call = scripted_messages_per_call
        self.calls = 0

    def invoke(self, _: dict[str, Any]) -> dict[str, Any]:
        msgs = self.scripted_messages_per_call[self.calls]
        self.calls += 1
        return {"messages": msgs}


class SimpleSchema(BaseModel):
    value: int = Field(description="Some integer value")


def _call_generate_with_agent(agent, max_retries=2):
    # monkeypatch create_react_agent to return our dummy agent
    import schema_agent.llm as llm_mod

    original = llm_mod.create_react_agent
    llm_mod.create_react_agent = lambda **_: agent
    try:
        resp = generate_with_schema(
            user_prompt="give me a value",
            llm="dummy",
            schema=SimpleSchema,
            max_retries=max_retries,
        )
    finally:
        llm_mod.create_react_agent = original
    return resp


def test_generate_success_first_try():
    ok = ToolMessage(json.dumps({"value": 1}), status="success")
    agent = DummyAgent([[ok]])
    resp = _call_generate_with_agent(agent)
    assert resp["success"] is True
    assert resp["retries"] == 0


def test_generate_retries_then_succeeds():
    err = ToolMessage("Invalid JSON: x. [VALIDATION FAILED. RETRY.]", status="error")
    ok = ToolMessage(json.dumps({"value": 2}), status="success")
    agent = DummyAgent([[err], [ok]])
    resp = _call_generate_with_agent(agent)
    assert resp["success"] is True
    assert resp["retries"] == 1


def test_generate_unexpected_error_raises():
    err = ToolMessage("Some other error", status="error")
    agent = DummyAgent([[err]])
    with pytest.raises(UnexpectedToolcallError):
        _call_generate_with_agent(agent)
