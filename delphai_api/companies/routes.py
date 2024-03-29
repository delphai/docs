import enum

from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional, Tuple
from delphai_fastapi.auth import Authorization
from delphai_fastapi.companies.models import (
    CompaniesSearchResults,
    Company,
    CompanyCustomAttributes,
    CompanyCustomAttributesUpdate,
    CompanyPeers,
)
from delphai_fastapi.job_posts.models import JobPosts
from delphai_fastapi.news_articles.models import NewsArticles
from delphai_fastapi.funding_rounds.models import FundingRounds
from delphai_fastapi.types import LimitOffset, ObjectId
from fastapi import APIRouter, Path, Query

from ..types import AddedField, EmployeeCountField, HeadquartersField, Ownership


router = APIRouter(tags=["Companies"], dependencies=[Authorization])


class CompanyInclude(str, enum.Enum):
    CUSTOM_ATTRIBUTES = "customAttributes"


@router.get("", response_model=CompaniesSearchResults)
async def search_companies(
    query: Optional[str] = Query(None, description="Search query"),
    url: Optional[str] = Query(None, description="Get company by url"),
    name: Optional[str] = Query(None, description="Get company by name"),
    headquarters_country: Optional[str] = Query(
        None, description="Get company by country", alias="headquarters.country"
    ),
    headquarters_city: Optional[str] = Query(
        None, description="Get company by city", alias="headquarters.city"
    ),
    founding_year: Optional[int] = Query(
        None, description="Get company by founding year", alias="foundingYear"
    ),
    industries: Optional[List[str]] = Query(
        None, description="Get company by similar industries"
    ),
    products: Optional[List[str]] = Query(
        None, description="Get company by similar products"
    ),
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


@router.get("/{companyId}/custom-attributes", response_model=CompanyCustomAttributes)
async def get_company_custom_attributes(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
) -> Dict[str, Any]:
    ...


@router.patch("/{companyId}/custom-attributes", response_model=CompanyCustomAttributes)
async def update_company_custom_attributes(
    custom_attributes: CompanyCustomAttributesUpdate,
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
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
    sortBy: Annotated[List[str], Query()] = [],  # noqa: N803
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
    sortBy: Annotated[List[str], Query()] = [],  # noqa: N803
) -> Dict[str, Any]:
    """
    Lists all job posts from a company or filtered by creation date.\n
    To filter by creation date, a comparison option can be used.\n
    Options: greater than (gt), less than (lt), greater than or equal (gte),
    less than or equal (lte)\n
    Example: ?added[gt]=2022-09-15T15:53:00Z
    """


@router.get("/{companyId}/funding-rounds", response_model=FundingRounds)
async def get_funding_rounds(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    limit_offset: tuple[int, int] = LimitOffset(),
    sortBy: Annotated[List[str], Query()] = [],  # noqa: N803
) -> Dict[str, Any]:
    """
    Lists all funding rounds of specified company.\n
    """
