import sys
import types


def _ensure_module(name: str):
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)
    return sys.modules[name]


def pytest_sessionstart(session):  # noqa: ARG001
    # Provide minimal stubs for optional external deps to allow import-time resolution
    language_models = _ensure_module("langchain_core.language_models")
    messages = _ensure_module("langchain_core.messages")
    tools = _ensure_module("langchain_core.tools")
    prebuilt = _ensure_module("langgraph.prebuilt")

    class LanguageModelLike:  # minimal stub type
        pass

    class ToolMessage:  # minimal stub matching attributes used
        def __init__(self, content: str, status: str = "success") -> None:
            self.content = content
            self.status = status

    class Tool:  # minimal stub matching attributes used
        def __init__(self, name: str, description: str, func):  # noqa: ANN001
            self.name = name
            self.description = description
            self.func = func

    def create_react_agent(**kwargs):  # noqa: ANN001, ANN003
        # In unit tests we overwrite this via monkeypatch where needed.
        class _Dummy:
            def invoke(self, _):  # noqa: ANN001, ANN202
                return {"messages": []}

        return _Dummy()

    language_models.LanguageModelLike = LanguageModelLike
    messages.ToolMessage = ToolMessage
    tools.Tool = Tool
    prebuilt.create_react_agent = create_react_agent
