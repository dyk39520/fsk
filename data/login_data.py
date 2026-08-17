"""登录功能测试数据，支持代码和外部 CSV 两种数据源。"""

from config import LOGIN_CASES_FILE, LOGIN_PASSWORD, LOGIN_USERNAME
from utils.data_reader import resolve_cases


LOGIN_CODE_CASES = [
    {
        "case": "正确账号密码登录",
        "username": LOGIN_USERNAME,
        "password": LOGIN_PASSWORD,
        "expected_result": "success",
        "execute": True,
    },
    {
        "case": "密码错误",
        "username": LOGIN_USERNAME,
        "password": "WrongPassword123",
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "邮箱格式错误",
        "username": "invalid-email",
        "password": LOGIN_PASSWORD,
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "空密码",
        "username": LOGIN_USERNAME,
        "password": "",
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "用户名为空",
        "username": "",
        "password": LOGIN_PASSWORD,
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "账号不存在",
        "username": "not-exist@example.com",
        "password": LOGIN_PASSWORD,
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "用户名首尾空格自动去除后登录",
        "username": f" {LOGIN_USERNAME} ",
        "password": LOGIN_PASSWORD,
        "expected_result": "success",
        "execute": True,
    },
    {
        "case": "密码过短",
        "username": LOGIN_USERNAME,
        "password": "A1",
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "密码全为空格",
        "username": LOGIN_USERNAME,
        "password": "      ",
        "expected_result": "fail",
        "execute": True,
    },
    {
        "case": "正确账号大小写邮箱登录",
        "username": "3026288915@QQ.COM",
        "password": LOGIN_PASSWORD,
        "expected_result": "success",
        "execute": True,
    },
]


LOGIN_CASES = resolve_cases(LOGIN_CODE_CASES, LOGIN_CASES_FILE)
LOGIN_SUCCESS_DATA = [
    case for case in LOGIN_CASES if case.get("expected_result") == "success"
]
LOGIN_FAILED_DATA = [
    case for case in LOGIN_CASES if case.get("expected_result") == "fail"
]
