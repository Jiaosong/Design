"""OLEANDER source authority states."""

SOURCE_STATES = {
    "SOURCE": "editable authority",
    "DERIVED": "generated from source, not authority",
    "DIAGNOSTIC": "analysis output only",
    "ARCHIVED": "historical reference",
}


def can_edit(state: str) -> bool:
    return state == "SOURCE"


__all__ = ["SOURCE_STATES", "can_edit"]
