from pydantic import BaseModel, Field
from dotenv import load_dotenv

from schema_agent import generate_with_schema

# Psst... create an .env file in the root directory with "OPENAI_API_KEY=sk-proj-..." inside.
# Or, you can create any LangGraph compatible LLM object and pass that to `generate_with_schema`.

load_dotenv()


class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")


def main() -> None:
    # Replace `llm` with a configured LanguageModelLike if desired, e.g.,
    # OpenAI(model="gpt-4o-mini"). Ensure your API key is set in env.
    resp = generate_with_schema(
        user_prompt="Return a person object for John Doe, age 42",
        llm="openai:gpt-4o-mini",
        schema=Person,
        max_retries=2,
    )
    print(f"Success: {resp['success']} after {resp['retries']} retries")
    print(resp["output"].model_dump_json(indent=2))  # full message trace from the agent


if __name__ == "__main__":
    main()
