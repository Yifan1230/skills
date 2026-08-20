# Feature Model

## 四层语义

### 1. Technical Change
字段、Action、页面、SQL、权限、Java 方法变化。

### 2. Change Unit
一次相对完整的业务变化。

### 3. Business Feature
稳定的产品能力概念。

示例：

- 选课限制规则
- 退课规则
- 选课时间控制
- 容量控制
- 冲突校验

### 4. Feature Variant
同一 Feature 在客户中的具体变化形态。

例如：

```text
Feature：选课限制规则

Variant A：按年级
Variant B：按培养层次
Variant C：按学院
Variant D：年级 + 培养层次 + 学院
```

## Feature 关系

后续可以维护：

- mandatory
- optional
- requires
- excludes
- alternative
- configuration_dimension

第一版不强制恢复完整 Feature Model，优先把 Feature / Variant 做准。
