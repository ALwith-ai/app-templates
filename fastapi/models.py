"""Pydantic models of the API boundary: every request and response is one of these."""

from pydantic import BaseModel, ConfigDict


class Record(BaseModel):
    """Strict base model shared by API records."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
