from typing import List, Optional

from fastapi_camelcase import CamelModel
from pydantic import Field


class Label(CamelModel):
    name: str = Field(description="Assigned label")
    children: List["Label"] = Field(description="Sublabels")


class Location(CamelModel):
    country: Optional[str] = Field(
        description="Company address (country)", example="Germany"
    )
    city: Optional[str] = Field(description="Company address (city)", example="Berlin")
    continent: Optional[str] = Field(
        description="Company address (continent)", example="Europe"
    )
    state: Optional[str] = Field(
        description="Company address (state/land)", example="Berlin"
    )
    latitude: Optional[float] = Field(example=52.5167)
    longitude: Optional[float] = Field(example=13.3833)
    zip_code: Optional[str] = Field(
        description="Company address (zip code)", example="10999"
    )