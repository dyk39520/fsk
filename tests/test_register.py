"""注册功能测试脚本。"""

import pytest

from config import BROWSER, REGISTER_SUCCESS_URL, REGISTER_URL
from data.register_data import (
    REGISTER_NEGATIVE_CASES,
    REGISTER_SUCCESS_CASES,
    generate_register_data,
)
from pages.home_page import HomePage
from pages.login_page import PageLogin
from utils.account_registry import record_registered_account


def _get_error_text(page, error_field):
    """按字段名读取注册页对应错误提示。"""
    if error_field == "email":
        return page.get_field_error(page.email)
    if error_field == "mobile":
        return page.get_error_text(page.mobile_error)
    if error_field == "password":
        return page.get_error_text(page.password_error)
    if error_field == "re_password":
        return page.get_error_text(page.re_password_error)
    if error_field == "first_name":
        return page.get_field_error(page.first_name)
    if error_field == "last_name":
        return page.get_field_error(page.last_name)
    if error_field == "agreement":
        return page.get_error_text(page.agreement_error)
    if error_field == "modal":
        return page.get_modal_text()
    raise ValueError(f"未知错误字段: {error_field}")


@pytest.mark.register
@pytest.mark.register_positive
def test_register_success_random_account(register_page, request):
    """注册成功后登记账号，并验证登出后可用手机号重新登录。"""
    case = REGISTER_SUCCESS_CASES[0]
    data = generate_register_data(case=case)
    register_page.fill_form(data).submit()
    register_page.wait_for_success()
    expected_url = case.get("expected_url_contains") or REGISTER_SUCCESS_URL
    assert expected_url in register_page.driver.current_url

    browser = request.config.getoption("--browser") or BROWSER
    record_registered_account(data, browser=browser, case=case.get("case"))

    # 清空 Cookie 等价于退出当前登录态，避免依赖不稳定的会员中心退出入口。
    register_page.driver.delete_all_cookies()

    login_page = PageLogin()
    login_page.open_url()
    login_page.login_with_mobile(data["mobile"], data["password"], wait_for_success=True)
    home_page = HomePage(login_page.driver)
    home_page.wait_for_home_page()
    assert home_page.is_home_page()


@pytest.mark.register
@pytest.mark.parametrize("case", REGISTER_NEGATIVE_CASES, ids=lambda item: item["case"])
def test_register_negative(register_page, case):
    """提交不符合规则的数据，应停留注册页并显示对应错误提示。"""
    data = generate_register_data(case=case)
    register_page.fill_form(data).submit()
    assert REGISTER_URL in register_page.driver.current_url
    error_text = _get_error_text(register_page, case["error_field"])
    assert error_text, f"{case['case']} 未显示错误提示"
    assert case["expected_keyword"] in error_text
