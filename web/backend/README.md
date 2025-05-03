# Backend

## Dev
To run server local:
```bash
PYTHONPATH=src uvicorn src.main:app --host 0.0.0.0 --port 8000
```

To do curl test:
```bash
curl "http://localhost:8000/unemployment?year=1991&month=11"
```

## Bugs

```
ERROR - Error fetching unemployment data: [NUM_COLUMNS_MISMATCH] UNION can only be performed on inputs with the same number of columns, but the first input has 3 columns and the 9th input has 0 columns.;
```
