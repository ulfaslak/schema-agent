from schema_agent.types import RetryAgentResponse
from pydantic import BaseModel


class DummyModel(BaseModel):
    pass


def test_retry_agent_response_typed_dict_keys():
    resp: RetryAgentResponse = {
        "response": {},
        "output": DummyModel(),
        "success": True,
        "retries": 1,
    }
    assert set(resp.keys()) == {"response", "output", "success", "retries"}
