import base64
import os
import pytest
import pytest_html
from pytest_metadata.plugin import metadata_key
from datetime import datetime

def pytest_html_report_title(report):
    report.title = "Pytest HTML Report Example"

def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Pytest With Eric"


LOG_FILE = "../logs/run_log.txt"


def write_log(message: str):
    os.makedirs("../logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        test_name = item.name
        status = "PASSED" if report.passed else "FAILED"
        driver = item.funcargs.get("driver", None)
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            img_name = f"{test_name}_{status}.png"
            screenshot_path = f"screenshots/{img_name}"
            driver.save_screenshot(screenshot_path)
            with open(screenshot_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            extras.append(pytest_html.extras.png(encoded_string, name="Screenshot"))
        report.extras = extras