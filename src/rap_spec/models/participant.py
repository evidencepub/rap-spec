"""Participant schema."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class Age(BaseModel):
    """Age information."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["QuantityValue"] = Field(default="QuantityValue", alias="@type")
    value: float = Field(..., ge=0, description="Age value")
    unit: str = Field(default="YR", description="Unit of age (typically YR for years)")


class DemographicData(BaseModel):
    """Demographic and experimental group information."""

    model_config = ConfigDict(populate_by_name=True)

    age: Optional[Age] = Field(None, description="Participant age")
    sex: Optional[Literal["M", "F", "other", "unknown"]] = Field(
        None, description="Biological sex"
    )
    gender: Optional[str] = Field(None, description="Gender identity")
    group: Optional[str] = Field(
        None,
        description="Experimental group assignment",
        examples=["experimental", "control", "treatment_a", "treatment_b"],
    )
    ethnicity: Optional[str] = Field(None, description="Self-reported ethnicity")
    handedness: Optional[Literal["left", "right", "ambidextrous", "unknown"]] = Field(
        None, description="Handedness"
    )
    species: Optional[str] = Field(
        default="human",
        description="Species (for animal studies)",
        examples=["human", "mouse", "rat", "monkey"],
    )
    strain: Optional[str] = Field(
        None,
        description="Genetic strain (for animal studies)",
        examples=["C57BL/6J", "Sprague-Dawley"],
    )
    genetic_modification: Optional[str] = Field(
        None,
        alias="geneticModification",
        description="Genetic modifications (for animal studies)",
    )


class Medication(BaseModel):
    """Medication history entry."""

    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, description="Medication name")
    dosage: Optional[str] = Field(None, description="Dosage")
    duration: Optional[str] = Field(None, description="Duration of use")


class Assessment(BaseModel):
    """Clinical assessment entry."""

    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, description="Assessment name")
    score: Optional[float] = Field(None, description="Assessment score")
    date: Optional[str] = Field(None, description="Assessment date")


class ClinicalData(BaseModel):
    """Clinical or health-related information."""

    model_config = ConfigDict(populate_by_name=True)

    diagnosis: Optional[List[str]] = Field(None, description="Clinical diagnoses")
    medication_history: Optional[List[Medication]] = Field(
        None, alias="medicationHistory", description="Medication history"
    )
    assessments: Optional[List[Assessment]] = Field(
        None, description="Clinical assessment scores"
    )


class ProductsAvailable(BaseModel):
    """Summary of available data products for this participant."""

    model_config = ConfigDict(populate_by_name=True)

    count: Optional[int] = Field(None, ge=0, description="Total number of products")
    measures: Optional[List[str]] = Field(
        None, description="Types of measurements available"
    )
    sessions: Optional[List[str]] = Field(None, description="Sessions with data")
    by_measure: Optional[Dict[str, int]] = Field(
        None,
        alias="byMeasure",
        description="Product counts by measurement type",
    )
    by_session: Optional[Dict[str, int]] = Field(
        None,
        alias="bySession",
        description="Product counts by session",
    )


class SessionDuration(BaseModel):
    """Session duration."""

    model_config = ConfigDict(populate_by_name=True)

    value: Optional[float] = Field(None, description="Duration value")
    unit: str = Field(default="MIN", description="Duration unit")


class Environment(BaseModel):
    """Environmental conditions."""

    model_config = ConfigDict(populate_by_name=True)

    temperature: Optional[float] = Field(None, description="Temperature")
    lighting: Optional[str] = Field(None, description="Lighting conditions")
    noise_level: Optional[str] = Field(
        None, alias="noiseLevel", description="Noise level"
    )


class SessionMetadata(BaseModel):
    """Metadata about an experimental session."""

    model_config = ConfigDict(populate_by_name=True)

    session: Optional[str] = Field(None, description="Session identifier")
    date: Optional[str] = Field(None, description="Session date")
    duration: Optional[SessionDuration] = Field(None, description="Session duration")
    notes: Optional[str] = Field(None, description="Session notes")
    experimenter: Optional[str] = Field(None, description="Experimenter name")
    environment: Optional[Environment] = Field(
        None, description="Environmental conditions"
    )


class Links(BaseModel):
    """Links to related resources."""

    model_config = ConfigDict(populate_by_name=True)

    products: Optional[HttpUrl] = Field(
        None, description="Link to all products for this participant"
    )
    measures: Optional[HttpUrl] = Field(None, description="Link to available measures")
    sessions: Optional[HttpUrl] = Field(None, description="Link to session metadata")


class Consent(BaseModel):
    """Information about consent and data sharing."""

    model_config = ConfigDict(populate_by_name=True)

    consent_date: Optional[str] = Field(
        None, alias="consentDate", description="Consent date"
    )
    consent_version: Optional[str] = Field(
        None, alias="consentVersion", description="Version of consent form used"
    )
    data_sharing: Optional[Literal["public", "restricted", "private"]] = Field(
        None, alias="dataSharing", description="Level of data sharing permitted"
    )
    restrictions: Optional[List[str]] = Field(
        None, description="Specific restrictions on data use"
    )


class Participant(BaseModel):
    """A research participant with associated demographic data and available products.

    Contains demographic information, clinical data, consent information,
    and summaries of available data products.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/participant.json",
        },
    )

    context: Union[Literal["https://rap-spec.evidencepub.io/v1/context"], Dict[str, Any]] = Field(
        ..., alias="@context"
    )
    type_: Literal["Participant"] = Field(default="Participant", alias="@type")
    id_: HttpUrl = Field(..., alias="@id", description="Unique URI for this participant")
    identifier: str = Field(
        ...,
        description="Participant ID (e.g., sub-01, P001)",
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    demographic_data: Optional[DemographicData] = Field(
        None,
        alias="demographicData",
        description="Demographic and experimental group information",
    )
    enrollment_date: Optional[str] = Field(
        None,
        alias="enrollmentDate",
        description="Date participant was enrolled in study",
    )
    status: Optional[Literal["active", "completed", "withdrawn", "excluded"]] = Field(
        None, description="Current participation status"
    )
    exclusion_reason: Optional[str] = Field(
        None,
        alias="exclusionReason",
        description="Reason for exclusion if status is 'excluded'",
    )
    clinical_data: Optional[ClinicalData] = Field(
        None,
        alias="clinicalData",
        description="Clinical or health-related information",
    )
    products_available: Optional[ProductsAvailable] = Field(
        None,
        alias="productsAvailable",
        description="Summary of available data products for this participant",
    )
    session_metadata: Optional[List[SessionMetadata]] = Field(
        None,
        alias="sessionMetadata",
        description="Metadata about each experimental session",
    )
    links: Optional[Links] = Field(None, description="Links to related resources")
    consent: Optional[Consent] = Field(
        None, description="Information about consent and data sharing"
    )
    privacy_level: Optional[Literal["anonymous", "pseudonymous", "identifiable"]] = Field(
        default="pseudonymous",
        alias="privacyLevel",
        description="Level of privacy protection",
    )
