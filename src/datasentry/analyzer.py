import pandas as pd
from dataclasses import dataclass

@dataclass
class AnalysisReport:
    total_rows: int
    total_columns: int
    missing_values: int
    duplicate_records: int
    invalid_dates: int
    average_amount: float | None

def analyze_dataset(df: pd.DataFrame) -> AnalysisReport:
    def calculate_average_amount() -> float | None:
        if "amount" in df.columns:
            return df["amount"].mean()
        return None

    average_amount = calculate_average_amount()

    return AnalysisReport(
        total_rows=int(len(df)),
        total_columns=int(len(df.columns)),
        missing_values=int(df.isnull().sum().sum()),
        duplicate_records=int(
            df.duplicated(
                subset=["customer", "amount", "date", "status"]
            ).sum()
        ),
        invalid_dates=int(
            pd.to_datetime(
                df["date"], errors="coerce"
            ).isna().sum()
        ),
        average_amount=(
            float(average_amount)
            if average_amount is not None
            else None
        )
    )