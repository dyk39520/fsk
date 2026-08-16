"""基础页面封装，提供浏览器驱动的公共初始化和元素查找能力。"""

import re
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT, SCREENSHOTS_DIR
from utils.logger import get_logger


logger = get_logger("page")


class BasePage(object):
    """所有页面类的父类，封装 WebDriver 的公共操作。"""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.default_timeout = timeout

    def find_element(self, loc):
        """查找页面元素，等待元素存在且可见后返回。
        Args:
            loc: Selenium 定位元组，例如 (By.ID, "l-login")。
        Returns:
            定位到的 WebElement 对象。
        Raises:
            元素在超时时间内未可见时抛出 Selenium 异常。
        """
        logger.info("查找元素: %s", loc)
        try:
            # visibility_of_element_located 要求元素存在且在页面中可见，
            # 比 presence_of_element_located 更适合作点击、输入前的等待条件。
            element = (WebDriverWait(self.driver, self.default_timeout)
                       .until(EC.visibility_of_element_located(loc)))
            logger.info("元素已找到: %s", loc)
            return element
        except Exception as e:
            logger.exception("查找元素失败: %s", loc)
            raise e

    def base_input(self, loc, text):
        """等待元素可见后，清空输入框并输入 text。"""
        element = self.find_element(loc)
        element.clear()
        element.send_keys(text)

    def base_click(self, loc):
        """等待元素可见后执行点击。"""
        self.find_element(loc).click()

    def base_press_enter(self, loc):
        """等待元素可见后按下回车。"""
        self.find_element(loc).send_keys(Keys.ENTER)

    def click_via_js(self, loc):
        """对可点击但可能被遮罩/移出视口的元素执行 JS 点击。"""
        element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(loc)
        )
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def wait_for_text(self, text, timeout=None):
        """等待页面 body 中出现指定文本。"""
        WebDriverWait(self.driver, timeout or self.default_timeout).until(
            lambda driver: text in driver.find_element(By.TAG_NAME, "body").text,
            message=f"页面未出现文本: {text}",
        )
        return self

    def wait_for_url_contains(self, text, timeout=None):
        """等待当前 URL 包含指定片段。"""
        WebDriverWait(self.driver, timeout or self.default_timeout).until(
            lambda driver: text in driver.current_url,
            message=f"URL 未包含: {text}",
        )
        return self

    def save_screenshot(self, file_path=None):
        """将当前页面截图保存到指定路径；未传路径时保存到 screenshots 目录。"""
        if file_path is None:
            file_path = SCREENSHOTS_DIR / f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(file_path))
        return str(file_path)

    def save_evidence(self, label="evidence", element=None):
        """保存当前页面截图；传入 element 时同时保存关键元素特写。"""
        safe_label = re.sub(r"[^\w.\-]", "_", label)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        png_path = SCREENSHOTS_DIR / f"{safe_label}_{timestamp}.png"
        try:
            png_path.parent.mkdir(parents=True, exist_ok=True)
            if element is not None:
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                        element,
                    )
                except Exception:
                    pass
            self.driver.save_screenshot(str(png_path))
            logger.info("页面证据已保存: %s", png_path)
            return str(png_path)
        except Exception as exc:
            logger.error("保存页面证据失败: %s", exc)
            return ""

    def switch_window(self, index=0):
        """切换到指定序号的窗口，序号从 0 开始。"""
        handles = self.driver.window_handles
        if index < 0 or index >= len(handles):
            raise IndexError(f"窗口序号 {index} 超出范围，当前共有 {len(handles)} 个窗口")
        self.driver.switch_to.window(handles[index])

    def switch_to_new_window(self):
        """切换到最新打开的窗口。"""
        # window_handles 最后一位通常是最近打开的窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
