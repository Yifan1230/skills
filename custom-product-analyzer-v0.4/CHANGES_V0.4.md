# V0.4 Changes

## 核心修复

此前 Skill 即使使用“产品语言”，仍然容易从代码差异直接推导产品问题。

V0.4 改为 Behavior-first：

```text
Technical Diff
→ Runtime Behavior
→ Behavior Delta
→ Feature
→ Product Problem
→ Ideal Product Behavior
```

## 新增

- `references/runtime-behavior-analysis.md`
- `references/behavior-recovery-pass.md`
- `templates/behavior-delta.schema.json`

## 强制要求

正式产品候选必须明确：

- 标品当前行为
- 客户版本行为
- 用户可感知差异

回答不了，就只能进入“行为语义待确认”，不得进入产品建议。
