"""注册页面对象，负责注册表单元素定位和注册操作。"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import (
    DEFAULT_TIMEOUT,
    REGISTER_MOBILE_COUNTRY,
    REGISTER_SUCCESS_URL,
    REGISTER_URL,
    REGISTER_WAIT_SECONDS,
)
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("register")


class RegisterPage(BasePage):
    """注册页面对象，继承 BasePage 后复用元素查找和输入封装。"""

    def __init__(self):
        """初始化注册页面对象，并定义注册表单元素定位器。"""
        driver = Tools.get_driver()
        super().__init__(driver)

        self.email = (By.NAME, "customForm[1][registerEmail]")
        self.mobile = (By.NAME, "customForm[1][registerMobile][tel_no]")
        self.password = (By.NAME, "customForm[1][registerPassword]")
        self.re_password = (By.NAME, "customForm[1][registerRePassword]")
        self.first_name = (By.NAME, "customForm[1][registerFirstName]")
        self.last_name = (By.NAME, "customForm[1][registerLastName]")
        self.agreement_checkbox = (By.ID, "customForm_1_registerAgreement")
        self.submit_button = (By.CSS_SELECTOR, "form#register-form button.login-button")
        self.mobile_flag = (By.CSS_SELECTOR, "form#register-form .selected-flag")

        self.email_error = (By.ID, "register-email-errors")
        self.mobile_error = (By.ID, "register-mobile-errors")
        self.password_error = (By.ID, "register-password-errors")
        self.re_password_error = (By.ID, "register-re-password-errors")
        self.agreement_error = (By.ID, "submit-checkbox-error")

    def open_url(self):
        """打开注册页面地址。"""
        logger.info("打开注册页: %s", REGISTER_URL)
        self.driver.get(REGISTER_URL)

    def wait_for_form(self):
        """等待注册表单和提交按钮可见。"""
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(self.submit_button)
        )
        return self

    def fill_form(self, data):
        """按测试数据填写注册表单。"""
        logger.info("填写注册表单")
        self.base_input(self.email, data["email"])
        self.base_input(self.password, data["password"])
        self.base_input(self.re_password, data["re_password"])
        self.base_input(self.first_name, data["first_name"])
        self.base_input(self.last_name, data["last_name"])
        if data.get("agreement", True):
            self.check_agreement()
        # intl-tel-input 在失焦后会清空手机号，必须放到提交前最后输入。
        self.input_mobile(data["mobile"])
        return self

    def select_mobile_country(self, country=None):
        """通过页面区号下拉框选择手机号国家/地区。"""
        country = country or REGISTER_MOBILE_COUNTRY
        logger.info("选择手机号区号: %s", country)
        flag = WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(self.mobile_flag)
        )
        flag.click()
        country_option = WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"li.country[data-country-code='{country}']")
            )
        )
        country_option.click()
        return self

    def input_mobile(self, mobile, country=None):
        """选择区号后输入手机号；intl-tel-input 要求先点击输入框再输入。"""
        self.select_mobile_country(country)
        element = self.find_element(self.mobile)
        element.click()
        element.send_keys(mobile)
        return self

    def check_agreement(self):
        """勾选注册协议；icheck 会隐藏原生 checkbox，需点击其可视化外层。"""
        checkbox = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.agreement_checkbox)
        )
        if not checkbox.is_selected():
            logger.info("勾选注册协议")
            wrapper = WebDriverWait(self.driver, self.default_timeout).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "form#register-form div.icheckbox_square-blue")
                )
            )
            wrapper.click()
        return self

    def submit(self):
        """点击注册提交按钮。"""
        logger.info("点击立即登记按钮")
        self.base_click(self.submit_button)
        return self

    def register(self, data, wait_for_success=True, wait_seconds=None):
        """打开注册页并提交表单；默认显式等待注册成功。"""
        self.open_url()
        self.wait_for_form()
        self.fill_form(data)
        self.submit()
        if wait_for_success:
            self.wait_for_success()
        else:
            wait_seconds = (
                wait_seconds if wait_seconds is not None else REGISTER_WAIT_SECONDS
            )
            logger.info("等待注册处理 %s 秒", wait_seconds)
            time.sleep(wait_seconds)
        return self

    def wait_for_success(self, timeout=DEFAULT_TIMEOUT):
        """等待注册成功并进入会员中心页面。"""
        logger.info("等待注册成功页面: %s", REGISTER_SUCCESS_URL)
        WebDriverWait(self.driver, timeout).until(
            lambda driver: REGISTER_SUCCESS_URL in driver.current_url,
            message=f"注册成功后未进入页面: {REGISTER_SUCCESS_URL}",
        )
        return self

    def get_error_text(self, loc):
        """读取指定错误提示容器文本，未出现时返回空字符串。"""
        try:
            element = WebDriverWait(self.driver, self.default_timeout).until(
                EC.visibility_of_element_located(loc)
            )
            text = element.text.strip()
            if text:
                self.save_evidence("register_field_error", element=element)
            return text
        except Exception:
            return ""

    def get_field_error(self, loc):
        """读取输入框后跟随的 Parsley 错误文本，未出现时返回空字符串。"""
        try:
            field = WebDriverWait(self.driver, self.default_timeout).until(
                EC.presence_of_element_located(loc)
            )
            error_list = field.find_element(
                By.XPATH,
                "following-sibling::ul[contains(@class,'parsley-errors-list')]",
            )
            text = error_list.text.strip()
            if text:
                self.save_evidence("register_parsley_error", element=error_list)
            return text
        except Exception:
            return ""

    def _visible_modal_element(self, driver):
        """返回当前可见且有文本的弹窗，并在发现瞬间保存关键截图。"""
        for element in driver.find_elements(By.CSS_SELECTOR, ".modal-body"):
            if not element.is_displayed():
                continue
            text = element.text.strip()
            if text:
                self.save_evidence("register_modal", element=element)
                return element
        return None

    def get_modal_text(self):
        """读取服务端或业务校验弹窗文本，未出现时返回空字符串。"""
        try:
            modal = WebDriverWait(
                self.driver,
                self.default_timeout,
                poll_frequency=0.02,
            ).until(self._visible_modal_element)
        except Exception:
            return ""
        try:
            return modal.text.strip()
        except Exception:
            return ""
