"""Common types and models shared across the RAP specification."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Unit(BaseModel):
    """Unit of measurement (QUDT-compatible structure)."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["Unit"] = Field(default="Unit", alias="@type")
    symbol: str = Field(..., description="Unit symbol (e.g., ms, Hz)")
    label: Optional[str] = Field(None, description="Human-readable unit label")
    uri: Optional[HttpUrl] = Field(None, description="QUDT unit URI")


class QuantityValue(BaseModel):
    """A quantity with a value and unit."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["QuantityValue"] = Field(default="QuantityValue", alias="@type")
    value: float = Field(..., ge=0, description="Numeric value")
    unit: str = Field(..., description="Unit of measurement")


class SoftwareApplication(BaseModel):
    """Software application metadata."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["SoftwareApplication"] = Field(
        default="SoftwareApplication", alias="@type"
    )
    name: str = Field(..., description="Software name")
    version: Optional[str] = Field(None, description="Software version")
    url: Optional[HttpUrl] = Field(None, description="Software URL")


class ProcessingStep(BaseModel):
    """A single step in the data processing pipeline."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ProcessingStep"] = Field(default="ProcessingStep", alias="@type")
    step_order: int = Field(..., ge=1, alias="stepOrder", description="Step order in pipeline")
    name: str = Field(..., description="Step name")
    software_agent: Optional[SoftwareApplication] = Field(
        None, alias="softwareAgent", description="Software used for this step"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        None, description="Processing parameters"
    )


class ProcessingProvenance(BaseModel):
    """Provenance tracking for data processing pipeline."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ProcessingProvenance"] = Field(
        default="ProcessingProvenance", alias="@type"
    )
    was_derived_from: Dict[str, Any] = Field(
        ...,
        alias="wasDerivedFrom",
        description="Source data this was derived from",
    )
    processing_steps: List[ProcessingStep] = Field(
        ..., alias="processingSteps", description="Processing pipeline steps"
    )


class ComputeEnvironment(BaseModel):
    """Computational environment information."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ComputeEnvironment"] = Field(
        default="ComputeEnvironment", alias="@type"
    )
    container_image: Optional[Dict[str, Any]] = Field(
        None, alias="containerImage", description="Container image information"
    )


class CreativeWork(BaseModel):
    """Creative work (for licenses)."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["CreativeWork"] = Field(default="CreativeWork", alias="@type")
    id_: HttpUrl = Field(..., alias="@id", description="License URI")
    name: Optional[str] = Field(None, description="License name")


class DataDownload(BaseModel):
    """Distribution/download information."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["DataDownload"] = Field(default="DataDownload", alias="@type")
    content_url: HttpUrl = Field(..., alias="contentUrl", description="Download URL")
    encoding_format: Optional[str] = Field(
        None, alias="encodingFormat", description="File format (MIME type)"
    )
    content_size: Optional[str] = Field(
        None, alias="contentSize", description="File size"
    )


class PropertyValue(BaseModel):
    """Property value (used for identifiers like DOI)."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["PropertyValue"] = Field(default="PropertyValue", alias="@type")
    property_id: str = Field(..., alias="propertyID", description="Property identifier")
    value: str = Field(..., description="Property value")


class ScholarlyArticle(BaseModel):
    """Scholarly article citation."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ScholarlyArticle"] = Field(default="ScholarlyArticle", alias="@type")
    identifier: Optional[Dict[str, Any]] = Field(
        None, description="Article identifier (e.g., DOI)"
    )
    name: Optional[str] = Field(None, description="Article title")
