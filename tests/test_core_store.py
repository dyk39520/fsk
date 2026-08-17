"""核心商城链路测试：搜索、加购、会员结算登录门禁。"""

import pytest


@pytest.mark.core
@pytest.mark.core_stable
@pytest.mark.store
def test_search_returns_laser_products(public_home_page):
    """按核心关键词搜索后应展示商品结果。"""
    public_home_page.search("laser")
    public_home_page.wait_for_search_results("LASER HAIR REMOVAL")
    assert "action=search&keyword=laser" in public_home_page.driver.current_url


@pytest.mark.core
@pytest.mark.core_stable
@pytest.mark.store
def test_product_detail_add_to_cart(product_page):
    """商品详情加入购物车后小计应等于商品单价。"""
    assert product_page.get_price() == "234"
    product_page.add_to_cart()
    assert product_page.get_cart_subtotal() == "$ 234"


@pytest.mark.core
@pytest.mark.core_stable
@pytest.mark.store
def test_member_checkout_requires_login(product_page):
    """会员专属商品结算应引导用户登录。"""
    product_page.add_to_cart()
    product_page.proceed_checkout()
    assert "/account/login" in product_page.driver.current_url
