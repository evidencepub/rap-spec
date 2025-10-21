"""MRI relaxometry measurement schema."""

from typing import List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field
from rap_spec.measurements.base import BaseMeasurement
from rap_spec.models.common import Unit


class SpatialResolution(BaseModel):
    """Spatial resolution of the measurement."""

    model_config = ConfigDict(populate_by_name=True)

    value: float = Field(..., ge=0, description="Resolution value")
    unit: Unit = Field(..., description="Unit of spatial resolution")


class FieldStrength(BaseModel):
    """Magnetic field strength."""

    model_config = ConfigDict(populate_by_name=True)

    value: float = Field(..., ge=0, description="Field strength value")
    unit: Unit = Field(..., description="Field strength unit")


class AcquisitionParameters(BaseModel):
    """MRI acquisition parameters."""

    model_config = ConfigDict(populate_by_name=True)

    field_strength: Optional[FieldStrength] = Field(
        None, alias="fieldStrength", description="Magnetic field strength"
    )
    scanner: Optional[str] = Field(None, description="Scanner manufacturer and model")
    sequence: Optional[str] = Field(None, description="MRI pulse sequence used")
    TR: Optional[float] = Field(None, ge=0, description="Repetition time in ms")
    TE: Optional[Union[float, List[float]]] = Field(
        None, description="Echo time(s) in ms"
    )
    TI: Optional[Union[float, List[float]]] = Field(
        None, description="Inversion time(s) in ms"
    )
    flip_angle: Optional[float] = Field(
        None,
        alias="flipAngle",
        ge=0,
        le=180,
        description="Flip angle in degrees",
    )


class RelaxometryMRIMeasurement(BaseMeasurement):
    """Measurement schema for MRI relaxometry data.

    Extends BaseMeasurement with MRI-specific fields.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://rap-spec.evidencepub.io/v1/schemas/measurements/relaxometry-mri.json",
        },
    )

    measurement_type: Literal["relaxometry_mri"] = Field(
        default="relaxometry_mri",
        alias="measurementType",
        description="Type of measurement",
    )
    specific_measure: str = Field(
        ...,
        alias="specificMeasure",
        description="Specific relaxometry measure",
        examples=["t1_relaxation_time", "t2_relaxation_time", "t2star_relaxation_time"],
    )
    anatomical_region: Optional[str] = Field(
        None,
        alias="anatomicalRegion",
        description="Anatomical region measured",
        examples=["gray_matter", "white_matter", "hippocampus", "cortex"],
    )
    region_type: Optional[Literal["tissue_class", "anatomical_roi", "functional_roi", "voxel_wise"]] = Field(
        None,
        alias="regionType",
        description="Type of region definition",
    )
    vector_length: Optional[int] = Field(
        None,
        alias="vectorLength",
        ge=1,
        description="Number of values in the measurement vector",
    )
    spatial_resolution: Optional[SpatialResolution] = Field(
        None,
        alias="spatialResolution",
        description="Spatial resolution of the measurement",
    )
    coordinate_system: Optional[str] = Field(
        None,
        alias="coordinateSystem",
        description="Coordinate system used",
        examples=["MNI152", "Talairach", "native"],
    )
    acquisition_parameters: Optional[AcquisitionParameters] = Field(
        None,
        alias="acquisitionParameters",
        description="MRI acquisition parameters",
    )
