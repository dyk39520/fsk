"""预约确认与支付结算页面对象。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import CHECKOUT_URL
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("checkout")


class CheckoutPage(BasePage):
    """预约确认/结算页对象。"""

    first_name = (By.NAME, "coreShippingFirstName")
    last_name = (By.NAME, "coreShippingLastName")
    mobile = (By.NAME, "coreShippingMobile")
    email = (By.NAME, "coreShippingEmail")
    payment_methods = (By.NAME, "corePaymentMethod")
    agree = (By.ID, "order-agree")
    submit_button = (By.CSS_SELECTOR, "button.nav-button[type='submit']")
    remove_item = (By.CSS_SELECTOR, "#checkout-form .remove-item")
    service_rows = (By.CSS_SELECTOR, "#checkout-form .service-item")
    cart_clear_all = (
        By.CSS_SELECTOR,
        "#common-side-cart .cart-title .clear-btn",
    )
    cart_items = (By.CSS_SELECTOR, "#common-side-cart .product-item")
    cart_item_clear = (
        By.CSS_SELECTOR,
        "#common-side-cart .product-item .clear-btn",
    )

    def __init__(self):
        super().__init__(Tools.get_driver(), timeout=60)

    def open_url(self):
        """打开结算页。"""
        logger.info("打开结算页: %s", CHECKOUT_URL)
        self.driver.get(CHECKOUT_URL)
        self.wait_for_text("提交预约")
        return self

    def wait_for_checkout(self):
        """等待预约确认页面。"""
        self.wait_for_text("提交预约")
        self.wait_for_text("服务")
        return self

    def get_payment_methods(self):
        """返回可选支付方式。"""
        return [
            element.get_attribute("value")
            for element in self.driver.find_elements(*self.payment_methods)
        ]

    def is_submit_enabled(self):
        """检查提交预约按钮是否可用。"""
        button = self.find_element(self.submit_button)
        return button.is_enabled()

    def remove_first_item(self):
        """点击结算页服务行的 x 删除预约服务。"""
        logger.info("点击结算页 x 删除服务")
        before = len(self.get_service_rows())
        element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.remove_item)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
            element,
        )
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: len(self.get_service_rows()) < before
        )
        return self

    def remove_all_items(self, max_items=20):
        """清空结算页已选服务，用于避免测试账号残留数据干扰。"""
        logger.info("清空结算页服务")
        clear_button = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.cart_clear_all)
        )
        self.driver.execute_script("arguments[0].click();", clear_button)
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: (
                not driver.find_elements(*self.cart_items)
                and not self.get_service_rows()
            )
        )
        return self

    def get_service_rows(self):
        """返回结算页所有服务行文本。"""
        return [
            element.text.strip().replace("\n", " ")
            for element in self.driver.find_elements(*self.service_rows)
            if element.text.strip()
        ]

    def get_body_text(self):
        """返回页面文本，便于断言服务、时间、金额。"""
        return self.driver.find_element(By.TAG_NAME, "body").text
