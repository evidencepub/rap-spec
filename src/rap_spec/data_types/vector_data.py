"""Vector data schema for 1D numeric arrays."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from rap_spec.models.common import Unit


class Statistics(BaseModel):
    """Summary statistics for the vector."""

    model_config = ConfigDict(populate_by_name=True)

    mean: Optional[float] = Field(None, description="Mean value")
    median: Optional[float] = Field(None, description="Median value")
    std: Optional[float] = Field(None, description="Standard deviation")
    min: Optional[float] = Field(None, description="Minimum value")
    max: Optional[float] = Field(None, description="Maximum value")
    count: Optional[int] = Field(None, description="Number of values")


class VectorData(BaseModel):
    """Schema for vector data (1D array of values).

    Represents a 1D numeric array with associated unit, statistics, and optional metadata.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/data-types/vector-data.json",
        },
    )

    type_: Literal["VectorData"] = Field(default="VectorData", alias="@type")
    values: List[float] = Field(
        ...,
        min_length=1,
        description="Array of numeric values",
    )
    unit: Union[Unit, HttpUrl] = Field(
        ...,
        description="Unit of measurement for all values",
    )
    length: Optional[int] = Field(
        None,
        ge=1,
        description="Number of elements in the vector",
    )
    labels: Optional[List[str]] = Field(
        None,
        description="Optional labels for each value",
    )
    statistics: Optional[Statistics] = Field(
        None,
        description="Summary statistics for the vector",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the vector",
    )
