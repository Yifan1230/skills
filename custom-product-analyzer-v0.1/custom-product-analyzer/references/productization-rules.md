# Productization Rules

## 目标

不是“定制出现多次就进标品”。

需要判断它更像：

- 标品固定功能
- 参数化
- 配置化
- 规则引擎
- 流程配置
- 动态字段
- 权限配置
- 数据适配
- 保持客户定制

## 观察维度

### repeat_frequency
多少独立客户出现。

### cross_customer_generality
是否跨学校/客户仍是同一个业务问题。

### variant_diversity
同一 Feature 出现多少种变化形态。

高 variant diversity 往往意味着：
标品不应该继续硬编码一个“正确值”，而应建设可配置能力。

### maintenance_duplication
是否存在多套重复实现。

### standard_product_gap
当前标品是否明显把可变规则写死。

### customer_specificity
是否高度依赖某校政策、组织结构、数据接口。

### baseline_reliability
如果 baseline 很弱，产品判断也必须降级。

## 推荐枚举

- strong_productization_candidate
- productization_candidate
- configuration_candidate
- observe
- keep_custom

## 常见抽象模式

### 高频值变化
例：固定专家数反复变。

不要：
增加“3人”“5人”功能。

优先：
专家数量参数化。

### 高频维度变化
例：规则反复增加学院、年级、培养层次。

优先：
规则维度配置化。

### 高频流程节点变化
优先：
流程配置化，而不是继续复制流程。

### 高频字段变化
先判断：
是否动态字段/表单配置问题。

### 高频权限变化
先判断：
是否权限模型粒度不足。

## 反证要求

每个推荐必须回答：

- 为什么不应继续定制？
- 为什么不应该只加一个固定功能？
- 有没有客户特有政策解释？
- 是否会显著增加标品复杂度？
