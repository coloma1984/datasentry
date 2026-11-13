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

    report = analyze_dataset(
        df,
        duplicate_subset=["customer", "amount", "date", "status"],
    )

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


def test_dataset_without_date_column():
    df = pd.DataFrame({
        "product": ["A", "B"],
        "price": [10.0, 20.0]
    })

    report = analyze_dataset(df)

    assert report.invalid_dates == 0
    assert report.average_amount is None


def test_dataset_without_amount_column():
    df = pd.DataFrame({
        "product": ["A", "B"],
        "date": ["2026-10-01", "2026-10-02"]
    })

    report = analyze_dataset(df)

    assert report.average_amount is None


def test_empty_dataset():
    df = pd.DataFrame(columns=["product", "price"])

    report = analyze_dataset(df)

    assert report.total_rows == 0
    assert report.total_columns == 2
    assert report.missing_values == 0
    assert report.duplicate_records == 0
    assert report.average_amount is None


def test_missing_dates_are_not_invalid_dates():
    df = pd.DataFrame({
        "date": ["2026-10-01", None, "INVALID_DATE"]
    })

    report = analyze_dataset(df)

    assert report.missing_values == 1
    assert report.invalid_dates == 1


def test_non_numeric_amount_values():
    df = pd.DataFrame({
        "amount": ["100", "200", "INVALID"]
    })

    report = analyze_dataset(df)

    assert report.average_amount == 150.0


def test_duplicates_across_all_columns():
    df = pd.DataFrame({
        "product": ["A", "B", "A"],
        "price": [10, 20, 10]
    })

    report = analyze_dataset(df)

    assert report.duplicate_records == 1
