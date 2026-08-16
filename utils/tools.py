"""Selenium 浏览器驱动封装，支持 Chrome 和 Firefox。"""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from config import (
    BROWSER,
    CHROME_DRIVER_PATH,
    FIREFOX_BINARY_PATH,
    FIREFOX_DRIVER_PATH,
    HEADLESS,
    IMPLICIT_WAIT,
    INITIAL_URL,
)


SUPPORTED_BROWSERS = ("chrome", "firefox")


class Tools:
    """浏览器驱动工具类，driver 使用类变量做全局复用。"""

    driver = None

    @classmethod
    def get_driver(cls, browser=None):
        """获取全局 driver；首次调用时创建并初始化指定浏览器。"""
        if cls.driver is None:
            browser = (browser or BROWSER).strip().lower()
            if browser == "chrome":
                cls.driver = cls._create_chrome_driver()
            elif browser == "firefox":
                cls.driver = cls._create_firefox_driver()
            else:
                raise ValueError(
                    f"不支持的浏览器: {browser}，可选值: {', '.join(SUPPORTED_BROWSERS)}"
                )

            if HEADLESS:
                cls.driver.set_window_size(1920, 1080)
            else:
                try:
                    cls.driver.maximize_window()
                except Exception:
                    cls.driver.set_window_size(1920, 1080)
            cls.driver.implicitly_wait(IMPLICIT_WAIT)
        return cls.driver

    @classmethod
    def _create_chrome_driver(cls):
        """创建 Chrome 驱动；优先使用显式路径，其次 webdriver-manager。"""
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        driver_path = cls._find_driver_path(CHROME_DRIVER_PATH)
        if driver_path:
            return webdriver.Chrome(
                service=ChromeService(executable_path=driver_path),
                options=options,
            )
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )
        except Exception:
            return webdriver.Chrome(options=options)

    @classmethod
    def _create_firefox_driver(cls):
        """创建 Firefox 驱动；优先使用显式路径，其次 webdriver-manager。"""
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
        if FIREFOX_BINARY_PATH:
            options.binary_location = FIREFOX_BINARY_PATH

        driver_path = cls._find_driver_path(FIREFOX_DRIVER_PATH)
        if driver_path:
            return webdriver.Firefox(
                service=FirefoxService(executable_path=driver_path),
                options=options,
            )
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            return webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
        except Exception:
            return webdriver.Firefox(options=options)

    @staticmethod
    def _find_driver_path(configured_path):
        """返回存在的驱动路径，未配置或不存在时返回 None。"""
        if not configured_path:
            return None
        path = Path(configured_path)
        return str(path) if path.exists() else None

    @classmethod
    def quit_driver(cls):
        """关闭浏览器并清理全局 driver，便于下次重新创建。"""
        if cls.driver:
            cls.driver.quit()
            cls.driver = None


if __name__ == '__main__':
    # 本地演示：创建 driver、跳转页面后关闭浏览器。
    driver = Tools.get_driver()
    driver.get(INITIAL_URL)
    Tools.quit_driver()
