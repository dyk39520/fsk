"""登录后首页页面对象。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT, HOME_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    """登录后的首页页面对象。"""

    member_link = (By.CSS_SELECTOR, "a.link-item.is-login")
    sign_out_link = (
        By.CSS_SELECTOR,
        "a.link-item[href*='sign-out'], a[href*='sign-out']",
    )

    def wait_for_home_page(self, timeout=DEFAULT_TIMEOUT):
        """等待浏览器跳转到登录后的首页地址。"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: HOME_URL in driver.current_url,
            message=f"未跳转到首页: {HOME_URL}",
        )
        return self

    def is_home_page(self):
        """判断当前是否已进入登录后首页。"""
        return HOME_URL in self.driver.current_url

    def wait_for_loaded(self):
        """等待首页登录用户入口可见。"""
        self.find_element(self.member_link)
        return self

    def sign_out(self):
        """点击退出登录入口。"""
        before_url = self.driver.current_url
        self.base_click(self.sign_out_link)
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: (
                driver.current_url != before_url
                and "sign-out" not in driver.current_url
                and not driver.find_elements(By.CSS_SELECTOR, "a[href*='sign-out']")
            )
        )
        return self
