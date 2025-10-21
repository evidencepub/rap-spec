"""Research product schema."""

from typing import Any, Dict, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from rap_spec.models.common import (
    ComputeEnvironment,
    CreativeWork,
    DataDownload,
    ProcessingProvenance,
    PropertyValue,
    ScholarlyArticle,
)
from rap_spec.measurements.relaxometry_mri import RelaxometryMRIMeasurement
from rap_spec.measurements.timeseries import TimeseriesMeasurement
from rap_spec.data_types.vector_data import VectorData


class DemographicData(BaseModel):
    """Demographic information for a participant (embedded reference)."""

    model_config = ConfigDict(populate_by_name=True)

    age: Optional[Dict[str, Any]] = Field(None, description="Age information")
    sex: Optional[Literal["M", "F", "other", "unknown"]] = Field(
        None, description="Biological sex"
    )
    group: Optional[str] = Field(None, description="Experimental group assignment")


class ParticipantReference(BaseModel):
    """Reference to a research participant."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["Participant"] = Field(default="Participant", alias="@type")
    id_: HttpUrl = Field(..., alias="@id", description="Participant URI")
    identifier: str = Field(..., description="Participant ID")
    demographic_data: Optional[DemographicData] = Field(
        None, alias="demographicData", description="Demographic information"
    )


class ResearchProduct(BaseModel):
    """A processed, analysis-ready research data product.

    Main entity representing a research data product with measurement metadata,
    actual data, provenance chain, and distribution information.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/research-product.json",
        },
    )

    context: Union[Literal["https://rap-spec.evidencepub.io/v1/context"], Dict[str, Any]] = Field(
        ..., alias="@context"
    )
    type_: Literal["ResearchProduct"] = Field(
        default="ResearchProduct", alias="@type"
    )
    id_: HttpUrl = Field(
        ...,
        alias="@id",
        description="Unique URI identifying this research product",
    )
    identifier: Optional[PropertyValue] = Field(
        None,
        description="DOI or other persistent identifier",
    )
    product_type: Literal[
        "processed_timeseries",
        "processed_scalar",
        "processed_image",
        "processed_spatial",
        "processed_categorical",
        "processed_vector",
    ] = Field(..., alias="productType", description="Type of data product")
    processing_level: Literal["raw", "preprocessed", "analysis_ready", "aggregated"] = Field(
        ..., alias="processingLevel", description="Level of processing applied"
    )
    data: Optional[VectorData] = Field(
        None,
        description="The actual data for this research product",
    )
    participant: ParticipantReference = Field(
        ...,
        description="Reference to the research participant",
    )
    measurement: Union[RelaxometryMRIMeasurement, TimeseriesMeasurement] = Field(
        ...,
        description="Measurement details",
    )
    provenance: Optional[ProcessingProvenance] = Field(
        None,
        description="Provenance tracking for data processing",
    )
    compute_environment: Optional[ComputeEnvironment] = Field(
        None,
        alias="computeEnvironment",
        description="Computational environment information",
    )
    license: Optional[CreativeWork] = Field(
        None,
        description="License for this data product",
    )
    distribution: Optional[DataDownload] = Field(
        None,
        description="Distribution/download information",
    )
    citation: Optional[ScholarlyArticle] = Field(
        None,
        description="Citation to related publication",
    )
    quality_metrics: Optional[Dict[str, Any]] = Field(
        None,
        alias="qualityMetrics",
        description="Quality assessment metrics",
    )
