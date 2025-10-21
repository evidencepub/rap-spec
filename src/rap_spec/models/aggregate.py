"""Aggregate statistics schema."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AggregateFilters(BaseModel):
    """Filters applied before aggregation."""

    model_config = ConfigDict(populate_by_name=True)

    participant: Optional[Union[str, List[str]]] = Field(
        None, description="Participant filter(s)"
    )
    session: Optional[Union[str, List[str]]] = Field(None, description="Session filter(s)")
    group: Optional[str] = Field(None, description="Group filter")
    age_range: Optional[Dict[str, float]] = Field(
        None, alias="ageRange", description="Age range filter"
    )


class MeanValue(BaseModel):
    """Mean value with optional units."""

    model_config = ConfigDict(populate_by_name=True)

    value: float = Field(..., description="Mean value")
    units: Optional[str] = Field(None, description="Units")


class QuantileValues(BaseModel):
    """Quantile values."""

    model_config = ConfigDict(populate_by_name=True)

    q25: Optional[float] = Field(None, description="25th percentile")
    q50: Optional[float] = Field(None, description="50th percentile (median)")
    q75: Optional[float] = Field(None, description="75th percentile")


class ConfidenceInterval(BaseModel):
    """Confidence interval."""

    model_config = ConfigDict(populate_by_name=True)

    level: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence level (e.g., 0.95 for 95%)",
    )
    lower: float = Field(..., description="Lower bound")
    upper: float = Field(..., description="Upper bound")


class Statistics(BaseModel):
    """Statistical measures."""

    model_config = ConfigDict(populate_by_name=True)

    mean: Optional[Union[float, MeanValue]] = Field(None, description="Mean value")
    median: Optional[float] = Field(None, description="Median value")
    std: Optional[float] = Field(None, description="Standard deviation")
    sem: Optional[float] = Field(None, description="Standard error of the mean")
    variance: Optional[float] = Field(None, description="Variance")
    min: Optional[float] = Field(None, description="Minimum value")
    max: Optional[float] = Field(None, description="Maximum value")
    range: Optional[List[float]] = Field(
        None, min_length=2, max_length=2, description="Range [min, max]"
    )
    quantiles: Optional[QuantileValues] = Field(None, description="Quantile values")
    confidence_interval: Optional[ConfidenceInterval] = Field(
        None, alias="confidenceInterval", description="Confidence interval"
    )


class Histogram(BaseModel):
    """Histogram distribution."""

    model_config = ConfigDict(populate_by_name=True)

    bins: Optional[List[float]] = Field(None, description="Histogram bin edges")
    counts: Optional[List[int]] = Field(None, description="Counts per bin")


class KDE(BaseModel):
    """Kernel density estimate."""

    model_config = ConfigDict(populate_by_name=True)

    x: Optional[List[float]] = Field(None, description="X values")
    y: Optional[List[float]] = Field(None, description="Y values (density)")


class Distribution(BaseModel):
    """Distribution information."""

    model_config = ConfigDict(populate_by_name=True)

    histogram: Optional[Histogram] = Field(None, description="Histogram distribution")
    kde: Optional[KDE] = Field(None, description="Kernel density estimate")


class AggregateLinks(BaseModel):
    """Links to related resources."""

    model_config = ConfigDict(populate_by_name=True)

    products: Optional[HttpUrl] = Field(
        None, description="Link to products in this group"
    )
    raw_data: Optional[HttpUrl] = Field(
        None, alias="rawData", description="Link to download raw aggregate data"
    )


class AggregateGroup(BaseModel):
    """Aggregate results for a single group."""

    model_config = ConfigDict(populate_by_name=True)

    participant: Optional[str] = Field(None, description="Participant ID")
    session: Optional[str] = Field(None, description="Session ID")
    group: Optional[str] = Field(None, description="Group name")
    participant_count: Optional[int] = Field(
        None, ge=0, alias="participantCount", description="Number of participants in this group"
    )
    product_count: Optional[int] = Field(
        None, ge=0, alias="productCount", description="Number of products in this group"
    )
    statistics: Statistics = Field(..., description="Statistical measures")
    distribution: Optional[Distribution] = Field(None, description="Distribution information")
    links: Optional[AggregateLinks] = Field(None, description="Links to related resources")


class ComparisonGroup(BaseModel):
    """Group being compared."""

    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, description="Group name")
    participant_count: Optional[int] = Field(
        None, alias="participantCount", description="Number of participants"
    )
    statistics: Optional[Dict[str, float]] = Field(
        None, description="Group statistics (mean, std)"
    )


class EffectSize(BaseModel):
    """Effect size measure."""

    model_config = ConfigDict(populate_by_name=True)

    measure: Literal["cohensD", "hedgesG", "glassD", "eta-squared", "omega-squared"] = Field(
        ..., description="Effect size measure type"
    )
    value: float = Field(..., description="Effect size value")


class StatisticalTest(BaseModel):
    """Statistical test results."""

    model_config = ConfigDict(populate_by_name=True)

    method: Literal["t-test", "anova", "mann-whitney", "kruskal-wallis", "chi-square"] = Field(
        ..., description="Statistical test used"
    )
    statistic: float = Field(..., description="Test statistic value")
    p_value: float = Field(
        ..., ge=0, le=1, alias="pValue", description="P-value"
    )
    significant: Optional[bool] = Field(
        None, description="Whether result is significant at chosen alpha"
    )
    alpha: Optional[float] = Field(
        default=0.05, description="Significance threshold"
    )
    effect_size: Optional[EffectSize] = Field(
        None, alias="effectSize", description="Effect size"
    )
    degrees_of_freedom: Optional[Union[float, List[float]]] = Field(
        None, alias="degreesOfFreedom", description="Degrees of freedom"
    )


class PostHocComparison(BaseModel):
    """Post-hoc pairwise comparison."""

    model_config = ConfigDict(populate_by_name=True)

    group1: Optional[str] = Field(None, description="First group")
    group2: Optional[str] = Field(None, description="Second group")
    p_value: Optional[float] = Field(None, alias="pValue", description="P-value")
    adjusted: Optional[bool] = Field(
        None, description="Whether p-value is adjusted for multiple comparisons"
    )
    adjustment_method: Optional[Literal["bonferroni", "holm", "fdr_bh", "fdr_by"]] = Field(
        None, alias="adjustmentMethod", description="Adjustment method used"
    )


class Comparison(BaseModel):
    """Statistical comparison between groups."""

    model_config = ConfigDict(populate_by_name=True)

    groups: Optional[List[ComparisonGroup]] = Field(
        None, description="Groups being compared"
    )
    test: StatisticalTest = Field(..., description="Statistical test results")
    post_hoc: Optional[List[PostHocComparison]] = Field(
        None, alias="postHoc", description="Post-hoc pairwise comparisons"
    )


class AggregateMetadata(BaseModel):
    """Additional metadata about the aggregation."""

    model_config = ConfigDict(populate_by_name=True)

    computed_at: Optional[str] = Field(
        None, alias="computedAt", description="When these statistics were computed"
    )
    software_used: Optional[Dict[str, str]] = Field(
        None, alias="softwareUsed", description="Software used for computation"
    )
    excluded_products: Optional[List[Dict[str, str]]] = Field(
        None,
        alias="excludedProducts",
        description="Products excluded from aggregation and why",
    )


class AggregateStatistics(BaseModel):
    """Aggregated statistics across multiple research products.

    Provides group-level statistics, distributions, and statistical comparisons.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/aggregate.json",
        },
    )

    context: Union[Literal["https://rap-spec.evidencepub.io/v1/context"], Dict[str, Any]] = Field(
        ..., alias="@context"
    )
    type_: Literal["AggregateStatistics"] = Field(
        default="AggregateStatistics", alias="@type"
    )
    id_: HttpUrl = Field(..., alias="@id", description="URI of this aggregate query")
    measure: str = Field(..., description="The measurement type being aggregated")
    grouping: Optional[str] = Field(
        None,
        description="The dimension(s) used for grouping",
        examples=["session", "participant", "group", "participant,session"],
    )
    filters: Optional[AggregateFilters] = Field(
        None, description="Filters applied before aggregation"
    )
    aggregates: List[AggregateGroup] = Field(
        ..., description="Array of aggregate results for each group"
    )
    comparison: Optional[Comparison] = Field(
        None, description="Statistical comparison between groups"
    )
    metadata: Optional[AggregateMetadata] = Field(
        None, description="Additional metadata about the aggregation"
    )
