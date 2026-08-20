# custom-product-analyzer v0.4

Claude Code / Multica Skill，用于：

> 指定一个标品应用，横向扫描所有客户变体，从技术差异还原真正的业务产品问题，并输出产品经理可判断的标品优化方案。

## V0.4 核心

产品分析对象改为运行时 Behavior Delta：标品怎么运行、客户怎么运行、用户感知什么不同。代码差异仅作为证据附录。

核心链路：

```text
Technical Diff
→ Runtime Behavior
→ Behavior Delta
→ Feature
→ Product Problem
→ Ideal Product Behavior
```

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
业务场景
标品当前行为
客户版本行为
用户感知差异
共性问题
建议优化后的运行行为
证据客户
```

技术证据放在报告后半部分。

## 注意

- `/opt/multica/product` 和 `/opt/multica/school` 一律只读。
- 不读取/输出 jdbc 密码、证书、密钥。
- 4.0/4.6 客户不要直接与 4.7 当前标品做高置信度定制判断。
- 伪基线必须显式标注。
- 代码差异本身不能直接作为产品问题。
