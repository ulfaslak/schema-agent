import schema_agent


def test_public_api_exports_generate_with_schema():
    assert hasattr(schema_agent, "generate_with_schema")
