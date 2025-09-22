from pydantic import BaseModel, Field

from schema_agent.str import schema_to_example


class Address(BaseModel):
    street: str = Field(description="Street name")
    zip_code: int = Field(description="Postal code")


class User(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    address: Address = Field(description="Home address")


def test_schema_to_example_contains_comments_and_types():
    out = schema_to_example(User)
    assert '"name": str' in out
    assert '"age": int' in out
    assert '"address": {' in out
    # comments included
    assert "# Full name" in out
    assert "# Home address" in out


def test_schema_to_example_omit_fields():
    out = schema_to_example(User, omit_fields=["age"])
    assert '"age"' not in out
