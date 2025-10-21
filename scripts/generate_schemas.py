#!/usr/bin/env python3
"""
Generate JSON Schema files from Pydantic models.

This script exports all RAP Pydantic models to JSON Schema 2020-12 format,
preserving exact $id and $schema values for compatibility.
"""

import json
from pathlib import Path
from typing import Any, Dict

# Import all models
from rap_spec.measurements.base import BaseMeasurement
from rap_spec.measurements.relaxometry_mri import RelaxometryMRIMeasurement
from rap_spec.measurements.timeseries import TimeseriesMeasurement
from rap_spec.data_types.vector_data import VectorData
from rap_spec.models.research_product import ResearchProduct
from rap_spec.models.participant import Participant
from rap_spec.models.collection import ResearchProductCollection
from rap_spec.models.aggregate import AggregateStatistics
from rap_spec.models.api_descriptor import ResearchAPIDescriptor


def post_process_schema(schema: Dict[str, Any], schema_id: str) -> Dict[str, Any]:
    """
    Post-process the generated schema to ensure compatibility.

    Args:
        schema: The generated JSON schema
        schema_id: The $id value for this schema

    Returns:
        Post-processed schema
    """
    # Ensure top-level $schema and $id
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = schema_id

    # Remove Pydantic-specific keys that shouldn't be in JSON Schema
    keys_to_remove = ["additionalProperties"]
    for key in keys_to_remove:
        schema.pop(key, None)

    # Set additionalProperties to false for strict validation (except where needed)
    if "properties" in schema:
        # ResearchProduct should have additionalProperties: false
        if "ResearchProduct" in schema.get("title", ""):
            schema["additionalProperties"] = False

    return schema


def generate_schema(model_class: Any, output_path: Path, schema_id: str) -> None:
    """
    Generate JSON Schema for a Pydantic model.

    Args:
        model_class: The Pydantic model class
        output_path: Path to write the schema file
        schema_id: The $id for this schema
    """
    # Generate schema using Pydantic v2 API
    schema = model_class.model_json_schema(
        mode="serialization",
        by_alias=True,
    )

    # Post-process schema
    schema = post_process_schema(schema, schema_id)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write schema file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
        f.write("\n")  # Add trailing newline

    print(f"✓ Generated: {output_path}")


def main() -> None:
    """Generate all JSON schemas."""
    # Base directory
    repo_root = Path(__file__).parent.parent
    schemas_dir = repo_root / "schemas" / "v1"

    print("Generating JSON Schemas from Pydantic models...\n")

    # Measurement schemas
    print("Measurement schemas:")
    generate_schema(
        BaseMeasurement,
        schemas_dir / "measurements" / "base-measurement.json",
        "https://rap-spec.evidencepub.io/v1/schemas/measurements/base-measurement.json",
    )
    generate_schema(
        RelaxometryMRIMeasurement,
        schemas_dir / "measurements" / "relaxometry-mri.json",
        "https://rap-spec.evidencepub.io/v1/schemas/measurements/relaxometry-mri.json",
    )
    generate_schema(
        TimeseriesMeasurement,
        schemas_dir / "measurements" / "timeseries.json",
        "https://rap-spec.evidencepub.io/v1/schemas/measurements/timeseries.json",
    )

    # Data type schemas
    print("\nData type schemas:")
    generate_schema(
        VectorData,
        schemas_dir / "data-types" / "vector-data.json",
        "https://rap-spec.evidencepub.io/v1/schemas/data-types/vector-data.json",
    )

    # Entity schemas
    print("\nEntity schemas:")
    generate_schema(
        ResearchProduct,
        schemas_dir / "research-product.json",
        "https://rap-spec.evidencepub.io/v1/schemas/research-product.json",
    )
    generate_schema(
        Participant,
        schemas_dir / "participant.json",
        "https://rap-spec.evidencepub.io/v1/schemas/participant.json",
    )
    generate_schema(
        ResearchProductCollection,
        schemas_dir / "collection.json",
        "https://rap-spec.evidencepub.io/v1/schemas/collection.json",
    )
    generate_schema(
        AggregateStatistics,
        schemas_dir / "aggregate.json",
        "https://rap-spec.evidencepub.io/v1/schemas/aggregate.json",
    )
    generate_schema(
        ResearchAPIDescriptor,
        schemas_dir / "api-descriptor.json",
        "https://rap-spec.evidencepub.io/v1/schemas/api-descriptor.json",
    )

    print("\n✅ All schemas generated successfully!")
    print(f"   Output directory: {schemas_dir}")


if __name__ == "__main__":
    main()
