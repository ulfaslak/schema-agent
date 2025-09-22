"""Top-level module for schema_agent."""

__all__ = ["generate_with_schema"]


def generate_with_schema(*args, **kwargs):  # type: ignore[no-untyped-def]
    # Lazy import to avoid importing heavy optional deps during package import
    from .llm import generate_with_schema as _generate_with_schema

    return _generate_with_schema(*args, **kwargs)
