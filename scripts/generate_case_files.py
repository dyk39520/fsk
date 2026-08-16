"""从 CSV 用例文件生成 Excel 版本，保持两种外部数据源一致。"""

from pathlib import Path

from openpyxl import Workbook

from config import CASE_FILES_DIR
from utils.data_reader import load_cases


LOGIN_CSV = CASE_FILES_DIR / "login_cases.csv"
REGISTER_CSV = CASE_FILES_DIR / "register_cases.csv"
LOGIN_XLSX = CASE_FILES_DIR / "login_cases.xlsx"
REGISTER_XLSX = CASE_FILES_DIR / "register_cases.xlsx"


def write_excel(csv_path: Path, xlsx_path: Path) -> None:
    """把 CSV 用例按原表结构写入 Excel。"""
    rows = load_cases(csv_path)
    if not rows:
        raise ValueError(f"用例文件为空: {csv_path}")

    headers = list(rows[0].keys())
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(headers)
    for row in rows:
        worksheet.append([row.get(header, "") for header in headers])
    workbook.save(xlsx_path)
    print(f"已生成 Excel 用例文件: {xlsx_path} ({len(rows)} 条)")


def main() -> None:
    """生成 login/register 的 xlsx 数据文件。"""
    write_excel(LOGIN_CSV, LOGIN_XLSX)
    write_excel(REGISTER_CSV, REGISTER_XLSX)


if __name__ == "__main__":
    main()
