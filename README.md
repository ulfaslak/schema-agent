# schema_agent

Practical, robust structured generation for LLMs using Pydantic schemas. Provide a schema, a prompt, and a model; get back a validated `BaseModel` instance with automatic retries when validation fails.

*Note: This is minimalist experimental package, and it does nearly the same as [Instructor](https://github.com/567-labs/instructor), with some slight differences in implementation design. However, if you need this for production, I recommend using Instructor.*

<img width="500" height="385" alt="Screenshot 2025-09-22 at 13 24 17" src="https://github.com/user-attachments/assets/c4d417a9-3d2a-4743-a76b-f1bbb7f5671b" />


## Features


- Schema-first: define your output as a Pydantic model
- Automatic retries: validates via a tool call and re-prompts on failure
- Provider-agnostic: accepts LangChain-compatible models or a provider string (e.g. `"openai:gpt-4o-mini"`)
- Strong typing: returns a Pydantic instance alongside raw agent traces
- Simple API: one function `generate_with_schema(...)`

## Usage

Install from PyPI:

```bash
pip install schema_agent
# Optional OpenAI support (needed to run scripts/demo.py as-is)
pip install "schema_agent[openai]"
```

Basic example:

```python
from pydantic import BaseModel, Field
from schema_agent import generate_with_schema

class Person(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")

resp = generate_with_schema(
    user_prompt="Hos name was John Doe and he was 42 years old",
    llm="openai:gpt-4o-mini",   # or pass a LangChain model instance
    schema=Person,
    max_retries=2,
)

# Validated Pydantic instance
print(resp["output"])        # -> Person(name='John Doe', age=42)
print(resp["success"])      # -> True/False
print(resp["retries"])      # -> number of retries performed
```

With a LangChain model object:

```python
from langchain_openai import ChatOpenAI
from schema_agent import generate_with_schema

llm = ChatOpenAI(model="gpt-4o-mini")
resp = generate_with_schema(
    user_prompt="Hos name was John Doe and he was 42 years old",
    llm=llm,
    schema=Person,
    max_retries=2,
)
```

With a validation callback (example that extracts a phone number from a large text):

```python
def validate_output(x: str | dict) -> None:
    if x["name"] != "John Doe":
        raise ValueError("Name is not John Doe")

class PhoneNumber(BaseModel):
    phone_number: str = Field(description="Phone number")

def check_phone_number_in_data(x: str | dict) -> None:
    if x["phone_number"] not in large_text:
        raise ValueError("Extracted attribute 'phone_number' not found in data")

resp = generate_with_schema(
    user_prompt=large_text,  # large text that contains a phone number
    llm=llm,
    schema=Person,
    max_retries=2,
    validation_callback=check_phone_number_in_data,
)
```

Run the demo script:

```bash
pixi run demo
```

Notes:

- Set `OPENAI_API_KEY` in your environment if using OpenAI (e.g., via a `.env` file when installing the `openai` extra).
- On unexpected tool errors the call raises an exception; expected validation failures are retried up to `max_retries`.

## Project Structure

- `schema_agent/`: Package logic
  - `llm.py`: `generate_with_schema` agent orchestration and validation tool
  - `str.py`: schema-to-example string utilities
  - `utils.py`, `errors.py`, `consts.py`, `types.py`: helpers, exceptions, prompts, typings
- `tests/`: Unit tests for all modules
- `scripts/`: `demo.py` script

## Development

This package has been created with [pymc-labs/project-starter](https://github.com/pymc-labs/project-starter). It features:

- 📦 **`pixi`** for dependency and environment management.
- 🧹 **`pre-commit`** for formatting, spellcheck, etc. If everyone uses the same standard formatting, then PRs won't have flaky formatting updates that distract from the actual contribution. Reviewing code will be much easier.
- 🧪 **`pytest`** for testing.
- 🔄 **Github Actions** for running the pre-commit checks on each PR, automated testing and dependency management (dependabot). Merges to `main` publish to PyPI via trusted publishing.

### Prerequisites

- Python 3.11 or higher
- [Pixi package manager](https://pixi.sh/latest/)

### Get started

1. Run `pixi install` to install the dependencies.
2. Run `pixi r test` to run the tests.
3. Run `pre-commit install` to set up pre-commit hooks.
