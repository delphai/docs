import enum

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pydantic import Field
from delphai_fastapi.auth import Authorization
from delphai_fastapi.companies.models import (
    Company,
    CompaniesSearchResults,
    CompanyPeers,
)
from delphai_fastapi.job_posts.models import JobPosts
from delphai_fastapi.news_articles.models import NewsArticles
from delphai_fastapi.types import LimitOffset, ObjectId
from fastapi import APIRouter, Path, Query

from ..types import AddedField, EmployeeCountField, HeadquartersField, Ownership


router = APIRouter(tags=["Companies"], dependencies=[Authorization])


class CompanyInclude(str, enum.Enum):
    CUSTOM_ATTRIBUTES = "customAttributes"


class Company(Company):
    custom_attributes: Optional[Dict[str, Any]] = Field(
        description="Company custom attributes",
        example={"crmId": 84831, "labels": ["Partner", "Supplier"]},
    )


@router.get("", response_model=CompaniesSearchResults)
async def search_companies(
    query: str = Query(..., description="Query"),
    limit_offset: Tuple[int, int] = LimitOffset(),
) -> Dict[str, Any]:
    """
    Searches delphai for the query string and returns search results sorted by relevance
    """


@router.get("/{companyId}", response_model=Company)
async def get_company_profile(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    include: List[CompanyInclude] = Query([]),
) -> Dict[str, Any]:
    ...


@router.get("/{companyId}/peers", response_model=CompanyPeers)
async def list_company_peers(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    limit_offset: Tuple[int, int] = LimitOffset(limit_default=5, limit_max=50),
    headquarters: Dict[str, str] = HeadquartersField,
    employee_count: Dict[str, int] = EmployeeCountField,
    ownership: Optional[Ownership] = Query(default="", example="private"),
) -> Dict[str, Any]:
    """
    Returns top peers of specified company.\n
    To filter by headquarters, one of the option can be used.\n
    Options: continent, country, state, city\n
    Example: ?headquarters[country]=Germany\n
    To filter by employee count, a comparison option can be used.\n
    Options: greater than or equal (gte), less than or equal (lte)\n
    Example: ?employeeCount[gte]=500
    """


@router.get("/{companyId}/news", response_model=NewsArticles)
async def list_news_articles(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    created: Dict[str, datetime] = AddedField,
    limit_offset: Tuple[int, int] = LimitOffset(),
) -> Dict[str, Any]:
    """
    Lists all news articles from a company or filtered by creation date.\n
    To filter by creation date, a comparison option can be used.\n
    Options: greater than (gt), less than (lt), greater than or equal (gte),
    less than or equal (lte)\n
    Example: ?added[gt]=2022-09-15T15:53:00Z
    """


@router.get("/{companyId}/job-posts", response_model=JobPosts)
async def list_job_posts(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    created: Dict[str, datetime] = AddedField,
    limit_offset: Tuple[int, int] = LimitOffset(),
) -> Dict[str, Any]:
    """
    Lists all job posts from a company or filtered by creation date.\n
    To filter by creation date, a comparison option can be used.\n
    Options: greater than (gt), less than (lt), greater than or equal (gte),
    less than or equal (lte)\n
    Example: ?added[gt]=2022-09-15T15:53:00Z
    """
