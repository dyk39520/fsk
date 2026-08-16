"""业务配置：浏览器、等待时间、登录账号和元素定位。"""

import os

from config.paths import DATA_DIR


# 浏览器配置
BROWSER = os.getenv("BROWSER", "chrome").strip().lower()
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", r"C:\Program Files\Python311\chromedriver.exe")
FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH", "")
FIREFOX_BINARY_PATH = os.getenv("FIREFOX_BINARY_PATH", "")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
INITIAL_URL = os.getenv("INITIAL_URL", "https://www.baidu.com")
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

# 登录页面配置
LOGIN_URL = os.getenv("LOGIN_URL", "https://web21.posify.me/fskinandlasersit@9.3.01.2403.0625.21/sc/account/login")
REGISTER_URL = os.getenv("REGISTER_URL", LOGIN_URL + "?register=yes")
REGISTER_MOBILE_COUNTRY = os.getenv("REGISTER_MOBILE_COUNTRY", "cn").strip().lower()
REGISTER_SUCCESS_URL = os.getenv(
    "REGISTER_SUCCESS_URL",
    "https://web21.posify.me/fskinandlasersit@9.3.01.2403.0625.21/sc/page/member-mine",
)
HOME_URL = os.getenv("HOME_URL", "https://web21.posify.me/fskinandlasersit@9.3.01.2403.0625.21/page/index")
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME", "3026288915@qq.com")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "A123456")
LOGIN_USERNAME_ID = "l-login"
LOGIN_PASSWORD_ID = "l-password"
LOGIN_BUTTON_SELECTOR = "form#login-form button.login-button"
LOGIN_WAIT_SECONDS = int(os.getenv("LOGIN_WAIT_SECONDS", "2"))
LOGIN_MOBILE_COUNTRY = os.getenv("LOGIN_MOBILE_COUNTRY", REGISTER_MOBILE_COUNTRY).strip().lower()
REGISTER_WAIT_SECONDS = int(os.getenv("REGISTER_WAIT_SECONDS", "2"))

# Failure screenshot settle time
SCREENSHOT_SETTLE_SECONDS = float(os.getenv("SCREENSHOT_SETTLE_SECONDS", "2.0"))

# 外部测试用例数据文件
CASE_FILES_DIR = DATA_DIR / "cases"
LOGIN_CASES_FILE = os.getenv(
    "LOGIN_CASES_FILE",
    str(CASE_FILES_DIR / "login_cases.csv"),
)
REGISTER_CASES_FILE = os.getenv(
    "REGISTER_CASES_FILE",
    str(CASE_FILES_DIR / "register_cases.xlsx"),
)
