from typing import TypedDict

from pydantic import BaseModel


class RetryAgentResponse(TypedDict):
    response: dict
    reply: BaseModel
    success: bool
    retries: int
