# custom-product-analyzer

Claude Code / Multica Skill，用于：

> 指定一个标品应用，横向扫描所有客户变体，识别定制差异并输出标品优化机会。

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

## 注意

- `/opt/multica/product` 和 `/opt/multica/school` 一律只读。
- 不读取/输出 jdbc 密码、证书、密钥。
- 4.0/4.6 客户不要直接与 4.7 当前标品做高置信度定制判断。
- 伪基线必须显式标注。
