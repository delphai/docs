from datetime import datetime

from fastapi import Query, Depends, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, create_model
from typing import Iterable, Optional


def subfields(field_name: str, field_type: type, subfields: Iterable[str], **kwargs):
    root_field = {"": (field_type, Query(alias=field_name, **kwargs))}

    # Model with root field for the schema definition
    field_model = create_model("FieldModel", **root_field)

    # Model with all fields for parsing
    subfields_model = create_model(
        "SubfieldsModel",
        **root_field,
        **{
            subfield: (field_type, Query(alias=f"{field_name}[{subfield}]", **kwargs))
            for subfield in subfields
        },
    )

    async def parse_subfields(request: Request, root_field: field_model = Depends()):
        try:
            return subfields_model.parse_obj(request.query_params).dict(
                exclude_none=True
            )
        except ValidationError as error:
            raise RequestValidationError(error.raw_errors)

    return Depends(parse_subfields)


AddedField = subfields(
    "added",
    Optional[datetime],
    ["gt", "gte", "lt", "lte"],
    example="2022-09-15T15:53:00Z",
)
