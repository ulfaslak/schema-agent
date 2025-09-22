from schema_agent.consts import RETRY_SIGNAL, FAILURE_PROMPT, SYSTEM_PROMPT


def test_retry_signal_contains_brackets():
    assert RETRY_SIGNAL.startswith("[") and RETRY_SIGNAL.endswith("]")


def test_failure_prompt_mentions_retry():
    assert "try again" in FAILURE_PROMPT.lower()


def test_system_prompt_includes_placeholders():
    assert "{schema}" in SYSTEM_PROMPT
    assert "{RETRY_SIGNAL}" in SYSTEM_PROMPT
