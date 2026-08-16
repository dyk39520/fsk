"""本地登记正向注册生成的测试账号，便于后续审计和清理。"""

import csv
from datetime import datetime
from pathlib import Path

from config import LOG_DIR
from utils.logger import get_logger


logger = get_logger("account_registry")
ACCOUNT_FILE = LOG_DIR / "registered_accounts.csv"
HEADERS = ["注册时间", "邮箱", "手机号", "密码", "浏览器", "用例"]


def record_registered_account(data, browser="chrome", case="随机账号注册"):
    """把一次成功注册写入本地账号登记表。"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    is_new = not Path(ACCOUNT_FILE).exists()
    with ACCOUNT_FILE.open("a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "注册时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "邮箱": data["email"],
                "手机号": data["mobile"],
                "密码": data["password"],
                "浏览器": browser,
                "用例": case,
            }
        )
    logger.info("已登记注册账号: %s", data["email"])
    return str(ACCOUNT_FILE)
