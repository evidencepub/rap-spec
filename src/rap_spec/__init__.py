"""
Research API Protocol (RAP) Specification

JSON Schema definitions for standardizing research data products, queries, and APIs.
"""

__version__ = "1.0.0"

from rap_spec.models.research_product import ResearchProduct
from rap_spec.models.participant import Participant
from rap_spec.models.collection import ResearchProductCollection
from rap_spec.models.aggregate import AggregateStatistics
from rap_spec.models.api_descriptor import ResearchAPIDescriptor
from rap_spec.measurements.base import BaseMeasurement
from rap_spec.measurements.relaxometry_mri import RelaxometryMRIMeasurement
from rap_spec.measurements.timeseries import TimeseriesMeasurement
from rap_spec.data_types.vector_data import VectorData

__all__ = [
    "ResearchProduct",
    "Participant",
    "ResearchProductCollection",
    "AggregateStatistics",
    "ResearchAPIDescriptor",
    "BaseMeasurement",
    "RelaxometryMRIMeasurement",
    "TimeseriesMeasurement",
    "VectorData",
]
