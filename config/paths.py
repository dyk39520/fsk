"""项目路径配置。"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"
HTML_REPORT_PATH = REPORTS_DIR / "report.html"
ALLURE_REPORT_DIR = REPORTS_DIR / "allure-report"
