from typing import TypedDict

from pydantic import BaseModel


class RetryAgentResponse(TypedDict):
    response: dict
    output: BaseModel
    success: bool
    retries: int
