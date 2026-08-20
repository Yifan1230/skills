# Product Language Gate

## 强制规则

最终报告中的“产品经理决策区”必须通过自动校验。

决策区使用标记：

```md
<!-- PM_DECISION_START -->
...
<!-- PM_DECISION_END -->
```

该区域禁止出现以下内容：

### 内部分类枚举
- configuration_candidate
- productization_candidate
- strong_productization_candidate
- keep_custom
- observe

### 技术文件/模型后缀
- .java
- .epm / .epmx
- .edm / .edmx
- .eda
- .epg
- .jsp
- .xml（除非是用户明确讨论配置文件，但主报告原则上仍不应出现）

### 技术实现词作为产品方向
- hash
- hutool
- controller
- service
- dao
- jar
- sdk
- version drift / 版本漂移项
- CU-xxx / F-xxx

如果出现，`report_guard.py` 必须返回失败。

---

## 不是简单禁词，而是分层

技术信息可以出现在：

```text
技术证据附录
```

但不能出现在：

```text
产品问题
根因
优化方向
建议产品能力
```

---

## 产品语言最低要求

每个主表候选至少包含：

- 业务场景；
- 标品限制；
- 多客户共性；
- 产品根因；
- 建议产品能力。

若缺失，宁可写：

```text
业务语义不足，暂不形成产品建议
```

也不要用技术词硬凑结论。
