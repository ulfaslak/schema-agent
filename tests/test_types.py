from schema_agent.types import RetryAgentResponse
from pydantic import BaseModel


class DummyModel(BaseModel):
    pass


def test_retry_agent_response_typed_dict_keys():
    resp: RetryAgentResponse = {
        "response": {},
        "reply": DummyModel(),
        "success": True,
        "retries": 1,
    }
    assert set(resp.keys()) == {"response", "reply", "success", "retries"}
