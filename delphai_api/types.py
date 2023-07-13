from datetime import datetime
import enum

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


HeadquartersField = subfields(
    "headquarters",
    Optional[str],
    ["continent", "country", "state", "city"],
    description="Headquarters filter. Available options: continent, country, state, city.",  # noqa E501
    example="[country]=Germany",
)


EmployeeCountField = subfields(
    "employeeCount",
    Optional[int],
    ["gte", "lte"],
    description="Employee count filter. Available options: gte, lte",
    example="[gte]=500",
)


class Ownership(str, enum):
    PRIVATE = "private"
    PUBLIC = "public"
