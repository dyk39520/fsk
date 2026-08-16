"""登录后首页业务冒烟测试。"""

import pytest

from pages.home_page import HomePage


@pytest.mark.smoke
def test_login_then_home_page(login_page):
    """使用正确账号登录后，应进入登录后首页。"""
    login_page.login()
    home_page = HomePage(login_page.driver)
    home_page.wait_for_home_page()
    assert home_page.is_home_page()
    home_page.wait_for_loaded()
