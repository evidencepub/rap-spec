"""Research product collection schema."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from rap_spec.models.research_product import ResearchProduct


class AppliedFilters(BaseModel):
    """Currently applied filters."""

    model_config = ConfigDict(populate_by_name=True)

    participant: Optional[Union[str, List[str]]] = Field(
        None, description="Participant ID filter(s)"
    )
    measure: Optional[Union[str, List[str]]] = Field(
        None, description="Measurement type filter(s)"
    )
    session: Optional[Union[str, List[str]]] = Field(
        None, description="Session filter(s)"
    )
    group: Optional[str] = Field(None, description="Group filter")
    processing_level: Optional[
        Literal["raw", "preprocessed", "analysis_ready", "aggregated"]
    ] = Field(None, alias="processingLevel", description="Processing level filter")


class AvailableFilters(BaseModel):
    """All available filter values."""

    model_config = ConfigDict(populate_by_name=True)

    participant: Optional[List[str]] = Field(
        None, description="List of all participant IDs"
    )
    measure: Optional[List[str]] = Field(
        None, description="List of all measurement types"
    )
    session: Optional[List[str]] = Field(None, description="List of all session types")
    group: Optional[List[str]] = Field(
        None, description="List of all experimental groups"
    )
    processing_level: Optional[List[str]] = Field(
        None, alias="processingLevel", description="List of all processing levels"
    )


class Filter(BaseModel):
    """Information about applied and available filters."""

    model_config = ConfigDict(populate_by_name=True)

    applied: Optional[AppliedFilters] = Field(
        None, description="Currently applied filters"
    )
    available: Optional[AvailableFilters] = Field(
        None, description="All available filter values"
    )


class ProductSummary(BaseModel):
    """Brief summary of a research product."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ResearchProduct"] = Field(
        default="ResearchProduct", alias="@type"
    )
    id_: HttpUrl = Field(..., alias="@id", description="Product URI")
    identifier: str = Field(..., description="Product identifier")
    participant: Optional[Dict[str, Any]] = Field(
        None, description="Participant reference"
    )
    measurement: Optional[Dict[str, Any]] = Field(
        None, description="Measurement metadata"
    )
    summary: Optional[Dict[str, Any]] = Field(
        None, description="Brief summary of the product"
    )
    distribution: Optional[Dict[str, Any]] = Field(
        None, description="Distribution information"
    )


class PaginationLinks(BaseModel):
    """Pagination links."""

    model_config = ConfigDict(populate_by_name=True)

    first: Optional[HttpUrl] = Field(None, description="First page link")
    prev: Optional[HttpUrl] = Field(None, description="Previous page link")
    next: Optional[HttpUrl] = Field(None, description="Next page link")
    last: Optional[HttpUrl] = Field(None, description="Last page link")


class Pagination(BaseModel):
    """Pagination information for large collections."""

    model_config = ConfigDict(populate_by_name=True)

    page: Optional[int] = Field(None, ge=1, description="Current page number")
    page_size: Optional[int] = Field(
        None, ge=1, alias="pageSize", description="Number of items per page"
    )
    total_pages: Optional[int] = Field(
        None, ge=1, alias="totalPages", description="Total number of pages"
    )
    links: Optional[PaginationLinks] = Field(None, description="Pagination links")


class SortedBy(BaseModel):
    """Current sort order."""

    model_config = ConfigDict(populate_by_name=True)

    field: Optional[str] = Field(None, description="Field name being sorted by")
    order: Optional[Literal["asc", "desc"]] = Field(None, description="Sort order")


class ResearchProductCollection(BaseModel):
    """A collection of research products with filtering capabilities.

    Supports filtering, pagination, and sorting of research products.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/collection.json",
        },
    )

    context: Union[Literal["https://rap-spec.evidencepub.io/v1/context"], Dict[str, Any]] = Field(
        ..., alias="@context"
    )
    type_: Literal["ResearchProductCollection"] = Field(
        default="ResearchProductCollection", alias="@type"
    )
    id_: HttpUrl = Field(..., alias="@id", description="URI of this collection")
    total_items: int = Field(
        ...,
        ge=0,
        alias="totalItems",
        description="Total number of products in the collection",
    )
    filter: Optional[Filter] = Field(
        None, description="Information about applied and available filters"
    )
    member: List[Union[ResearchProduct, ProductSummary]] = Field(
        ..., description="Array of research products in this collection"
    )
    pagination: Optional[Pagination] = Field(
        None, description="Pagination information for large collections"
    )
    sorted_by: Optional[SortedBy] = Field(
        None, alias="sortedBy", description="Current sort order"
    )
