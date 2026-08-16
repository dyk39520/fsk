# Selenium PO Pytest 项目

基于 Python + Selenium + Page Object + Pytest 的自动化测试项目。

## 目录结构

```text
Po/
├─ config/          # 项目配置
├─ pages/           # 页面对象
├─ utils/           # 工具类
├─ tests/           # pytest 测试
├─ scripts/         # 脚本
├─ data/            # 测试数据
├─ logs/            # 日志
├─ reports/         # 测试报告
├─ screenshots/     # 失败截图
├─ allure-results/  # Allure 结果
└─ .github/         # CI 配置
```

## 环境准备

```bash
pip install -r requirements.txt
```

默认使用 Chrome 运行；如需 Firefox 兼容性测试，请先安装 Firefox。geckodriver 未配置时，`webdriver-manager` 会自动下载。

## 运行测试

```bash
python -m pytest
```

`pytest.ini` 已配置生成 HTML 报告，运行后会输出到 `reports/report.html`。

## 数据驱动

测试数据存放在外部文件中，测试运行时会读取文件后参数化：

- 登录用例：`data/cases/login_cases.csv`
- 注册用例：`data/cases/register_cases.xlsx`，同目录下也有 CSV 版本
- 新增或修改用例时直接编辑对应文件，不需要修改测试函数
- 如果编辑了 CSV，可执行 `python -m scripts.generate_case_files` 重新生成 Excel 版本
- 可用环境变量 `LOGIN_CASES_FILE`、`REGISTER_CASES_FILE` 指定其他 CSV/Excel 数据文件
- 默认 `auto`：有文件时用文件，文件不存在时退回代码里的用例数据
- 强制只用文件：`python -m pytest --data-source file`
- 强制只用代码：`python -m pytest --data-source code`
- 也可以用环境变量 `TEST_DATA_SOURCE=code` 或 `TEST_DATA_SOURCE=file`

## 选择浏览器

```bash
# Chrome（默认）
python -m pytest

# Firefox 兼容性测试
python -m pytest --browser firefox
```

也可以设置环境变量 `BROWSER=firefox`。如需指定驱动或浏览器程序路径，可设置 `FIREFOX_DRIVER_PATH`、`FIREFOX_BINARY_PATH`。

## 注册功能测试

```bash
# 只跑注册用例，默认 Chrome
python -m pytest -m register

# Firefox 兼容性注册测试
python -m pytest -m register --browser firefox

# 一键运行注册用例
python -m scripts.run_tests -m register --browser firefox
```

注册邮箱和手机号每次执行时由 Faker 随机生成。手机号默认选择中国区号 `cn`，可设置 `REGISTER_MOBILE_COUNTRY=hk` 切换为香港区号。

## 按标记运行

```bash
# 只运行登录用例
python -m pytest -m login

# 只运行冒烟用例
python -m pytest -m smoke
```

## 一键运行并生成报告

```bash
python -m scripts.run_tests
```

Firefox 兼容性测试也可通过一键脚本运行：

```bash
python -m scripts.run_tests --browser firefox
```

该脚本会：

1. 运行全部 pytest 用例。
2. 自动生成 HTML 报告到 `reports/report.html`。
3. 如果安装了 `allure-pytest`，生成 Allure 结果到 `allure-results/`。
4. 如果同时安装了 Allure CLI，生成 Allure 报告到 `reports/allure-report/`。

## 手动生成 Allure 报告

```bash
python -m pytest --alluredir=allure-results
allure generate allure-results -o reports/allure-report --clean
```
