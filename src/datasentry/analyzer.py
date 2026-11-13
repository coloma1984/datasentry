from dataclasses import dataclass

import pandas as pd


@dataclass
class AnalysisReport:
    total_rows: int
    total_columns: int
    missing_values: int
    duplicate_records: int
    invalid_dates: int
    average_amount: float | None


def analyze_dataset(
    df: pd.DataFrame,
    duplicate_subset: list[str] | None = None,
) -> AnalysisReport:
    """
    Analyze a dataset and return basic data quality metrics.

    By default, duplicate detection considers all columns.
    A custom subset can be provided to identify business duplicates.
    """

    if duplicate_subset is not None:
        missing_columns = set(duplicate_subset) - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Duplicate subset contains unknown columns: "
                f"{sorted(missing_columns)}"
            )

    duplicate_records = int(
        df.duplicated(subset=duplicate_subset).sum()
    )

    missing_values = int(df.isna().sum().sum())

    invalid_dates = 0

    if "date" in df.columns:
        date_values = df["date"].dropna()

        invalid_dates = int(
            pd.to_datetime(
                date_values,
                errors="coerce"
            ).isna().sum()
        )

    average_amount = None

    if "amount" in df.columns:
        numeric_amounts = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).dropna()

        if not numeric_amounts.empty:
            average_amount = float(numeric_amounts.mean())

    return AnalysisReport(
        total_rows=int(len(df)),
        total_columns=int(len(df.columns)),
        missing_values=missing_values,
        duplicate_records=duplicate_records,
        invalid_dates=invalid_dates,
        average_amount=average_amount,
    )
