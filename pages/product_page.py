"""商品详情与购物车页面对象。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import PRODUCT_URL
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("product")


class ProductPage(BasePage):
    """商品详情页对象，同时封装公共侧边购物车操作。"""

    title = (By.CSS_SELECTOR, "h1.product-title")
    price = (By.ID, "sku-price")
    quantity = (By.ID, "qty")
    add_to_cart_button = (By.ID, "action-button")
    cart_items = (By.CSS_SELECTOR, "#common-side-cart .cart-items")
    cart_subtotal = (By.CSS_SELECTOR, "#common-side-cart .grand-total-price")
    checkout_button = (By.CSS_SELECTOR, "#common-side-cart .checkout button")

    def __init__(self):
        super().__init__(Tools.get_driver(), timeout=60)

    def open_url(self):
        """打开测试商品详情页。"""
        logger.info("打开商品详情页: %s", PRODUCT_URL)
        self.driver.get(PRODUCT_URL)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(self.add_to_cart_button)
        )
        return self

    def get_price(self):
        """返回当前商品单价。"""
        return self.find_element(self.price).text.strip()

    def add_to_cart(self, quantity=1):
        """设置数量并加入购物车，等待购物车出现商品。"""
        if quantity != 1:
            qty_input = self.find_element(self.quantity)
            qty_input.clear()
            qty_input.send_keys(str(quantity))
        self.base_click(self.add_to_cart_button)
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: "Laser hair removal - Brazilian".lower()
            in driver.execute_script(
                "return arguments[0].textContent",
                driver.find_element(*self.cart_items),
            ).lower()
        )
        return self

    def get_cart_subtotal(self):
        """返回购物车小计文本。"""
        element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.cart_subtotal)
        )
        return self.driver.execute_script(
            "return arguments[0].textContent",
            element,
        ).strip()

    def proceed_checkout(self):
        """进入结算；商品为会员专属时应跳转登录页。"""
        logger.info("点击 Proceed Checkout")
        self.click_via_js(self.checkout_button)
        self.wait_for_url_contains("/account/login")
        return self

    def proceed_checkout_logged_in(self):
        """登录状态下进入结算页。"""
        logger.info("登录状态下点击 Proceed Checkout")
        self.click_via_js(self.checkout_button)
        self.wait_for_url_contains("/checkout")
        return self
