# Code → Business Model 

核心原则：

- `SKILL.md` 只保留主分析流程和强制规则；
- 具体判断方法拆到 `references/`；
- 示例拆到 `expected_outputs/`；
- `scripts/` 只做机械盘点，不直接判断业务；
- 默认不要求一次读取全部附件。

## 推荐优先阅读

1. `SKILL.md`
2. 当前阶段需要的一个 reference
3. 必要时查看一个 expected output 示例

不要一次把所有 reference 和示例全部塞进上下文。

## 最重要的分析主线

```text
系统模块
→ 业务对象
→ 生命周期
→ 业务规则
→ 条件分支
→ 业务场景
→ 完整流程
→ 权限/配置/异常
→ 页面映射
→ 覆盖检查
```
