"""支付/结算覆盖：ATM、金额；CMS 支付成功/失败按环境受限处理。"""

import pytest

from pages.checkout_page import CheckoutPage
from pages.product_page import ProductPage


@pytest.mark.core
@pytest.mark.core_stable
@pytest.mark.payment
def test_checkout_payment_method_is_atm_only(login_page):
    """当前站点支付方式应只有 ATM，符合到店/ATM 单一支付配置。"""
    login_page.login()
    product_page = ProductPage()
    product_page.open_url()
    product_page.add_to_cart()
    product_page.proceed_checkout_logged_in()
    checkout_page = CheckoutPage()
    checkout_page.wait_for_checkout()
    assert checkout_page.get_payment_methods() == ["atm"]


@pytest.mark.core
@pytest.mark.core_stable
@pytest.mark.payment
def test_checkout_amount_calculation(login_page):
    """商品加入购物车后结算页应付金额应与单价一致。"""
    login_page.login()
    product_page = ProductPage()
    product_page.open_url()
    product_page.add_to_cart()
    product_page.proceed_checkout_logged_in()
    checkout_page = CheckoutPage()
    checkout_page.wait_for_checkout()
    body_text = checkout_page.get_body_text()
    assert "$ 234" in body_text
    assert "应付金额" in body_text


@pytest.mark.payment
def test_payment_success_requires_cms_sandbox():
    """当前无 CMS，支付成功无法端到端验证。"""
    pytest.skip("当前站点仅 ATM/到店支付，无 CMS 沙箱，无法端到端验证支付成功")


@pytest.mark.payment
def test_payment_failure_requires_cms_sandbox():
    """当前无 CMS，支付失败无法端到端验证。"""
    pytest.skip("当前站点仅 ATM/到店支付，无 CMS 沙箱，无法端到端验证支付失败")
