"""验证项目能够从 CSV/Excel 外部文件读取测试用例数据。"""

import importlib

import data.login_data as login_data_module
import data.register_data as register_data_module
from config import CASE_FILES_DIR, LOGIN_CASES_FILE, REGISTER_CASES_FILE
from data.login_data import LOGIN_FAILED_DATA, LOGIN_SUCCESS_DATA
from data.register_data import (
    REGISTER_NEGATIVE_CASES,
    REGISTER_SUCCESS_CASES,
    generate_register_data,
)
from utils.data_reader import load_cases, read_csv_cases, resolve_cases


def _reload_data_modules():
    """重新加载数据模块，让 TEST_DATA_SOURCE 环境变量生效。"""
    return (
        importlib.reload(login_data_module),
        importlib.reload(register_data_module),
    )


def test_login_cases_read_from_csv():
    cases = load_cases(LOGIN_CASES_FILE)

    assert len(cases) == 10
    assert len(LOGIN_SUCCESS_DATA) == 3
    assert len(LOGIN_FAILED_DATA) == 7
    assert LOGIN_SUCCESS_DATA[0]["username"] == "3026288915@qq.com"
    assert LOGIN_FAILED_DATA[-1]["password"] == ""
    assert all(case.get("execute") for case in cases)


def test_register_cases_read_from_excel():
    cases = load_cases(REGISTER_CASES_FILE)

    assert len(cases) == 8
    assert len(REGISTER_SUCCESS_CASES) == 1
    assert len(REGISTER_NEGATIVE_CASES) == 7
    assert "邮箱格式错误" in {case["case"] for case in REGISTER_NEGATIVE_CASES}
    assert "名字为空" in {case["case"] for case in REGISTER_NEGATIVE_CASES}
    assert isinstance(cases[0]["agreement"], bool)
    assert isinstance(cases[0]["execute"], bool)
    assert REGISTER_SUCCESS_CASES[0]["expected_url_contains"]


def test_csv_and_excel_versions_are_synced():
    login_csv = load_cases(CASE_FILES_DIR / "login_cases.csv")
    login_xlsx = load_cases(CASE_FILES_DIR / "login_cases.xlsx")
    register_csv = load_cases(CASE_FILES_DIR / "register_cases.csv")
    register_xlsx = load_cases(CASE_FILES_DIR / "register_cases.xlsx")

    assert login_csv == login_xlsx
    assert register_csv == register_xlsx


def test_generate_register_data_from_external_case():
    positive_case = REGISTER_SUCCESS_CASES[0]
    positive_data = generate_register_data(case=positive_case)

    assert "@" in positive_data["email"]
    assert len(positive_data["mobile"]) >= 8
    assert positive_data["agreement"] is True

    empty_mobile_case = next(
        case
        for case in REGISTER_NEGATIVE_CASES
        if case["case"] == "手机号为空"
    )
    empty_mobile_data = generate_register_data(case=empty_mobile_case)
    assert empty_mobile_data["mobile"] == ""

    no_agreement_case = next(
        case
        for case in REGISTER_NEGATIVE_CASES
        if case["case"] == "未勾选协议"
    )
    no_agreement_data = generate_register_data(case=no_agreement_case)
    assert no_agreement_data["agreement"] is False


def test_csv_reader_handles_bom_and_blank_rows(tmp_path):
    csv_path = tmp_path / "cases.csv"
    csv_path.write_text(
        "\ufeffcase,value,execute\nA,1,TRUE\n\n",
        encoding="utf-8",
    )

    rows = read_csv_cases(csv_path)

    assert len(rows) == 1
    assert rows[0] == {"case": "A", "value": "1", "execute": True}


def test_data_source_can_switch_between_code_and_file(monkeypatch):
    monkeypatch.setenv("TEST_DATA_SOURCE", "code")
    login_module, register_module = _reload_data_modules()
    try:
        assert login_module.LOGIN_CASES == login_module.LOGIN_CODE_CASES
        assert register_module.REGISTER_CASES == register_module.REGISTER_CODE_CASES
        assert len(register_module.REGISTER_NEGATIVE_CASES) == 7
    finally:
        monkeypatch.delenv("TEST_DATA_SOURCE", raising=False)
        _reload_data_modules()

    monkeypatch.setenv("TEST_DATA_SOURCE", "file")
    login_module, register_module = _reload_data_modules()
    try:
        assert login_module.LOGIN_CASES == load_cases(LOGIN_CASES_FILE)
        assert register_module.REGISTER_CASES == load_cases(REGISTER_CASES_FILE)
    finally:
        monkeypatch.delenv("TEST_DATA_SOURCE", raising=False)
        _reload_data_modules()


def test_resolve_cases_auto_falls_back_to_code(tmp_path):
    missing_file = tmp_path / "missing_cases.xlsx"
    code_cases = [{"case": "代码用例", "execute": True}]

    resolved = resolve_cases(code_cases, missing_file, source="auto")

    assert resolved == code_cases


def test_resolve_cases_file_mode_requires_existing_file(tmp_path):
    missing_file = tmp_path / "missing_cases.xlsx"

    import pytest

    with pytest.raises(FileNotFoundError):
        resolve_cases([], missing_file, source="file")
