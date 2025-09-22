from schema_agent.utils import get_last_item_of_type


class A:  # simple distinct classes for isinstance checks
    pass


class B:
    pass


def test_get_last_item_of_type_returns_last_match():
    items = [A(), B(), A(), B()]
    assert isinstance(get_last_item_of_type(items, A), A)
    assert isinstance(get_last_item_of_type(items, B), B)


def test_get_last_item_of_type_none_when_no_match():
    items = [A(), A()]
    assert get_last_item_of_type(items, B) is None
