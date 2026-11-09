from io import BytesIO

import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from datasentry.analyzer import analyze_dataset


class CorrelationIdFilter(logging.Filter):

    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s - %(levelname)s "
        "[%(correlation_id)s] - %(message)s"
    )
)

logger = logging.getLogger(__name__)
logger.addFilter(CorrelationIdFilter())


correlation_id_var: ContextVar[str] = ContextVar(
    "correlation_id",
    default="unknown"
)


class AnalysisReportResponse(BaseModel):
    total_rows: int
    total_columns: int
    missing_values: int
    duplicate_records: int
    invalid_dates: int
    average_amount: float | None


class CorrelationIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        correlation_id = request.headers.get(
            "X-Correlation-ID",
            str(uuid.uuid4())
        )

        token = correlation_id_var.set(correlation_id)

        try:
            response = await call_next(request)

            response.headers["X-Correlation-ID"] = correlation_id

            return response

        finally:
            correlation_id_var.reset(token)


app = FastAPI(
    title="DataSentry API",
    description="Data quality analysis service",
    version="1.0.0"
)


app.add_middleware(CorrelationIdMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unexpected error processing %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def process_csv(file: UploadFile) -> AnalysisReportResponse:

    if not (file.filename or "").lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    contents = await file.read(MAX_FILE_SIZE + 1)

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    logger.info("CSV upload received: %d bytes", len(contents))

    if len(contents) > MAX_FILE_SIZE:
        logger.warning("CSV upload rejected: file exceeds maximum size")
        raise HTTPException(
            status_code=413,
            detail="File exceeds maximum allowed size of 10 MB"
    )

    try:
        df = pd.read_csv(BytesIO(contents))

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="CSV file has no header or data"
        )

    except pd.errors.ParserError:
        raise HTTPException(
            status_code=400,
            detail="Malformed CSV file"
        )

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV must use UTF-8 encoding"
        )

    required_columns = {
        "customer", "amount", "date", "status"
    }

    missing_columns = sorted(
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Missing required columns",
                "missing_columns": missing_columns
            }
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="CSV contains no data rows"
        )

    report = analyze_dataset(df)

    logger.info(
        "CSV analysis completed: %d rows, %d columns",
        report.total_rows,
        report.total_columns
    )

    return AnalysisReportResponse(**report.__dict__)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisReportResponse)
async def analyze_file(file: UploadFile = File(...)):
    return await process_csv(file)


@app.post("/analyze/download")
async def download_report(file: UploadFile = File(...)):

    report = await process_csv(file)

    json_content = report.model_dump_json(indent=2)

    return StreamingResponse(
        iter([json_content]),
        media_type="application/json",
        headers={
            "Content-Disposition":
                'attachment; filename="datasentry-report.json"'
        }
    )