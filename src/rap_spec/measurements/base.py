"""Base measurement schema for all measurement types."""

from typing import Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from rap_spec.models.common import Unit


class BaseMeasurement(BaseModel):
    """Base schema for all measurement types.

    Domain-specific measurement types should extend this class.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/measurements/base-measurement.json",
        },
    )

    type_: Literal["Measurement"] = Field(
        default="Measurement",
        alias="@type",
        description="Type identifier for measurements",
    )
    measurement_type: str = Field(
        ...,
        alias="measurementType",
        description="Type of measurement (e.g., relaxometry_mri, timeseries)",
    )
    specific_measure: str = Field(
        ...,
        alias="specificMeasure",
        description="Specific measure within the measurement type",
    )
    session: Optional[str] = Field(
        None,
        description="Session identifier for longitudinal studies",
    )
    unit: Optional[Union[Unit, HttpUrl]] = Field(
        None,
        description="Unit of measurement",
    )
    quantity_kind: Optional[HttpUrl] = Field(
        None,
        alias="quantityKind",
        description="QUDT quantity kind URI (e.g., http://qudt.org/vocab/quantitykind/Time)",
    )
