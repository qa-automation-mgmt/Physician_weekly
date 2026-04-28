import pytest
import os
from datetime import datetime


def run_tests():

    # ── Timestamped report folder ──────────────────────
    # FIXED: format now matches conftest.py exactly (%Y_%m_%d_%H_%M_%S)
    # Previously used %d_%m_%Y which created a DIFFERENT folder name than
    # conftest.py, so HTML went into one folder and Excel/screenshots into another.
    run_time      = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    report_folder = f"reports/Run_{run_time}"
    html_report    = f"{report_folder}/PW_Report.html"

    os.makedirs(report_folder, exist_ok=True)

    # ── Run pytest ─────────────────────────────────────
    pytest.main([
        "tests",
        f"--html={html_report}",
        "--self-contained-html",
        "--reruns",       "4",       # retry failed tests 4 times
        "--reruns-delay", "4",       # wait 4 seconds before retry
        "--capture=tee-sys",
        "-v",
    ])

    # ── Print paths ────────────────────────────────────
    excel_path = f"{report_folder}/PW_Execution_Report.xlsx"
    print("\n" + "=" * 60)
    print("  PROJECT     : Physician Weekly")
    print("  TESTER      : Ashok Kumar")
    print(f"  RUN TIME    : {run_time}")
    print("-" * 60)
    print(f"  HTML Report   : {html_report}")
    print(f"  Excel Report  : {excel_path}")
    print(f"  Screenshots   : {report_folder}/screenshots/")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()