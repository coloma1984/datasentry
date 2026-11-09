import pandas as pd

from datasentry.analyzer import analyze_dataset


def main() -> None:
    filename = "data/transactions.csv"

    df = pd.read_csv(filename)

    report = analyze_dataset(df)

    print("Welcome to DataSentry!")
    print("\nAnalysis report:")
    print(f"Total rows: {report.total_rows}")
    print(f"Total columns: {report.total_columns}")
    print(f"Missing values: {report.missing_values}")
    print(f"Business duplicates: {report.duplicate_records}")
    print(f"Invalid dates: {report.invalid_dates}")
    print(f"Average amount: {report.average_amount:.2f}")


if __name__ == "__main__":
    main()