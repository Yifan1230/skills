# Methodology

## 核心思想

本 Skill 借鉴 Software Product Line / Variability Analysis 的思想，但面向产品经理的真实目标做了改造。

分析对象不是“代码文件”，而是：

```text
Application Variant
→ Change Unit
→ Business Feature
→ Feature Variant
→ Productization Opportunity
```

## Commonality / Variability

- Commonality：多个客户共同存在、基本稳定的能力。
- Variability：只在部分客户出现，或同一能力存在不同规则、粒度、流程、字段、权限的变化。

真正值得产品经理关注的不是“哪里不同”，而是：

1. 哪些差异重复出现；
2. 同一个 Feature 被怎样反复改造；
3. 这些改造是否说明标品某个能力被写死；
4. 应做成固定功能、参数、配置、规则、流程，还是继续保留定制。

## 不直接复制论文算法

历史方法可能使用 FCA / LSI 等。本 Skill 在现代 Agent 环境中优先采用：

- 文件系统 diff
- XML/DSL 结构化解析
- Hash / 版本 / 参考号聚类
- 引用关系图
- LLM 语义归类
- 必要时 Embedding（后续增强）

学方法论，不机械复刻旧算法。
