"""登录页面对象，负责登录页元素定位和登录操作。"""

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    DEFAULT_TIMEOUT,
    LOGIN_BUTTON_SELECTOR,
    LOGIN_MOBILE_COUNTRY,
    LOGIN_PASSWORD,
    LOGIN_PASSWORD_ID,
    LOGIN_URL,
    LOGIN_USERNAME,
    LOGIN_USERNAME_ID,
    LOGIN_WAIT_SECONDS,
)
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("login")


class PageLogin(BasePage):
    """登录页面对象，继承 BasePage 后复用 find_element 封装。"""

    def __init__(self):
        """初始化登录页面对象，并定义登录页元素定位器。"""
        # 获取全局复用的浏览器驱动
        driver = Tools.get_driver()
        # 调用父类构造方法，保存 driver 和默认等待时间
        super().__init__(driver)

        # 页面元素定位元组：By.ID + 元素 id
        self.username = (By.ID, LOGIN_USERNAME_ID)
        self.password = (By.ID, LOGIN_PASSWORD_ID)
        self.login_button = (By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)
        self.mobile_login_tab = (By.CSS_SELECTOR, "button[data-login-type=mobile]")
        self.mobile_input = (By.ID, "l-login-mobile")
        self.mobile_country_flag = (By.CSS_SELECTOR, "form#login-form .selected-flag")

    def open_url(self):
        """打开登录页面地址。"""
        logger.info("打开登录页: %s", LOGIN_URL)
        self.driver.get(LOGIN_URL)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(self.login_button)
        )

    def wait_for_login_success(self, timeout=DEFAULT_TIMEOUT):
        """等待登录成功并离开登录页。"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.current_url != LOGIN_URL,
            message="登录后未离开登录页",
        )
        return self

    @staticmethod
    def _has_login_result(driver):
        """判断登录提交后是否已出现跳转、弹窗或表单错误。"""
        if driver.current_url != LOGIN_URL:
            return True
        for modal in driver.find_elements(By.CSS_SELECTOR, ".modal-body"):
            if modal.text.strip():
                return True
        for error in driver.find_elements(
            By.CSS_SELECTOR, ".parsley-errors-list li, .alert, .alert-danger, .error"
        ):
            if error.text.strip():
                return True
        return False

    def wait_for_login_settled(self, timeout=DEFAULT_TIMEOUT):
        """短等待登录结果；失败提示自动关闭时按原等待时间兜底。"""
        try:
            WebDriverWait(self.driver, min(timeout, LOGIN_WAIT_SECONDS)).until(
                self._has_login_result,
                message="登录提交后未产生跳转或错误提示",
            )
        except Exception:
            logger.info("未捕获到明确错误提示，等待 %s 秒后继续", LOGIN_WAIT_SECONDS)
            time.sleep(LOGIN_WAIT_SECONDS)
        return self

    def select_mobile_country(self, country=None):
        """选择手机号登录页签下的国家/地区区号。"""
        country = country or LOGIN_MOBILE_COUNTRY
        logger.info("选择手机登录区号: %s", country)
        flag = WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.mobile_country_flag)
        )
        ActionChains(self.driver).move_to_element(flag).click().perform()
        option_locator = f"li.country[data-country-code='{country}']"
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: any(
                element.is_displayed()
                for element in driver.find_elements(By.CSS_SELECTOR, option_locator)
            )
        )
        option = next(
            element
            for element in self.driver.find_elements(By.CSS_SELECTOR, option_locator)
            if element.is_displayed()
        )
        option.click()
        return self

    def login_with(self, username, password, wait_for_success=False):
        """按指定邮箱密码执行登录操作。"""
        logger.info("开始执行登录操作")

        # 输入测试用户名
        logger.info("输入用户名")
        self.base_input(self.username, username)

        # 输入测试密码
        logger.info("输入密码")
        self.base_input(self.password, password)

        # 点击登录按钮
        logger.info("点击登录按钮")
        self.base_click(self.login_button)

        if wait_for_success:
            logger.info("等待登录成功并离开登录页")
            self.wait_for_login_success(timeout=60)
        else:
            logger.info("等待登录结果")
            self.wait_for_login_settled()

    def login_with_mobile(self, mobile, password, wait_for_success=True):
        """切换到手机号登录并按指定手机号密码登录。"""
        logger.info("切换为手机号登录")
        mobile_tab = WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.mobile_login_tab)
        )
        mobile_tab.click()
        self.select_mobile_country()
        mobile_element = self.find_element(self.mobile_input)
        mobile_element.click()
        mobile_element.send_keys(mobile)
        self.base_input(self.password, password)
        self.base_click(self.login_button)

        if wait_for_success:
            logger.info("等待手机号登录成功")
            self.wait_for_login_success(timeout=60)
        else:
            logger.info("等待手机号登录结果")
            self.wait_for_login_settled()

    def login(self):
        """使用配置账号执行登录操作。"""
        self.login_with(LOGIN_USERNAME, LOGIN_PASSWORD, wait_for_success=True)

if __name__ == '__main__':
    # 本地演示：打开登录页并执行一次登录。
    lg = PageLogin()
    lg.open_url()
    lg.login()
