# core-business-testing Skill

## 适用场景

- 需要从真实站点调研中确定核心业务并落地自动化测试。
- 站点功能较多，不能平均铺开用例，需要按业务影响和失败风险排序。
- 需要同时交付可评审测试用例和可执行的 Selenium Page Object 自动化。

## 核心原则

1. 先区分核心业务与支撑链路，不为低价值页面写重复用例。
2. 核心业务优先覆盖“能直接带来收入和客户转化”的链路。
3. 用例生成必须使用 `test-case-writing` / `testcase-writer-plus` 的字段与设计方法规则。
4. 输出固定为 CSV + XLSX，表头必须完全一致。
5. 自动化实现要复用项目已有框架，不在外部站点上盲目提交真实业务数据。

## 执行流程

1. 项目理解：打开站点，抓取导航、表单、购物车、预约页和结算页，记录真实选择器与交互限制。
2. 核心业务定义：根据站点定位确定高价值链路；本项目定义为预约、商城成交。
3. 风险分级：核心链路标 P0/P1，纯内容展示、社交链接等只做冒烟或不纳入。
4. 用例生成：按固定表头输出 CSV/XLSX，并在“设计方法”列标注等价类划分、边界值分析、判定表、状态迁移、错误猜测、场景法。
5. 自动化落地：沿用现有 Selenium PO 项目结构，补充页面对象、测试文件和 pytest 标记。
6. 验证与迭代：真实浏览器执行，依据失败截图/页面源码调整隐藏控件、慢加载和异步购物车等待策略。
7. AI 赋能记录：把站点调研结论、Prompt、用例文件、自动化映射写入 `ai-testing/`，形成可追溯的 AI 测试资产。

## 本仓库落地

- 用例 Prompt：`prompts/generate-core-business-cases.md`
- 用例文件：`核心业务测试用例_最终.csv`、`核心业务测试用例_最终.xlsx`
- 页面对象：`pages/public_home_page.py`、`pages/product_page.py`、`pages/booking_page.py`、`pages/checkout_page.py`
- 自动化用例：`tests/test_core_store.py`、`tests/test_booking_scenarios.py`、`tests/test_payment_checkout.py`
- 运行入口：`python -m pytest -m core`

## 风险与约束

- 预约确认和有效咨询提交会写真实数据，默认自动化只测到“进入日期时间步骤”和“表单校验”。
- 会员专属商品结算只验证登录门禁，不在没有会员测试数据时继续完成支付。
- 购物车是 Vue 异步渲染的隐藏抽屉，读取小计必须使用 `textContent`，点击结算按钮使用 JS 点击。
- 预约页原生 radio 被自定义控件隐藏，Selenium 需要通过 DOM presence + JS click 操作。
