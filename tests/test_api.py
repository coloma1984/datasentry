from fastapi.testclient import TestClient
import uuid
from datasentry.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_empty_file():
    response = client.post(
        "/analyze",
        files={"file": ("empty.csv", b"", "text/csv")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"


def test_upload_invalid_extension():
    response = client.post(
        "/analyze",
        files={"file": ("document.pdf", b"fake content", "application/pdf")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are supported"


def test_upload_missing_columns():
    csv_content = (
        b"id,customer,amount,date\n"
        b"1,Alice,100,2026-10-01\n"
    )

    response = client.post(
        "/analyze",
        files={"file": ("invalid.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 422
    assert response.json()["detail"]["missing_columns"] == ["status"]


def test_download_report():
    csv_content = (
        b"id,customer,amount,date,status\n"
        b"1,Alice,100,2026-10-01,PAID\n"
        b"2,Bob,200,2026-10-02,PENDING\n"
    )

    response = client.post(
        "/analyze/download",
        files={
            "file": ("transactions.csv", csv_content, "text/csv")
        }
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "attachment" in response.headers["content-disposition"]

    report = response.json()

    assert report["total_rows"] == 2
    assert report["total_columns"] == 5


def test_upload_file_too_large():
    large_content = b"a" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/analyze",
        files={
            "file": (
                "large.csv",
                large_content,
                "text/csv"
            )
        }
    )

    assert response.status_code == 413

    assert response.json()["detail"] == (
        "File exceeds maximum allowed size of 10 MB"
    )


def test_correlation_id_from_request():
    response = client.get(
        "/health",
        headers={"X-Correlation-ID": "test-123"}
    )

    assert response.status_code == 200
    assert response.headers["x-correlation-id"] == "test-123"


def test_correlation_id_generated():
    response = client.get("/health")

    assert response.status_code == 200

    correlation_id = response.headers["x-correlation-id"]

    assert correlation_id is not None

    # Check that the generated ID is a valid UUID
    uuid.UUID(correlation_id)
