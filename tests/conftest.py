"""pytest 全局夹具。"""

import os
import re
import time
from datetime import datetime

import pytest
from selenium.webdriver.common.by import By

from config import LOG_DIR, SCREENSHOTS_DIR, SCREENSHOT_SETTLE_SECONDS
from pages.login_page import PageLogin
from pages.register_page import RegisterPage
from utils.logger import RUN_NUMBER, get_logger
from utils.tools import Tools


logger = get_logger("pytest")
_run_case_labels = {}
FAILURE_MODAL_SELECTORS = (
    ".modal-body",
    ".modal",
    ".swal2-container",
    ".alert",
    "[role=dialog]",
    ".parsley-errors-list li",
    ".form-group-parsley-error",
    ".mobile-error-message",
    ".error-container",
)


def pytest_addoption(parser):
    """添加浏览器参数，便于 Chrome / Firefox 兼容性测试切换。"""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="浏览器类型: chrome 或 firefox",
    )
    parser.addoption(
        "--data-source",
        action="store",
        default=None,
        choices=("auto", "file", "code"),
        help="测试用例数据源: auto=有文件用文件否则用代码，file=只用文件，code=只用代码",
    )


def pytest_configure(config):
    """把 --data-source 转成数据模块可读取的环境变量。"""
    data_source = config.getoption("--data-source")
    if data_source:
        os.environ["TEST_DATA_SOURCE"] = data_source


def _format_case_label(item, index, total):
    """生成带运行序号的用例名称。"""
    module = item.location[0]
    base_name = getattr(item, "originalname", item.name)
    label = f"[{index}/{total}] {module}::{base_name}"
    params = getattr(item, "callspec", None)
    if params is not None and "case" in params.params:
        case = params.params["case"]
        if isinstance(case, dict):
            case_name = case.get("case", "")
        else:
            case_name = str(case)
        if case_name:
            label = f"{label} - {case_name}"
    return label


def pytest_collection_modifyitems(session, config, items):
    """收集用例时缓存可读的用例序号。"""
    total = len(items)
    for index, item in enumerate(items, start=1):
        _run_case_labels[item.nodeid] = _format_case_label(item, index, total)


def pytest_sessionstart(session):
    """标记本次是第几次测试运行。"""
    logger.info("开始第 %s 次测试运行", RUN_NUMBER)


def pytest_sessionfinish(session, exitstatus):
    """测试运行结束后记录运行次数。"""
    logger.info("第 %s 次测试运行结束", RUN_NUMBER)


def pytest_runtest_makereport(item, call):
    """用例失败时自动保存截图。"""
    if call.when != "call" or call.excinfo is None:
        return

    driver = Tools.driver
    if driver is None:
        logger.warning("浏览器驱动不存在，跳过失败截图")
        return

    _save_failure_screenshot(driver, item, "immediate")
    time.sleep(SCREENSHOT_SETTLE_SECONDS)
    _save_failure_screenshot(driver, item, "settled")


def _save_failure_screenshot(driver, item, phase):
    """保存失败现场截图，phase 用于区分过早/过晚两帧。"""
    safe_nodeid = re.sub(r"[^\w.\-]", "_", item.nodeid)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_path = SCREENSHOTS_DIR / f"{safe_nodeid}_{timestamp}_{phase}"
    screenshot_path = base_path.with_suffix(".png")
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        driver.save_screenshot(str(screenshot_path))
        logger.info("失败截图已保存: %s", screenshot_path)
    except Exception as exc:
        logger.error("保存失败截图时发生异常: %s", exc)

    _save_failure_key_elements(driver, base_path)
    _save_failure_dom_evidence(driver, safe_nodeid, timestamp, phase)


def _selector_name(selector):
    """把 CSS 选择器转成适合放进文件名的短名称。"""
    return re.sub(r"[^\w.\-]", "_", selector).strip("_")


def _save_failure_key_elements(driver, base_path):
    """失败时对仍可见的弹窗/错误元素单独截图，便于查看关键提示。"""
    for selector in FAILURE_MODAL_SELECTORS:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception:
            continue
        for index, element in enumerate(elements, start=1):
            try:
                if not element.is_displayed() or not element.text.strip():
                    continue
            except Exception:
                continue
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                    element,
                )
            except Exception:
                pass
            selector_name = _selector_name(selector)
            element_path = base_path.with_name(
                f"{base_path.name}_{selector_name}_{index}_element.png"
            )
            view_path = base_path.with_name(
                f"{base_path.name}_{selector_name}_{index}.png"
            )
            try:
                element.screenshot(str(element_path))
                logger.info("失败关键元素截图已保存: %s", element_path)
            except Exception as exc:
                logger.error("保存失败关键元素截图时发生异常: %s", exc)
            try:
                driver.save_screenshot(str(view_path))
                logger.info("失败关键页面截图已保存: %s", view_path)
            except Exception as exc:
                logger.error("保存失败关键页面截图时发生异常: %s", exc)


def _save_failure_dom_evidence(driver, safe_nodeid, timestamp, phase):
    """失败时保留页面源码和文本证据到 logs，避免污染 screenshots。"""
    base_path = LOG_DIR / f"{safe_nodeid}_{timestamp}_{phase}"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        html_path = base_path.with_name(base_path.name + "_page_source.html")
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception as exc:
        logger.error("保存失败页面源码时发生异常: %s", exc)

    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body_text = body.text.strip()
    except Exception:
        body_text = ""

    modal_texts = _collect_failure_modal_texts(driver)
    try:
        evidence_path = base_path.with_name(base_path.name + "_evidence.txt")
        evidence = (
            f"URL: {driver.current_url}\n"
            f"\nBODY TEXT:\n{body_text}\n"
            f"\nMODAL-LIKE TEXT:\n{modal_texts or '(none)'}\n"
        )
        evidence_path.write_text(evidence, encoding="utf-8")
        logger.info("失败页面证据已保存: %s", evidence_path)
    except Exception as exc:
        logger.error("保存失败页面证据时发生异常: %s", exc)


def _collect_failure_modal_texts(driver):
    """收集弹窗类节点文本，并标注节点当前是否可见。"""
    lines = []
    for selector in FAILURE_MODAL_SELECTORS:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception:
            continue
        for element in elements:
            text = element.text.strip()
            if not text:
                continue
            try:
                state = "visible" if element.is_displayed() else "hidden"
            except Exception:
                state = "unknown"
            lines.append(f"[{selector}][{state}] {text[:500]}")
    return "\n".join(lines)


def pytest_runtest_logstart(nodeid, location):
    """记录用例开始执行。"""
    label = _run_case_labels.get(nodeid, nodeid)
    logger.info("开始用例: %s", label)


def pytest_runtest_logreport(report):
    """记录用例最终结果。"""
    if report.when == "call":
        label = _run_case_labels.get(report.nodeid, report.nodeid)
        if report.passed:
            logger.info("用例通过: %s", label)
        elif report.failed:
            logger.error("用例失败: %s", label)


@pytest.fixture(autouse=True)
def driver(request):
    """为每个用例创建浏览器驱动，并在用例结束后关闭。"""
    browser = request.config.getoption("--browser")
    logger.info("准备浏览器驱动: %s", browser or "默认配置")
    try:
        yield Tools.get_driver(browser=browser)
    finally:
        Tools.quit_driver()
        logger.info("关闭浏览器驱动")


@pytest.fixture
def login_page(driver):
    """打开登录页并返回登录页面对象。"""
    page = PageLogin()
    page.open_url()
    return page


@pytest.fixture
def register_page(driver):
    """打开注册页并返回注册页面对象。"""
    page = RegisterPage()
    page.open_url()
    page.wait_for_form()
    return page
