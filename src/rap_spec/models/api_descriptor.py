"""Research API descriptor schema."""

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Paper(BaseModel):
    """Paper metadata."""

    model_config = ConfigDict(populate_by_name=True)

    doi: str = Field(
        ...,
        pattern=r"^10\.\d{4,}/[\S]+$",
        description="DOI of the paper",
    )
    title: str = Field(..., description="Paper title")
    authors: Optional[List[str]] = Field(None, description="List of authors")
    publication_date: Optional[str] = Field(
        None, alias="publicationDate", description="Publication date"
    )


class API(BaseModel):
    """API version and configuration."""

    model_config = ConfigDict(populate_by_name=True)

    version: str = Field(
        ...,
        pattern=r"^\d+\.\d+\.\d+$",
        description="API version (semver)",
    )
    rap_spec_version: str = Field(
        ...,
        alias="rapSpecVersion",
        pattern=r"^\d+\.\d+$",
        description="RAP specification version",
    )
    base_url: HttpUrl = Field(..., alias="baseUrl", description="API base URL")
    documentation: Optional[HttpUrl] = Field(None, description="API documentation URL")


class Endpoint(BaseModel):
    """API endpoint definition."""

    model_config = ConfigDict(populate_by_name=True)

    path: str = Field(..., description="Endpoint path")
    methods: List[Literal["GET", "POST", "PUT", "DELETE"]] = Field(
        ..., description="Supported HTTP methods"
    )
    description: Optional[str] = Field(None, description="Endpoint description")


class ResearchAPIDescriptor(BaseModel):
    """Discovery metadata for a RAP-compliant API.

    Provides metadata about the research paper, API configuration, and available endpoints.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/api-descriptor.json",
        },
    )

    context: Literal["https://rap-spec.evidencepub.io/v1/context"] = Field(
        ..., alias="@context"
    )
    type_: Literal["ResearchAPIDescriptor"] = Field(
        default="ResearchAPIDescriptor", alias="@type"
    )
    paper: Paper = Field(..., description="Paper metadata")
    api: API = Field(..., description="API configuration")
    endpoints: List[Endpoint] = Field(..., description="Available API endpoints")
    license: Optional[str] = Field(None, description="Data license")
    access_policy: Optional[Literal["open", "authenticated", "embargoed"]] = Field(
        None, alias="accessPolicy", description="Access policy"
    )
