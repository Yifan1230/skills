# V0.3 Changes

## 修复的核心问题

V0.2 虽然规定要使用产品语言，但没有阻止 Agent 最终继续输出：

`Feature → configuration_candidate / observe / keep_custom`

V0.3 改为硬约束。

## 新增

1. `references/product-problem-synthesis.md`
2. `references/product-analyst-pass.md`
3. `references/product-language-gate.md`
4. `templates/product-problem-card.schema.json`
5. `scripts/business_semantics.py`
6. `scripts/report_guard.py`

## 新流程

`技术分析 → 业务证据包 → 产品分析二次 Pass → Product Problem Card → PM 报告 → 自动校验`

## 关键行为

- 只有 `ready_for_pm` 可进入产品优化主表。
- 无法确认业务含义时必须标 `needs_business_confirmation`。
- 主报告中出现 `.java/.epm/.eda`、hutool、内部英文枚举等，自动判失败。
