"""
Data Cleaning & Reporting Automation
Run: python main.py
Reads data/messy_student_data.csv, cleans it, and creates a cleaned CSV,
a text summary, and charts in the output/ folder.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "data" / "messy_student_data.csv"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT}")

    raw = pd.read_csv(INPUT)
    original_rows = len(raw)
    original_missing = int(raw.isna().sum().sum())

    # Standardize column names and text values
    raw.columns = [c.strip().lower().replace(" ", "_") for c in raw.columns]
    for col in raw.select_dtypes(include="object").columns:
        raw[col] = raw[col].astype("string").str.strip()

    # Remove duplicate records
    raw = raw.drop_duplicates()

    # Convert numeric columns safely
    numeric_cols = ["attendance_percent", "assignment_score", "study_hours_per_week"]
    for col in numeric_cols:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")

    # Treat impossible values as missing
    raw.loc[~raw["attendance_percent"].between(0, 100), "attendance_percent"] = pd.NA
    raw.loc[~raw["assignment_score"].between(0, 100), "assignment_score"] = pd.NA
    raw.loc[raw["study_hours_per_week"] < 0, "study_hours_per_week"] = pd.NA

    # Fill missing numeric values with each column's median
    for col in numeric_cols:
        median = raw[col].median()
        if pd.notna(median):
            raw[col] = raw[col].fillna(median)

    # Normalize category values and recompute status based on assignment score
    raw["department"] = raw["department"].str.upper()
    raw["status"] = raw["assignment_score"].apply(
        lambda score: "Pass" if score >= 50 else "Fail"
    )

    cleaned_path = OUT / "cleaned_student_data.csv"
    raw.to_csv(cleaned_path, index=False)

    # Generate automated summary report
    report_lines = [
        "DATA CLEANING & REPORTING AUTOMATION",
        "=" * 42,
        f"Rows in original file: {original_rows}",
        f"Duplicate rows removed: {original_rows - len(pd.read_csv(INPUT).drop_duplicates())}",
        f"Missing cells in original file: {original_missing}",
        f"Rows in cleaned file: {len(raw)}",
        "",
        "KEY METRICS",
        "-" * 42,
        f"Average attendance (%): {raw['attendance_percent'].mean():.1f}",
        f"Average assignment score: {raw['assignment_score'].mean():.1f}",
        f"Average study hours/week: {raw['study_hours_per_week'].mean():.1f}",
        "",
        "STUDENTS BY DEPARTMENT",
        "-" * 42,
    ]
    report_lines.extend([f"{dept}: {count}" for dept, count in raw["department"].value_counts().sort_index().items()])
    report_lines += ["", "PASS / FAIL SUMMARY", "-" * 42]
    report_lines.extend([f"{status}: {count}" for status, count in raw["status"].value_counts().sort_index().items()])
    (OUT / "summary_report.txt").write_text("\n".join(report_lines), encoding="utf-8")

    # Create chart: average assignment score by department
    score_by_dept = raw.groupby("department")["assignment_score"].mean().sort_index()
    plt.figure(figsize=(8, 5))
    score_by_dept.plot(kind="bar")
    plt.title("Average Assignment Score by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(OUT / "average_score_by_department.png", dpi=150)
    plt.close()

    # Create chart: pass/fail counts
    status_counts = raw["status"].value_counts().sort_index()
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind="bar")
    plt.title("Pass / Fail Summary")
    plt.xlabel("Status")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(OUT / "pass_fail_summary.png", dpi=150)
    plt.close()

    print("Done! Cleaned data, report, and charts are saved in the output/ folder.")

if __name__ == "__main__":
    main()
