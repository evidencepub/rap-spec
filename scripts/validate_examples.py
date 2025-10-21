#!/usr/bin/env python3
"""
Validate example data files using Pydantic models.

This script validates all example JSON-LD files against their corresponding
Pydantic models to ensure the examples conform to the specification.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

from rap_spec.models.research_product import ResearchProduct


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load a JSON/JSON-LD file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_research_product(file_path: Path) -> bool:
    """
    Validate a research product example file.

    Args:
        file_path: Path to the JSON-LD file

    Returns:
        True if valid, False otherwise
    """
    try:
        data = load_json_file(file_path)
        # Validate using Pydantic
        product = ResearchProduct.model_validate(data)
        print(f"✓ Valid: {file_path.name}")
        return True
    except Exception as e:
        print(f"✗ Invalid: {file_path.name}")
        print(f"  Error: {e}")
        return False


def main() -> int:
    """Validate all example files."""
    repo_root = Path(__file__).parent.parent
    examples_dir = repo_root / "examples"

    print("Validating example files using Pydantic models...\n")

    # Find all .jsonld files
    example_files = list(examples_dir.rglob("*.jsonld"))

    if not example_files:
        print("⚠ No example files found")
        return 1

    valid_count = 0
    invalid_count = 0

    for example_file in sorted(example_files):
        # Determine type based on file content or location
        if validate_research_product(example_file):
            valid_count += 1
        else:
            invalid_count += 1

    print(f"\n{'='*60}")
    print(f"Results: {valid_count} valid, {invalid_count} invalid")
    print(f"{'='*60}")

    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
