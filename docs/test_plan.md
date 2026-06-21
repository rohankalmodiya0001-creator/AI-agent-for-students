# Test Plan

## Unit Tests

- Validate resume parsing and text extraction.
- Validate job description entity extraction.
- Validate skill gap score calculations.
- Validate roadmap generation.
- Validate evaluation scoring.
- Validate memory persistence.

## Integration Tests

- Resume upload to skill gap analysis end-to-end.
- Mock interview question generation and evaluation flow.
- Knowledge base ingestion and retrieval.

## Test Commands

```powershell
pytest
```

## Notes

- Add `tests` folder with unit and integration test cases.
- Use `httpx` to test FastAPI endpoints.
