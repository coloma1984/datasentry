# DataSentry

**Automated Data Quality Analyzer**

DataSentry is a Python-based REST API designed to analyze CSV datasets and identify common data quality issues before they impact downstream processes.

It provides automated data profiling, data validation and structured diagnostic reports through a lightweight API.

## Key Features

- **Data profiling:** Extract dataset statistics, including total rows and columns.
- **Missing values:** Identify null and missing values.
- **Duplicate detection:** Detect duplicated business records.
- **Date validation:** Identify invalid date values.
- **Numeric analysis:** Calculate the average transaction amount.
- **Schema validation:** Ensure required columns are present.
- **File validation:** Validate file extensions, encoding, content and maximum upload size.
- **Diagnostic reports:** Generate structured JSON analysis reports.
- **Correlation IDs:** Track API requests through structured logging.
- **API documentation:** Automatically generated OpenAPI documentation.
- **Docker support:** Run the application in a containerized environment.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Core programming language |
| FastAPI | REST API framework |
| Pydantic | Data validation and response schemas |
| Pandas | Data processing and analysis |
| Uvicorn | ASGI server |
| Pytest | Automated testing |
| Docker | Containerization |

## Project Structure

```text
datasentry/
│
├── src/
│   └── datasentry/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── api.py
│       └── main.py
│
├── tests/
│   ├── test_analyzer.py
│   └── test_api.py
│
├── data/
│   ├── transactions.csv
│   ├── empty.csv
│   └── invalid.csv
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.14
- pip
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/datasentry.git
cd datasentry
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

### Running the application

Start the API using Uvicorn:

```bash
uvicorn datasentry.api:app --app-dir src --reload
```

The API will be available at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

OpenAPI specification:

`http://localhost:8000/openapi.json`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/analyze` | Upload and analyze a CSV file |
| POST | `/analyze/download` | Analyze a CSV and download the JSON report |

### CSV Requirements

Uploaded CSV files must:

- Use the `.csv` extension.
- Use UTF-8 encoding.
- Contain the following required columns:
  - `customer`
  - `amount`
  - `date`
  - `status`
- Contain at least one data row.
- Not exceed 10 MB.

### Example Request

Analyze a CSV file using cURL:

```bash
curl -X POST \
  http://localhost:8000/analyze \
  -F "file=@data/transactions.csv"
```

### Example Response

```json
{
  "total_rows": 100,
  "total_columns": 4,
  "missing_values": 3,
  "duplicate_records": 2,
  "invalid_dates": 1,
  "average_amount": 125.50
}
```

The values above are illustrative.

## Docker

Build the Docker image:

```bash
docker build -t datasentry:1.0 .
```

Run the container:

```bash
docker run -d \
  --name datasentry-api \
  -p 8000:8000 \
  datasentry:1.0
```

Check application logs:

```bash
docker logs datasentry-api
```

Stop the container:

```bash
docker stop datasentry-api
```

Remove the container:

```bash
docker rm datasentry-api
```

## Running Tests

Execute the automated test suite:

```bash
pytest -v
```

The project currently includes 12 automated tests covering:

- Dataset analysis.
- Missing value detection.
- Invalid date detection.
- Duplicate detection.
- API health checks.
- File upload validation.
- Missing required columns.
- JSON report generation.
- Maximum file size validation.
- Correlation ID handling.

## Architecture

DataSentry follows a modular architecture separating HTTP handling from data analysis responsibilities.

**API Layer (`api.py`)**

Handles HTTP requests, CSV uploads, input validation, error handling and JSON responses.

**Analysis Layer (`analyzer.py`)**

Contains the core data quality analysis logic, including missing value detection, duplicate identification, date validation and numerical aggregation.

**Application Entry Point (`main.py`)**

Provides a standalone entry point for running dataset analysis.

This separation improves maintainability, testability and extensibility.

## Future Improvements

Potential extensions include:

- Excel file support.
- Configurable data quality rules.
- Advanced statistical anomaly detection.
- AI-powered diagnostic recommendations.
- Historical analysis and data quality trends.
- Web-based user interface.

## License

This project is currently under development.