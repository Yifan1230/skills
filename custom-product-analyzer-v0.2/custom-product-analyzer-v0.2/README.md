# custom-product-analyzer v0.2

Claude Code / Multica Skill，用于：

> 指定一个标品应用，横向扫描所有客户变体，从技术差异还原真正的业务产品问题，并输出产品经理可判断的标品优化方案。

## v0.2 重点变化

V0.1 已能做到：

`Variant → Baseline → Diff → Change Unit → Feature → Productization`

V0.2 增加关键的产品语义层：

```text
技术差异
→ 用户行为变化
→ 业务场景/角色
→ 标品限制
→ 客户为何定制
→ 共性产品根因
→ 优化目标
→ 产品能力方案
```

因此最终报告不应再只出现：

```text
configuration_candidate
observe
keep_custom
```

这些仅保留为内部分类。

## 安装

将整个目录复制到：

```bash
~/.claude/skills/custom-product-analyzer/
```

或项目：

```bash
.claude/skills/custom-product-analyzer/
```

## 首次推荐

```text
分析应用：xkglapp
深度：poc
```

## 最终报告优先输出

```text
产品问题
业务场景/影响
客户定制共性
根因判断
优化目标
具体产品能力方案
证据客户
置信度
```

技术证据放在报告后半部分。

## 注意

- `/opt/multica/product` 和 `/opt/multica/school` 一律只读。
- 不读取/输出 jdbc 密码、证书、密钥。
- 4.0/4.6 客户不要直接与 4.7 当前标品做高置信度定制判断。
- 伪基线必须显式标注。
- `hutool`、类名、包名、XML 类型等纯技术项不得直接作为产品优化方向。
