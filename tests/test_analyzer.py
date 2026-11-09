import pandas as pd

from datasentry.analyzer import analyze_dataset


def test_analyze_dataset():

    data = {
        "id": [1, 2, 3],
        "customer": ["Alice", "Bob", "Alice"],
        "amount": [100.0, 200.0, 100.0],
        "date": ["2026-10-01", "2026-10-02", "2026-10-01"],
        "status": ["PAID", "PENDING", "PAID"]
    }

    df = pd.DataFrame(data)

    report = analyze_dataset(df)

    assert report.total_rows == 3
    assert report.total_columns == 5
    assert report.duplicate_records == 1
    assert report.average_amount == 400 / 3

def test_detect_missing_values():
    data = {
        "id": [1, 2],
        "customer": ["Alice", None],
        "amount": [100.0, 200.0],
        "date": ["2026-10-01", "2026-10-02"],
        "status": ["PAID", "PENDING"]
    }

    df = pd.DataFrame(data)

    report = analyze_dataset(df)

    assert report.missing_values == 1

def test_detect_invalid_dates():
    data = {
        "id": [1, 2],
        "customer": ["Alice", "Bob"],
        "amount": [100.0, 200.0],
        "date": ["2026-10-01", "INVALID_DATE"],
        "status": ["PAID", "PENDING"]
    }

    df = pd.DataFrame(data)

    report = analyze_dataset(df)

    assert report.invalid_dates == 1

def test_no_duplicates():
    data = {
        "id": [1, 2],
        "customer": ["Alice", "Bob"],
        "amount": [100.0, 200.0],
        "date": ["2026-10-01", "2026-10-02"],
        "status": ["PAID", "PENDING"]
    }

    df = pd.DataFrame(data)

    report = analyze_dataset(df)

    assert report.duplicate_records == 0