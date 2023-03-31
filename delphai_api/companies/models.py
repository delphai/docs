from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from fastapi_camelcase import CamelModel
from pydantic import Field

from ..types import ObjectId
from ..models import Label, Location


class EmployeeCount(CamelModel):
    min: Optional[int] = Field(
        description="Bottom range of the employee count interval", example=11
    )
    max: Optional[int] = Field(
        description="Top range of the employee count interval", example=50
    )
    exact: Optional[int] = Field(description="Exact number for employees", example=30)
    range: Optional[str] = Field(
        description="Employee count interval displayed in delphai", example="11-50"
    )


class CompanyDescription(CamelModel):
    long: Optional[str] = Field(
        description="Company's default description",
        example=(
            "delphai is an AI and big data analytics software platform that informs "
            "business decisions and validates strategies"
        ),
    )
    short: Optional[str] = Field(
        description="Truncated version of company's default description",
        example=("delphai is an AI and big data analytics software platform"),
    )


class CompanyRevenue(CamelModel):
    currency: Optional[str] = Field(
        description="currency of revenue number", example="EUR"
    )
    annual: Optional[int] = Field(
        description="Annual revenue number for specified year", example=5000000
    )


class Company(CamelModel):
    id: ObjectId = Field(..., description="Internal company ID")
    name: str = Field(..., description="Name of the company", example="Delphai")
    url: str = Field(..., description="Webpage of the company", example="delphai.com")
    descriptions: Optional[Dict[str, CompanyDescription]]
    founding_year: Optional[int] = Field(description="Founding year", example=2020)
    headquarters: Optional[Location] = Field(description="Company address")
    employee_count: Optional[EmployeeCount] = Field(description="Number of employees")
    additional_urls: Optional[Dict[str, str]] = Field(
        example={"linkedin": "https://www.linkedin.com/company/delphai"}
    )
    Companyrevenue: Optional[Dict[str, CompanyRevenue]] = Field(
        description="Company revenue with currency"
    )
    products: Optional[List[str]] = Field(
        description="List of company products", example=["Software"]
    )


class CompaniesSearchResult(CamelModel):
    company: Company
    score: float = Field(default=0, description="Search score", example="202.35745")
    snippets: List[str] = Field(
        default=[],
        description="Snippets containing query keywords",
        example=[
            "delphai is an AI and big data analytics software platform that informs "
            "business decisions and validates strategies"
        ],
    )


class CompaniesSearchResults(CamelModel):
    results: List[CompaniesSearchResult]
    total: int = Field(..., description="Number of results", example=1337)


class CompanyPeer(CamelModel):
    company: Company
    score: float = Field(default=0, description="Search score", example="202.35745")


class CompanyPeers(CamelModel):
    results: List[CompanyPeer]
    total: int = Field(..., description="Number of results", example=5)


class NewsArticleType(str, Enum):
    NEWS = "news"
    PRESS_RELEASE = "press release"


class NewsArticle(CamelModel):
    company_id: ObjectId = Field(..., description="Internal company ID")
    url: str = Field(..., description="Article URL")
    type: NewsArticleType = Field(..., description="Type of article")
    published: datetime = Field(..., description="When the article was published")
    snippet: str = Field(
        ..., description="Snippet of the article mentioning the company"
    )
    language: Optional[str] = Field(
        description="Original language of the article in ISO 639 code"
    )
    labels: Optional[List[Label]]
    title: str = Field(..., description="Article title")
    added: datetime = Field(..., description="When the article was added to delphai")


class NewsArticles(CamelModel):
    results: List[NewsArticle]
    total: int = Field(..., description="Number of results")


class JobPosting(CamelModel):
    company_id: ObjectId = Field(..., description="Internal company ID")
    url: str = Field(..., description="Job posting URL")
    published: datetime = Field(..., description="When the job post was published")
    location: Optional[str] = Field(description="Location of the position")
    job_description: Optional[str] = Field(description="Description of the position")
    language: Optional[str] = Field(description="Original language of the job posting")
    title: str = Field(..., description="Position title")
    added: datetime = Field(
        ..., description="When the job posting was added to delphai"
    )


class JobPostings(CamelModel):
    results: List[JobPosting]
    total: int = Field(..., description="Number of results")
