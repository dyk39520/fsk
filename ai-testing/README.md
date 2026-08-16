# AI 测试用例生成

这个目录保存项目使用 AI 辅助生成测试用例时的 Skill 说明和 Prompt 示例。

## 目录

```text
ai-testing/
├─ skills/
│  ├─ test-case-writing.md       # 基础测试用例编写 Skill
│  ├─ testcase-writer-plus.md    # 增强版测试用例编写 Skill
│  └─ core-business-testing.md   # 核心业务自动化测试 Skill
└─ prompts/
   ├─ generate-register-login-cases.md  # 注册/登录用例生成 Prompt
   └─ generate-core-business-cases.md   # 核心业务用例生成 Prompt
```

## 使用方式

1. 先选择 Skill：
   - 常规功能、单份需求、快速输出：使用 `test-case-writing`。
   - 多份需求文档、需要追踪矩阵和高风险覆盖：使用 `testcase-writer-plus`。
2. 打开对应 Prompt 文件，把项目需求、页面流程、限制条件补进去。
3. 将 AI 生成的用例输出为 CSV 和 XLSX。
4. 人工评审后再合并到 `data/cases/` 或项目根目录。

## AI 赋能测试记录

本项目已用 AI 完成一轮“站点调研 -> 核心业务定义 -> 用例生成 -> Selenium 自动化落地 -> 失败证据迭代”的闭环：

1. AI 实际打开站点，识别预约、商城、咨询表单和会员结算等真实入口。
2. 使用 `test-case-writing`、`testcase-writer-plus` 的规则生成核心业务 CSV/XLSX。
3. 将用例映射为 Selenium Page Object 和 pytest 标记，不重复扩大范围。
4. 执行时发现 Vue 隐藏购物车、隐藏 radio、慢加载等问题，AI 基于截图和页面源码调整等待与点击策略。
5. 最终执行结果：`python -m pytest -m core` 共 7 条核心用例通过。

核心业务用例 Prompt 见 `prompts/generate-core-business-cases.md`。

## 项目固定规则

- 用例必须在“设计方法”列明确标注：等价类划分、边界值分析、判定表、状态迁移、错误猜测、场景法。
- CSV 和 XLSX 必须使用完全相同的表头。
- 默认交付 CSV 和 XLSX 两个文件。
- AI 生成内容必须先人工评审，不直接作为最终测试资产。
