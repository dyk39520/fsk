"""注册功能测试数据，支持代码和外部 Excel 两种数据源。"""

import uuid
from typing import Any

from faker import Faker

from config import (
    REGISTER_CASES_FILE,
    REGISTER_MOBILE_COUNTRY,
    REGISTER_SUCCESS_URL,
)
from utils.data_reader import resolve_cases


_faker = Faker("zh_CN")
_CN_MOBILE_PREFIXES = [
    "130", "131", "132", "133", "135", "136", "137", "138", "139",
    "150", "151", "152", "153", "155", "156", "157", "158", "159",
    "170", "171", "176", "177", "178",
    "180", "181", "182", "183", "184", "185", "186", "187", "188", "189",
]
_HK_MOBILE_PREFIXES = ["5", "6", "9"]
_RANDOM_MARKERS = {"RANDOM", "AUTO", "随机"}
DEFAULT_PASSWORD = "Test123456"

REGISTER_CODE_CASES = [
    {
        "case": "随机账号注册",
        "email": "RANDOM",
        "mobile": "RANDOM",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "",
        "expected_keyword": "",
        "expected_url_contains": REGISTER_SUCCESS_URL,
        "design_method": "场景法",
        "execute": True,
    },
    {
        "case": "邮箱格式错误",
        "email": "invalid-email",
        "mobile": "RANDOM",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "email",
        "expected_keyword": "电子邮箱地址",
        "expected_url_contains": "",
        "design_method": "等价类划分",
        "execute": True,
    },
    {
        "case": "手机号为空",
        "email": "RANDOM",
        "mobile": "",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "mobile",
        "expected_keyword": "電話",
        "expected_url_contains": "",
        "design_method": "边界值分析",
        "execute": True,
    },
    {
        "case": "手机号已注册",
        "email": "RANDOM",
        "mobile": "13414764310",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "modal",
        "expected_keyword": "此手机号码已经有人使用",
        "expected_url_contains": "",
        "design_method": "场景法",
        "execute": True,
    },
    {
        "case": "密码不含英文字母",
        "email": "RANDOM",
        "mobile": "RANDOM",
        "password": "123456",
        "re_password": "123456",
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "password",
        "expected_keyword": "密码",
        "expected_url_contains": "",
        "design_method": "等价类划分",
        "execute": True,
    },
    {
        "case": "两次密码不一致",
        "email": "RANDOM",
        "mobile": "RANDOM",
        "password": DEFAULT_PASSWORD,
        "re_password": "Test1234567",
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": True,
        "error_field": "modal",
        "expected_keyword": "密码不相同",
        "expected_url_contains": "",
        "design_method": "错误猜测",
        "execute": True,
    },
    {
        "case": "未勾选协议",
        "email": "RANDOM",
        "mobile": "RANDOM",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "自动化",
        "last_name": "测试",
        "agreement": False,
        "error_field": "agreement",
        "expected_keyword": "请阅读并勾选",
        "expected_url_contains": "",
        "design_method": "判定表",
        "execute": True,
    },
    {
        "case": "名字为空",
        "email": "RANDOM",
        "mobile": "RANDOM",
        "password": DEFAULT_PASSWORD,
        "re_password": DEFAULT_PASSWORD,
        "first_name": "",
        "last_name": "测试",
        "agreement": True,
        "error_field": "first_name",
        "expected_keyword": "请输入名字",
        "expected_url_contains": "",
        "design_method": "边界值分析",
        "execute": True,
    },
]


def _should_generate_random(value: Any) -> bool:
    """判断外部数据文件中的 RANDOM 标记是否需要运行时生成。"""
    return str(value or "").strip().upper() in _RANDOM_MARKERS


def random_email():
    """生成随机且不易重复的注册邮箱。"""
    return f"auto_{uuid.uuid4().hex[:12]}@example.com"


def random_mobile():
    """按 REGISTER_MOBILE_COUNTRY 生成对应区号可用的纯数字手机号。"""
    if REGISTER_MOBILE_COUNTRY == "hk":
        return _faker.random_element(_HK_MOBILE_PREFIXES) + _faker.numerify("#######")
    return _faker.random_element(_CN_MOBILE_PREFIXES) + _faker.numerify("########")


def _apply_case_fields(case: dict[str, Any]) -> dict[str, Any]:
    """把外部用例行转换为注册表单数据，RANDOM 字段在运行时生成。"""
    return {
        "case": case.get("case") or "随机账号注册",
        "email": (
            random_email()
            if _should_generate_random(case.get("email"))
            else case.get("email", "")
        ),
        "mobile": (
            random_mobile()
            if _should_generate_random(case.get("mobile"))
            else case.get("mobile", "")
        ),
        "password": case.get("password", DEFAULT_PASSWORD),
        "re_password": case.get("re_password", DEFAULT_PASSWORD),
        "first_name": case.get("first_name", "自动化"),
        "last_name": case.get("last_name", "测试"),
        "agreement": case.get("agreement", True),
    }


def generate_register_data(
    overrides: dict[str, Any] | None = None,
    case: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """按外部用例生成完整注册数据；overrides 兼容旧的字段覆盖调用。"""
    data = _apply_case_fields(case or {})
    data.update(overrides or {})
    return data


REGISTER_CASES = resolve_cases(REGISTER_CODE_CASES, REGISTER_CASES_FILE)
REGISTER_SUCCESS_CASES = [
    case
    for case in REGISTER_CASES
    if not (case.get("error_field") or case.get("expected_keyword"))
]
REGISTER_NEGATIVE_CASES = [
    case
    for case in REGISTER_CASES
    if case.get("error_field") or case.get("expected_keyword")
]
