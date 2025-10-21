# RAP Specification Examples

This directory contains example data products that conform to the RAP specification schemas.

## Examples

### Relaxometry MRI

[`relaxometry-mri/product-sub-01-t1-ses-01-gm.jsonld`](relaxometry-mri/product-sub-01-t1-ses-01-gm.jsonld)

A complete example of an MRI relaxometry research product demonstrating:
- T1 relaxation time measurement in gray matter
- Full participant demographic data
- Detailed MRI acquisition parameters (3T Siemens Prisma, MP2RAGE sequence)
- Complete processing provenance chain (5 steps)
- Vector data with 50 sample values (actual datasets would contain full arrays)
- Quality metrics, licensing, and citation information

**Note**: The `values` array in the data section shows only 50 sample values for readability. In a real research product, this would contain all 2,847 values as indicated by the statistics.

### Timeseries

Placeholder for future timeseries examples.

## Validation

Examples should validate against their corresponding JSON Schemas:
- Use a JSON Schema validator supporting draft 2020-12
- Validate against the ResearchProduct schema: `schemas/v1/research-product.json`
- JSON-LD contexts are provided separately in `schemas/v1/measurements/` for semantic validation

## Creating New Examples

When creating new examples:
1. Conform to the appropriate schema in `schemas/v1/`
2. Include complete `@context` references (main context + measurement-specific context)
3. Provide realistic data and comprehensive metadata
4. Include full provenance information with software versions
5. Add quality metrics and licensing information
6. Use QUDT URIs for units when available
