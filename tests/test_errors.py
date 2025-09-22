from schema_agent.errors import ModelOutputError, UnexpectedToolcallError


def test_model_output_error_is_exception():
    err = ModelOutputError("msg")
    assert isinstance(err, Exception)


def test_unexpected_toolcall_error_is_exception():
    err = UnexpectedToolcallError("msg")
    assert isinstance(err, Exception)
