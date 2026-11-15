import pytest
from pydantic import ValidationError

from models import Record


class Item(Record):
    """A record with one text field."""

    name: str


def test_unknown_fields_are_rejected_at_the_boundary() -> None:
    with pytest.raises(ValidationError):
        Item.model_validate({"name": "tea", "unexpected": True})


def test_text_is_stripped() -> None:
    assert Item.model_validate({"name": "  tea "}).name == "tea"
