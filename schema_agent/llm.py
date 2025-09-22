import json

from langchain_core.language_models import LanguageModelLike
from langchain_core.messages import ToolMessage
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, ValidationError

from .consts import FAILURE_PROMPT, RETRY_SIGNAL, SYSTEM_PROMPT
from .errors import ModelOutputError, UnexpectedToolcallError
from .types import RetryAgentResponse
from .utils import get_last_item_of_type
from .str import schema_to_example


def generate_with_schema(
    user_prompt: str,
    llm: str | LanguageModelLike,
    schema: type[BaseModel],
    max_retries: int = 2,
) -> RetryAgentResponse:
    """Generate output matching schema. Retries upon failure.

    Args:
        user_prompt: The user prompt to the agent
        llm: The LLM to use. Either a string or a `LanguageModelLike` object such as `OpenAI`, or
            a string like "openai:gpt-4o-mini". In the latter case, the model will be loaded
            automatically, assuming a valid LLM provider API key is set as a environment variable.
        schema: Pydantic schema that output should match.
        max_retries: The maximum number of times the agent will retry matching the schema.

    Returns:
        RetryAgentResponse
    """

    def _validate_output(x: str | dict) -> str:
        try:
            x = x if isinstance(x, dict) else json.loads(x)
            schema.model_validate(x)
            return json.dumps(x)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {x}. {RETRY_SIGNAL}") from e
        except ValidationError as e:
            raise ModelOutputError(f"{e}. {RETRY_SIGNAL}") from e

    agent = create_react_agent(
        model=llm,
        tools=[
            Tool(
                name="validate_output",
                description="Validate the generated output is valid JSON and matches the given schema.",
                func=_validate_output,
            )
        ],
        interrupt_after=["tools"],
    )

    messages = [
        (
            "system",
            SYSTEM_PROMPT.format(
                schema=schema_to_example(schema), RETRY_SIGNAL=RETRY_SIGNAL
            ),
        ),
        ("user", user_prompt),
    ]

    for retry_count in range(max_retries + 1):  # noqa: B007
        response = agent.invoke({"messages": messages})
        last_tool_message = get_last_item_of_type(response["messages"], ToolMessage)
        failed = last_tool_message and last_tool_message.status == "error"
        if failed and (
            RETRY_SIGNAL in last_tool_message.content
            or "ToolException" in last_tool_message.content
        ):
            last_tool_message_index = response["messages"].index(last_tool_message)
            messages = response["messages"][: last_tool_message_index + 1] + [
                (
                    "user",
                    FAILURE_PROMPT,
                )
            ]
        elif failed:
            raise UnexpectedToolcallError(
                f"Unexpected error during tool call: {last_tool_message.content}"
            )
        else:
            break

    return RetryAgentResponse(
        response=response,
        reply=schema(
            **json.loads(
                get_last_item_of_type(response["messages"], ToolMessage).content
            )
        ),
        success=not failed,
        retries=retry_count,
    )
