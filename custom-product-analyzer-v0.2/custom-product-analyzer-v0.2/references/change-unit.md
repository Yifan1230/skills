# Change Unit

## 定义

Change Unit 是一组共同实现一次业务变化的技术改动。

不是：

```text
改了 5 个文件
```

而是：

```text
新增“按培养层次和年级控制选课限制”
```

## 聚合信号

强信号：

- EPG 引用 EDA
- EDA 引用 EPM
- EPM/EDA 引用 EDM
- 相同表/字段
- version.xml 对应新增表/字段
- permission.xml 对应同页面/动作

中信号：

- 同目录
- 同名前缀
- 相同 change_reference_id
- 相同业务词

弱信号：

- 纯文本相似

## Change Unit 输出

必须包含：

- change_unit_id
- customer
- app
- baseline_ref
- title
- technical_changes
- affected_pages
- affected_actions
- affected_models
- affected_tables
- affected_fields
- affected_permissions
- db_changes
- change_reference_ids
- inferred_business_change
- inference_type
- confidence
- evidence

## 合并原则

可以合并：

- 同一页面 + 同一 action + 同一表字段
- 同一次数据库升级 + 对应页面/动作
- 共同构成完整业务规则的多文件变化

不要合并：

- 仅仅同一目录
- 同一版本里完全无关的多个需求
- 纯样式和业务规则
