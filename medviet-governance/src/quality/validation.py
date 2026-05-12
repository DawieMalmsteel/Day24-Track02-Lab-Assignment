# src/quality/validation.py
import pandas as pd

try:
    import great_expectations as gx
    from great_expectations.core.expectation_suite import ExpectationSuite
except Exception:  # pragma: no cover
    gx = None
    ExpectationSuite = object


def build_patient_expectation_suite() -> ExpectationSuite:
    """Tạo expectation suite cho anonymized patient data."""
    if gx is None:
        raise RuntimeError("great_expectations is not available in this Python environment")

    context = gx.get_context()
    try:
        suite = context.add_expectation_suite("patient_data_suite")
    except Exception:
        suite = context.get_expectation_suite("patient_data_suite")

    df = pd.read_csv("data/raw/patients_raw.csv")
    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("patient_id")
    validator.expect_column_value_lengths_to_equal(column="cccd", value=12)
    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem", min_value=0, max_value=50
    )

    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(column="benh", value_set=valid_conditions)
    validator.expect_column_values_to_match_regex(
        column="email", regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    validator.expect_column_values_to_be_unique(column="patient_id")

    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    """Validate anonymized data."""
    df = pd.read_csv(filepath)
    results = {
        "success": True,
        "failed_checks": [],
        "stats": {"total_rows": len(df), "columns": list(df.columns)},
    }

    if "cccd" in df.columns and df["cccd"].astype(str).str.fullmatch(r"\d{12}").any():
        results["success"] = False
        results["failed_checks"].append("cccd_still_plain_numeric")

    important_cols = ["patient_id", "ho_ten", "cccd", "so_dien_thoai", "email", "benh"]
    missing_cols = [c for c in important_cols if c in df.columns and df[c].isnull().any()]
    if missing_cols:
        results["success"] = False
        results["failed_checks"].append(f"null_values_in:{','.join(missing_cols)}")

    original_df = pd.read_csv("data/raw/patients_raw.csv")
    if len(df) != len(original_df):
        results["success"] = False
        results["failed_checks"].append("row_count_mismatch")

    return results
