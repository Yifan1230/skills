# Baseline Strategy

## 为什么 Baseline 是第一优先级

客户版本 4.0 与当前标品 4.7 做直接 diff，会混入：

- 标品后续新增
- 标品 Bug Fix
- 框架升级
- 重构
- 真定制

所以必须先回答：

> 这个客户变体应该和哪个“当时的标品”比较？

## 三级 Baseline

### A. true_baseline

来源：

- 产品 Git 历史
- Release Tag
- 历史快照
- 官方归档版本

要求记录：

- source
- version
- commit/tag/path
- confidence=high

### B. consensus_pseudo_baseline

当真实历史标品缺失时：

1. 同 application version 分组；
2. emap_version 尽量相同；
3. change_reference_id 相同优先；
4. 计算相对安全文件的 Hash；
5. 找多数一致簇；
6. 选择多数内容作为“共识基线”。

注意：

- 它不是历史标品事实；
- 可能多个客户恰好共享同一批定制；
- 所以默认 confidence=medium；
- 若 change_reference_id 官方确认是“原版分发号”，可提高。

### C. no_reliable_baseline

无历史标品，也无足够一致客户簇。

处理：

- 只做结构差异和异常识别；
- 不做高置信度“定制”结论；
- 产品化建议最多 medium confidence。

## 伪基线最低要求

建议至少：

- 3 个来源；
- 关键业务文件中超过 70% Hash 一致；
- application version 相同；
- 无明显校名后缀或独立定制信号。

不足时应拒绝构造伪基线。
