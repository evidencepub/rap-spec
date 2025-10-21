"""Timeseries measurement schema."""

from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field
from rap_spec.measurements.base import BaseMeasurement
from rap_spec.models.common import Unit


class TimeDimension(BaseModel):
    """Time dimension information."""

    model_config = ConfigDict(populate_by_name=True)

    length: int = Field(..., ge=1, description="Number of time points")
    start: Optional[float] = Field(None, description="Start time")
    end: Optional[float] = Field(None, description="End time")


class Dimensions(BaseModel):
    """Dimensions of the timeseries data."""

    model_config = ConfigDict(populate_by_name=True)

    time: Optional[TimeDimension] = Field(None, description="Time dimension information")


class SamplingRate(BaseModel):
    """Sampling rate of the timeseries."""

    model_config = ConfigDict(populate_by_name=True)

    value: float = Field(..., gt=0, description="Sampling rate value")
    unit: Unit = Field(..., description="Sampling rate unit")


class Duration(BaseModel):
    """Total duration of the timeseries."""

    model_config = ConfigDict(populate_by_name=True)

    value: float = Field(..., ge=0, description="Duration value")
    unit: Unit = Field(..., description="Duration unit")


class Channels(BaseModel):
    """Channel information for multi-channel timeseries."""

    model_config = ConfigDict(populate_by_name=True)

    count: int = Field(..., ge=1, description="Number of channels")
    type_: Optional[str] = Field(None, alias="type", description="Type of channels")
    labels: Optional[List[str]] = Field(None, description="Labels for each channel")


class TimeseriesMeasurement(BaseMeasurement):
    """Measurement schema for timeseries data.

    Extends BaseMeasurement with timeseries-specific fields.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/measurements/timeseries.json",
        },
    )

    measurement_type: Literal["timeseries"] = Field(
        default="timeseries",
        alias="measurementType",
        description="Type of measurement",
    )
    specific_measure: str = Field(
        ...,
        alias="specificMeasure",
        description="Specific timeseries measure",
        examples=["calcium_imaging", "eeg", "ecg", "behavioral_response", "neural_activity"],
    )
    dimensions: Optional[Dimensions] = Field(
        None,
        description="Dimensions of the timeseries data",
    )
    sampling_rate: Optional[SamplingRate] = Field(
        None,
        alias="samplingRate",
        description="Sampling rate of the timeseries",
    )
    duration: Optional[Duration] = Field(
        None,
        description="Total duration of the timeseries",
    )
    channels: Optional[Channels] = Field(
        None,
        description="Channel information for multi-channel timeseries",
    )
