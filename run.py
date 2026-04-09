import pytest
import os

def run_tests():
    html_report = "/home/ashok/Desktop/PW-Playwright/report.html"
    os.makedirs(os.path.dirname(html_report), exist_ok=True)

    pytest.main([
        "tests",
        # HTML report
        f"--html={html_report}", 
        "--self-contained-html",
        # RETRIES (GLOBAL)
        "--reruns", "4",              # retry failed tests 2 times
        "--reruns-delay", "6",        # wait 2 seconds before retry
        # Output
        "--capture=tee-sys",
        "-v"
        # keep parallel OFF until suite is 100% stable
        # "-n", "2",
        # "--dist=loadscope",
    ])

if __name__ == "__main__":
    run_tests()
