class ModelOutputError(Exception):
    """
    Raised when the model fails, after multiple retries, to generate a response which matches the expected schema.
    """

    pass


class UnexpectedToolcallError(Exception):
    """
    Raised when a tool call results in an error that requires human intervention (bugfix).
    """

    pass
