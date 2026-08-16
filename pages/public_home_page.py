"""公开首页页面对象，覆盖商品搜索。"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT, HOME_URL
from pages.base_page import BasePage
from utils.logger import get_logger
from utils.tools import Tools


logger = get_logger("public_home")


class PublicHomePage(BasePage):
    """公开首页页面对象。"""

    search_input = (By.CSS_SELECTOR, "input[placeholder='Search for product...']")

    def __init__(self):
        super().__init__(Tools.get_driver())

    def open_url(self):
        """打开公开首页。"""
        logger.info("打开公开首页: %s", HOME_URL)
        self.driver.get(HOME_URL)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(self.search_input)
        )
        return self

    def search(self, keyword):
        """输入关键词并搜索商品。"""
        logger.info("搜索商品: %s", keyword)
        self.base_input(self.search_input, keyword)
        self.base_press_enter(self.search_input)
        return self

    def wait_for_search_results(self, keyword):
        """等待搜索 URL 和结果页出现。"""
        self.wait_for_url_contains("action=search&keyword=")
        self.wait_for_text(keyword.upper())
        return self
