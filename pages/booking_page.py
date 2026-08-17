"""服务预约页面对象，覆盖服务选择、日期时间、加服务和确认入口。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BOOKING_URL
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("booking")


class BookingPage(BasePage):
    """服务预约流程页面对象。"""

    service_radio = (By.CSS_SELECTOR, "input[type='radio']")
    next_button = (
        By.XPATH,
        "//button[normalize-space()='Next' or normalize-space()='下一步']",
    )
    add_service_button = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Add another service') "
        "or contains(normalize-space(), '繼續添加服務') "
        "or contains(normalize-space(), '继续添加服务')]",
    )
    proceed_button = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Proceed to Confirm Booking') "
        "or contains(normalize-space(), '前往確認') "
        "or contains(normalize-space(), '前往确认')]",
    )
    back_button = (
        By.XPATH,
        "//button[normalize-space()='Back' or normalize-space()='返回']",
    )

    def __init__(self):
        super().__init__(Tools.get_driver(), timeout=60)

    def open_url(self):
        """打开服务预约页。"""
        logger.info("打开预约页: %s", BOOKING_URL)
        self.driver.get(BOOKING_URL)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(self.service_radio)
        )
        return self

    def select_service(self, value):
        """通过 JS 选中指定服务；原生 radio 会被自定义控件拦截。"""
        locator = (By.CSS_SELECTOR, f"input[type='radio'][value='{value}']")
        radio = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", radio)
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda driver: driver.find_element(*locator).is_selected()
        )
        return self

    def click_next(self):
        """进入预约下一步。"""
        logger.info("点击 Next")
        self.base_click(self.next_button)
        return self

    def select_date(self, day):
        """在日期面板选择可用日期。"""
        logger.info("选择日期: %s", day)
        self.driver.execute_script(
            """
            const td = [...document.querySelectorAll('td')].find(
                el => el.classList.contains('available')
                    && el.querySelector('span')?.textContent.trim() === arguments[0]
            );
            if (td) td.click();
            """,
            str(day),
        )
        return self

    def select_time(self, time_value):
        """通过 JS 选择时间段。"""
        locator = (
            By.CSS_SELECTOR,
            f"input[type='radio'][value='{time_value}']",
        )
        radio = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].click();", radio)
        return self

    def wait_for_day_time(self):
        """等待日期时间步骤。"""
        self.wait_for_text("Day and time")
        return self

    def click_add_another_service(self):
        """点击继续添加服务，返回服务选择步骤。"""
        logger.info("点击继续添加服务")
        self.base_click(self.add_service_button)
        self.wait_for_text("Services")
        return self

    def click_proceed_to_checkout(self):
        """点击前往确认，进入预约确认/结算页。"""
        logger.info("点击前往确认")
        self.click_via_js(self.proceed_button)
        self.wait_for_url_contains("/checkout")
        return self

    def click_proceed_button(self):
        """仅点击前往确认，不等待跳转；用于校验拦截场景。"""
        logger.info("点击前往确认（不等待跳转）")
        self.click_via_js(self.proceed_button)
        return self

    def click_back(self):
        """返回上一步。"""
        logger.info("点击 Back")
        self.base_click(self.back_button)
        return self
