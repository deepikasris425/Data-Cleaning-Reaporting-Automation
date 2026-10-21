# Data Cleaning & Reporting Automation

**Internship Task 4 — Thiranex**

## Project overview
This beginner-friendly Python project automates a small data-cleaning and reporting workflow. It reads a sample student dataset containing missing values, an invalid attendance value, and a duplicate row; cleans the data; and generates a CSV, text summary, and visual charts.

## Features
- Reads a CSV dataset using pandas
- Standardizes column names and text fields
- Removes duplicate rows
- Handles missing and invalid numeric values
- Fills missing numeric values using the column median
- Produces a cleaned CSV file
- Generates an automated text report with key metrics and department/status counts
- Saves charts for average assignment score by department and pass/fail summary

## Project structure
```text
Data_Cleaning_Reporting_Automation/
├── data/
│   └── messy_student_data.csv
├── output/
│   └── (generated files appear here after running)
├── main.py
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.9 or later
- pandas
- matplotlib

## How to run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python main.py
   ```
5. Open the `output` folder to see the cleaned data, report, and charts.

## Output files
- `cleaned_student_data.csv` — cleaned dataset
- `summary_report.txt` — automated summary report
- `average_score_by_department.png` — department score chart
- `pass_fail_summary.png` — pass/fail chart

## Dataset note
The included data is synthetic sample data created for demonstration. It does not contain real student records. The pass/fail status is recalculated using a score threshold of 50 for demonstration purposes.

## Skills demonstrated
Python, pandas, CSV handling, data preprocessing, missing-value treatment, duplicate removal, data validation, automated reporting, and data visualization.

## Author
Deepikasri S  
AI & ML Department  
Rathinam Technical Campus
