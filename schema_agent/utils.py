from typing import Any


def get_last_item_of_type(items: list[Any], item_type: type) -> Any | None:
    """Get the last item of a given type from a list.

    Args:
        items: The list of items to search through
        item_type: The type of item to get the last of

    Returns:
        The last item of the given type from the list
    """
    return next(
        (m for m in items[::-1] if isinstance(m, item_type)),
        None,
    )
