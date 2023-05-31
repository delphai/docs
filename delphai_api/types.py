from datetime import datetime

from bson.objectid import ObjectId as BsonObjectId
from fastapi import Query, Depends, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, create_model
from typing import Iterable, Optional, Tuple


class ObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(BsonObjectId(v))

    @classmethod
    def __modify_schema__(cls, field_schema, field):
        field_schema.update(
            type="string",
            minLength=24,
            maxLength=24,
            pattern="^[0-9a-fA-F]{24}$",
        )

        if "example" not in field.field_info.extra:
            field_schema["example"] = field.field_info.extra[
                "example"
            ] = "5ecd2d2d0faf391eadb211a7"


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


def LimitOffset(limit_default=20, limit_max=300):  # noqa: N802
    @Depends
    def get_limit_offset(
        limit: int = Query(
            default=limit_default,
            ge=0,
            le=limit_max,
            description="The maximum number of entries to be returned per call",
            example=limit_default,
        ),
        offset: int = Query(
            default=0,
            ge=0,
            description="The (zero-based) offset of the first item returned in the collection",  # noqa: E501
            example=0,
        ),
    ) -> Tuple[int, int]:
        return limit, offset

    return get_limit_offset
