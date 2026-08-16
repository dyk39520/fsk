# AI 测试用例生成

这个目录保存项目使用 AI 辅助生成测试用例时的 Skill 说明和 Prompt 示例。

## 目录

```text
ai-testing/
├─ skills/
│  ├─ test-case-writing.md       # 基础测试用例编写 Skill
│  └─ testcase-writer-plus.md    # 增强版测试用例编写 Skill
└─ prompts/
   └─ generate-register-login-cases.md  # 注册/登录用例生成 Prompt
```

## 使用方式

1. 先选择 Skill：
   - 常规功能、单份需求、快速输出：使用 `test-case-writing`。
   - 多份需求文档、需要追踪矩阵和高风险覆盖：使用 `testcase-writer-plus`。
2. 打开对应 Prompt 文件，把项目需求、页面流程、限制条件补进去。
3. 将 AI 生成的用例输出为 CSV 和 XLSX。
4. 人工评审后再合并到 `data/cases/` 或项目根目录。

## 项目固定规则

- 用例必须在“设计方法”列明确标注：等价类划分、边界值分析、判定表、状态迁移、错误猜测、场景法。
- CSV 和 XLSX 必须使用完全相同的表头。
- 默认交付 CSV 和 XLSX 两个文件。
- AI 生成内容必须先人工评审，不直接作为最终测试资产。
