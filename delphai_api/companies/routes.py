from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Path, Query

from ..auth import OAuth2Token
from ..types import AddedField, LimitOffset, ObjectId, Tuple

from .models import (
    CompaniesSearchResults,
    Company,
    CompanyPeers,
    JobPosts,
    NewsArticles,
)

router = APIRouter(tags=["Companies"], dependencies=[OAuth2Token])


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
) -> Dict[str, Any]:
    ...


@router.get("/{companyId}/peers", response_model=CompanyPeers)
async def list_company_peers(
    companyId: ObjectId = Path(..., description="Internal company ID"),  # noqa: N803
    limit_offset: Tuple[int, int] = LimitOffset(limit_default=5, limit_max=50),
) -> Dict[str, Any]:
    """
    Returns top peers of specified company\n
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
