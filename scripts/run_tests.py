"""运行测试并生成 HTML / Allure 报告。"""

import shutil
import subprocess
import sys

from config import ALLURE_REPORT_DIR, ALLURE_RESULTS_DIR, HTML_REPORT_PATH


def has_allure_plugin():
    """检查当前环境是否安装了 allure-pytest。"""
    try:
        import allure  # noqa: F401
        return True
    except ImportError:
        return False


def main():
    """执行 pytest，并在环境允许时生成 Allure 报告。"""
    HTML_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    command = [sys.executable, "-m", "pytest", *sys.argv[1:]]
    if has_allure_plugin():
        command.extend(["--alluredir", str(ALLURE_RESULTS_DIR)])

    return_code = subprocess.call(command)

    allure_cli = shutil.which("allure")
    if has_allure_plugin() and allure_cli:
        ALLURE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.call([
            allure_cli,
            "generate",
            str(ALLURE_RESULTS_DIR),
            "-o",
            str(ALLURE_REPORT_DIR),
            "--clean",
        ])
    elif has_allure_plugin():
        print("已生成 Allure 结果，但未找到 Allure CLI，跳过 Allure HTML 报告。")
    else:
        print("未安装 allure-pytest，跳过 Allure 结果收集。")

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
