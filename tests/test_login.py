"""登录功能测试脚本。"""

import pytest

from config import LOGIN_URL
from data.login_data import LOGIN_FAILED_DATA, LOGIN_SUCCESS_DATA


@pytest.mark.login
@pytest.mark.parametrize("case", LOGIN_SUCCESS_DATA, ids=lambda item: item["case"])
def test_login_success(login_page, case):
    """使用正确账号密码登录后，页面应离开登录地址。"""
    login_page.login()
    assert login_page.driver.current_url != LOGIN_URL


@pytest.mark.login
@pytest.mark.parametrize("case", LOGIN_FAILED_DATA, ids=lambda item: item["case"])
def test_login_failed_remains_on_login_page(login_page, case):
    """错误账号或密码登录后应停留在登录页。"""
    login_page.login_with(case["username"], case["password"])
    assert login_page.driver.current_url == LOGIN_URL
