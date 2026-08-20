---
name: custom-product-analyzer
description: 横向分析某个标品应用在多个客户中的定制变体，从技术差异还原业务场景、真实产品问题、Feature Variant 与标品优化方案。输出优先使用产品经理可判断的业务语言，并保留从产品结论回溯到代码证据的链路。适用于 EMAP/Java/JSP/XML 类产品，尤其适合“一个标品应用对应大量客户定制版本”的场景。
---

# Custom Product Analyzer

## V0.4 核心变化：以运行时业务行为为分析核心

V0.3 仍可能出现一个问题：

```text
代码变了
→ Feature 变了
→ 再翻译成产品语言
```

这仍然是“代码中心”。

V0.4 强制改成：

```text
代码差异（只做证据）
↓
运行时行为还原
↓
标品行为 vs 客户行为
↓
用户可感知差异
↓
业务结果差异
↓
Feature / 产品问题
↓
标品优化后的理想运行行为
```

**产品分析的第一对象是 Behavior Delta，不是文件 Diff。**

任何正式产品结论都必须先回答：

1. 标品运行时怎么做；
2. 客户版本运行时怎么做；
3. 用户实际感知的不同是什么。

如果回答不了，不能进入产品建议。

详见：

- `references/runtime-behavior-analysis.md`
- `references/behavior-recovery-pass.md`
- `templates/behavior-delta.schema.json`

## 目标

对**一个指定标品应用**进行横向扫描：

`标品应用 → 客户变体 → 版本分组 → Baseline → 结构差异 → Change Unit → Feature → Feature Variant → 产品化机会`

本 Skill 的目标不是“找出所有文件差异”，而是：

1. 找出真正值得分析的客户变体；
2. 尽量避免把版本升级、分发差异、部署配置、Bug Fix、技术重构误判为产品定制；
3. 将多个技术差异聚合为可解释的 `Change Unit`；
4. 将 Change Unit 还原为业务 Feature / Feature Variant；
5. 跨客户识别重复定制、共同变化方向和底层能力缺口；
6. 将技术变化进一步还原为“业务场景 → 产品问题 → 根因 → 优化目标 → 产品能力方案”；
7. 为标品优化、配置化、规则化、平台化提供**产品经理可判断的证据化建议**。

---

# 使用方式

推荐用户输入：

```text
分析应用：xkglapp
```

也可附加：

```text
分析应用：xkglapp
客户范围：全部
深度：poc / full
输出目录：product-intelligence/
```

默认值：

- `product_root=/opt/multica/product/gsapp_xjpy/app`
- `school_root=/opt/multica/school`
- `output_root=product-intelligence`
- `depth=poc`
- 一次只深入分析一个标品应用
- 标品和客户代码一律视为只读

---

# 绝对规则

## 1. 应用中心，而不是客户中心

禁止先选客户再分析全部应用。

必须先确定一个 `canonical_app`，再横向扫描所有客户中的对应变体。

正确：

```text
xkglapp
├─ 学校A/xkglapp
├─ 学校B/xkglapp$A
├─ 学校C/xkglappbit
├─ 学校D/R106_XKGL/xkglapp
└─ 学校E/xkglapp
```

错误：

```text
学校A → 扫全部应用
学校B → 扫全部应用
```

---

## 2. 不把“当前标品”默认当历史客户的真实 Baseline

Baseline 分三级：

### Level A — true_baseline

存在客户对应历史标品版本，可直接比较。

### Level B — consensus_pseudo_baseline

没有真实历史标品时：

- 同 application version
- 尽量同 emap_version
- 同 change_reference_id / version.json 参考号优先
- 多客户文件 Hash 高度一致

使用多数一致内容重建“共识伪基线”。

必须明确标记它是推断出的伪基线，不能伪装成真实标品。

### Level C — no_reliable_baseline

找不到可靠历史标品或共识基线。

此时：

- 不允许输出高置信度“这是客户定制”的文件级结论；
- 只能输出“与当前标品/同组客户存在差异”；
- 结论置信度不得高于 medium。

详见 `references/baseline-strategy.md`。

---

## 3. 不把需求号直接当 Feature ID

`version.json`、目录 R 编号、Git/SVN 工单号等统一记录为：

```text
change_reference_id
```

只有在人工确认其确实代表业务 Feature 后，才可升级为 Feature ID。

---

## 4. 所有产品判断必须有证据

所有 Feature、Feature Variant、产品化建议必须保存：

- evidence
- inference_type
- confidence
- baseline_quality

`inference_type` 仅允许：

- `code_fact`
- `document_fact`
- `agent_inference`
- `human_confirmed`

不要把 Agent 推断写成代码事实。

---

## 5. 最终输出必须使用产品语言

技术分析是中间过程，不是最终产品结论。

最终“产品方向/产品化建议”部分必须做到：

- 先讲业务场景和角色；
- 再讲当前标品造成的限制；
- 再讲多个客户为何反复定制；
- 再抽象出产品能力根因；
- 最后给出用户未来能怎么用、产品应该增加什么能力。

禁止仅用下面内容作为产品方向：

- `configuration_candidate` / `observe` / `keep_custom`；
- Java/XML/SQL/表名/字段名；
- 工具库、类名、技术模块名；
- “版本漂移项”这类无法直接说明业务问题的名称。

如果无法从技术证据还原出用户角色、业务场景和标品限制，应将其放入“技术差异/业务语义待确认”，而不是硬生成产品方向。

详见 `references/product-problem-analysis.md`。

---

## 6. 安全边界

禁止读取或输出敏感文件内容：

- `*/com/ROOT/jdbc.properties`
- `*/ROOT/`
- `*/server/`
- `.svn/`
- `lib/`
- `.sonar/`
- `classes/`
- `pub_classes/`
- 明确的证书、密钥、密码文件
- `app_info.xml` 中 `<cer>` 的内容不得输出

允许读取 `app_info.xml` 的非敏感元数据，如：

- application version
- emap_version
- identity

如输出 XML 摘要，必须主动过滤 `password/secret/token/key/cer` 等字段。

不得修改 `/opt/multica/product` 和 `/opt/multica/school` 中的源文件。

---

# 总流程

## Stage 0 — 参数与安全检查

确认：

- canonical_app
- product_root
- school_root
- output_root
- depth

创建：

```text
<output_root>/apps/<canonical_app>/
```

子目录：

```text
inventory/
baselines/
normalized/
diffs/
change-units/
features/
matrix/
reports/
logs/
```

---

## Stage 1 — Variant Inventory

运行：

```bash
python3 scripts/inventory.py \
  --app <canonical_app> \
  --product-root /opt/multica/product/gsapp_xjpy/app \
  --school-root /opt/multica/school \
  --output <output_root>/apps/<canonical_app>/inventory/variant_inventory.json
```

匹配顺序：

1. exact-name
2. `$A-extension`
3. school-suffix-copy
4. R-directory
5. identity-match
6. uncertain

参照 `references/variant-taxonomy.md`。

必须生成：

- 客户
- 实际应用名
- 路径
- app version
- emap_version
- identity
- change_reference_id
- variant_type
- match_evidence
- match_confidence

---

## Stage 2 — Version Grouping & Baseline Resolution

运行：

```bash
python3 scripts/baseline_resolver.py \
  --inventory <variant_inventory.json> \
  --product-app <product_app_path> \
  --output-dir <output_root>/apps/<canonical_app>/baselines
```

处理逻辑：

1. 按 application version 主版本分组；
2. emap_version 作为辅助；
3. change_reference_id 作为强聚类线索，但不是 Feature；
4. 若存在 true baseline 则优先；
5. 否则在组内寻找文件 hash 多数一致簇，构造 pseudo baseline；
6. 记录 baseline 证据和置信度。

---

## Stage 3 — Fast Diff

目标：先缩小搜索范围，不让 LLM 阅读全量文件。

排除：

- `.svn`
- ROOT/server/lib/classes/pub_classes
- node_modules
- 二进制
- 图片/字体
- 纯构建产物

优先纳入：

- `.epg`
- `.epm/.epmx`
- `.edm/.edmx`
- `.eda`
- `.dic`
- `permission.xml`
- `version*.xml`
- `.java`
- `.jsp`
- `.js`
- `.html`

运行：

```bash
python3 scripts/file_diff.py \
  --baseline <baseline_path_or_manifest> \
  --variant <variant_path> \
  --output <diff.json>
```

只保留：

- added
- removed
- modified
- renamed_like
- structural_summary

---

## Stage 4 — XML / EMAP 结构化

不要让 LLM 直接生啃大量 XML。

对每个发生变化的 EMAP 文件先运行：

```bash
python3 scripts/xml_parser.py \
  --input <file_or_dir> \
  --output <normalized.json>
```

输出尽量统一为：

```json
{
  "file_type": "eda|epg|epm|edm|dic|permission|version|xml",
  "entities": [],
  "references": [],
  "tables": [],
  "fields": [],
  "actions": [],
  "pages": [],
  "permissions": [],
  "db_changes": []
}
```

解析失败时保留：

```json
{
  "parse_status": "partial",
  "raw_tags": []
}
```

不要因单个 XML 格式异常终止整个流程。

---

## Stage 5 — Change Unit 构建

Change Unit 是本 Skill 最重要的中间产物。

技术文件不是最终分析单位。

示例：

```text
EPG 页面变化
+ EDA 新增 action
+ EPM 模型变化
+ EDM 新字段
+ version.xml DDL
```

应尝试聚合为一个：

```text
CU-xxx：选课限制新增年级/培养层次维度
```

运行初步图构建：

```bash
python3 scripts/change_graph.py \
  --normalized-dir <normalized_dir> \
  --diff-dir <diff_dir> \
  --output <change_graph.json>
```

然后由 Agent 进行语义聚合。

聚合依据优先级：

1. 显式引用关系；
2. 相同表/字段；
3. 相同 action/page/model 名；
4. 相同目录/模块；
5. 相同 change_reference_id；
6. 词义相似；
7. Agent 推断。

每个 Change Unit 必须符合 `templates/change-unit.schema.json`。

详见 `references/change-unit.md`。

---

## Stage 6 — Runtime Behavior Recovery

这是 V0.4 的核心阶段。

**Change Unit 不能直接进入 Feature Recovery。**

先根据：

- 页面文字
- 按钮/字段
- 查询条件
- SQL where
- 校验提示
- 权限
- 流程
- 默认值
- 返回结果

还原运行行为。

按照：

```text
references/behavior-recovery-pass.md
```

生成：

```text
templates/behavior-delta.schema.json
```

每个 Behavior Delta 必须明确：

```text
business_scenario
standard_behavior
variant_behavior
user_visible_difference
```

其中至少后三项清晰，才允许继续。

### 示例

禁止：

```text
客户修改了 XsmdImportValidate.java
```

必须继续追踪到：

```text
标品运行时：
管理员导入名单时，可选择/可导入的学生范围是什么。

客户版本运行时：
可选择/可导入的学生范围变成什么。

用户感知：
哪些学生原来不能导入、现在可以；或者反过来。
```

如果无法确认：

```text
behavior_status=insufficient_evidence
```

并停止对该项做 Feature/Product Problem 推导。

详见 `references/runtime-behavior-analysis.md`。

---

## Stage 7 — Feature Recovery from Behavior

Feature 必须从 Behavior Delta 中恢复，而不是直接从文件差异恢复。

链路：

```text
Behavior Delta
↓
Business Feature
↓
Feature Variant
```

例如：

```text
标品：
选课限制对所有学生使用同一套条件

客户A：
按年级采用不同条件

客户B：
按培养层次采用不同条件

↓
Feature：
选课限制规则

Feature Variants：
全局固定 / 按年级 / 按培养层次
```

只有 `behavior_status=confirmed/probable` 才可进入 Feature Recovery。

技术文件、字段、类名不能直接成为 Business Feature。

---

## Stage 8 — Cross-Variant Behavior Clustering

优先将不同客户的 **Behavior Delta** 聚类，再映射到 Feature / Feature Variant。

重点不是“实现代码相似”，而是“运行时行为是否发生了同类变化，以及是否在解决同一个业务问题”。

例如：

```text
客户A：专家人数按项目类型
客户B：专家人数按批次
客户C：专家人数按学院
```

应聚类到：

```text
Feature：专家人数规则
Feature Variants：
- 项目类型级
- 批次级
- 学院级
```

再进一步识别：

```text
底层问题：专家人数配置粒度被写死
```

聚类时同时参考：

- Feature 名称语义；
- 表/字段；
- 页面/Action；
- change_reference_id；
- 业务对象；
- 规则结构；
- 客户出现模式。

---

## Stage 9 — Product × Behavior / Feature Matrix

运行：

```bash
python3 scripts/build_matrix.py \
  --features-dir <features_dir> \
  --output <matrix.csv>
```

矩阵至少表达：

```text
customer
actual_app
version
feature_id
feature_name
variant_name
presence
confidence
baseline_quality
```

不要只做 0/1。

优先保留 Feature Variant 内容。

---

## Stage 10 — Business Evidence Pack

在做产品判断前，先补充业务语义证据。

对高频/高价值 Feature Cluster 的变体，运行：

```bash
python3 scripts/business_semantics.py \
  --input <diff.json> \
  --variant-root <variant_path> \
  --output <business-evidence.json>
```

优先收集：

- 页面/菜单名称
- 按钮
- 字段中文名
- 错误提示
- 字典
- 权限名称
- JS/JSP/EPG 用户可见中文
- 表字段注释
- Change Reference 描述

不要只给 Product Analyst 看文件名和类名。

---

## Stage 11 — Product Analyst Pass

这是独立于技术分析的第二遍分析。

输入：

- Behavior Delta Cluster
- Feature Cluster
- Change Unit 摘要（仅作证据）
- Business Evidence Pack
- 客户差异
- Baseline 质量

按照 `references/product-analyst-pass.md` 工作。

严格输出：

```text
templates/product-problem-card.schema.json
```

每个候选必须得到四种状态之一：

- `ready_for_pm`
- `needs_business_confirmation`
- `technical_only`
- `version_noise`

### ready_for_pm 门槛

必须能回答：

1. 谁；
2. 在什么业务场景；
3. 标品当前有什么限制；
4. 至少两个客户的业务变化是什么；
5. 共同产品根因是什么；
6. 建议建设什么产品能力。

如果只能说：

```text
某 Java 文件被修改
某视图被替换
某工具库被引入
```

则不得进入 `ready_for_pm`。

如果知道多个客户实现不同，但不知道这种不同具体代表什么业务规则，则必须进入：

```text
needs_business_confirmation
```

**不要猜。**

---

## Stage 12 — PM Report Generation + Hard Validation

最终报告必须基于：

```text
templates/product-manager-report-template.md
```

而不是沿用旧的 Feature/技术分类表。

产品经理主报告只读取：

```text
Product Problem Cards where decision_status=ready_for_pm
```

其他内容分别进入：

- 业务语义待确认；
- 技术差异附录；
- 版本噪声。

报告生成后必须运行：

```bash
python3 scripts/report_guard.py \
  --report reports/<canonical_app>-productization-report.md
```

如果返回失败：

**不得把报告交付给用户。**

必须根据错误重写 `<!-- PM_DECISION_START -->` 与 `<!-- PM_DECISION_END -->` 之间的内容，直到校验通过。

### 主报告禁止项

不得出现：

- Feature 作为主表第一列；
- configuration_candidate / observe / keep_custom；
- F-xxx / CU-xxx；
- .java / .epm / .eda / .edm / .epg；
- hash；
- hutool；
- “版本漂移项”；
- 只有技术模块名、没有业务含义的标题。

### 产品主表必须是

| 业务场景 | 标品当前行为 | 客户版本行为 | 用户感知差异 | 共性问题 | 建议优化后的行为 | 证据客户 |
|---|---|---|---|---|---|---|

产品问题必须写成：

```text
<业务场景> + <标品限制/业务后果>
```

建议产品能力必须说明：

- 谁使用；
- 在哪里使用；
- 能配置/执行什么；
- 作用于什么范围；
- 解决什么问题。

详见 `references/product-problem-synthesis.md`。

# 深度模式

## poc

用于首次验证。

建议：

- 优先 true baseline；
- 其次 4.6/4.7 近版本；
- 4.0 只抽取有高一致共识基线的代表簇；
- 加入少量明显定制客户；
- 验证完整链路是否准确。

目标不是覆盖所有客户，而是验证：

`Variant → Baseline → Diff → CU → Feature → Cluster → Productization`

## full

前提：

- poc 已人工验收；
- Feature Dictionary 已有一定基础；
- Baseline 策略已验证。

full 才允许扫描全部有效变体。

---

# 子 Agent 使用原则

允许使用 Explore / Plan / general-purpose 子代理，但必须满足：

1. 子 Agent prompt 必须自包含；
2. 不让子 Agent 扫全部客户；
3. 每个子 Agent 只处理：
   - 一个客户变体；或
   - 一个 Change Unit 集合；或
   - 一个 Feature Cluster；
4. 子 Agent 输出必须是结构化 JSON/Markdown；
5. 主 Agent 负责最终合并和冲突消解。

推荐 Map-Reduce：

```text
Variant A → 子Agent → Change Units
Variant B → 子Agent → Change Units
Variant C → 子Agent → Change Units
...
             ↓
主Agent聚合 Feature
             ↓
Feature Cluster 子Agent
             ↓
主Agent产品化分析
```

---

# 长期资产

Skill 本体与分析数据分离。

建议长期维护：

```text
product-intelligence/
├─ apps/
│  ├─ xkglapp/
│  ├─ pyfaglapp/
│  └─ ...
├─ feature-dictionary.json
├─ productization-backlog.json
└─ analysis-index.json
```

`feature-dictionary.json` 允许逐步成长，不要求一开始完整。

新客户/新版本应支持增量分析。

---

# 最终报告格式

报告生成：

```text
reports/<canonical_app>-productization-report.md
```

**必须直接使用 `templates/product-manager-report-template.md` 的章节结构。**

不允许自由发挥成旧式：

```text
高频重复定制方向
产品化建议摘要
Feature | 建议 | 置信度
```

这种结构属于 V0.1/V0.2 失败输出。

## 决策区

必须包含：

```md
<!-- PM_DECISION_START -->
...
<!-- PM_DECISION_END -->
```

并通过：

```bash
python3 scripts/report_guard.py --report <report>
```

## 产品经理真正看到的顺序

1. 产品经理结论；
2. 正式产品优化候选；
3. 候选问题详情；
4. 业务语义不足、待确认；
5. 明确保持定制的业务需求；
6. 技术证据附录。

## 关键原则

**技术证据的价值是支撑产品结论，不是占据产品结论。**

任何产品结论都必须可回溯：

```text
产品问题
→ Feature Cluster
→ Change Unit
→ 客户 Variant
→ Baseline
→ 文件/模型/动作
```

但主报告阅读方向必须是反过来的：

```text
先理解产品问题
↓
再决定要不要做
↓
需要时再查看技术证据
```

# xkglapp PoC 已知条件

首次运行可使用以下已验证事实作为测试输入，但不要硬编码到通用逻辑：

- canonical app：`xkglapp`
- 客户覆盖约 45
- 变体约 49
- 存在：
  - 同名
  - `$A`
  - school suffix
  - R-directory
- 主版本：
  - 4.0.1_TR1
  - 4.6.x
  - 4.7.1_R1
- 当前标品为 4.7.1_R1
- 本地无法恢复 4.0/4.6 的真实历史标品
- 4.0 可尝试基于同版本、同 change_reference_id、文件 hash 多数一致构造共识伪基线

---

# 完成标准

一次分析只有满足以下条件才算完成：

- [ ] 已生成 Variant Inventory
- [ ] 每个深度分析变体都有 Baseline 结论
- [ ] 已排除敏感路径
- [ ] 差异已先结构化而非直接全量喂给 LLM
- [ ] 至少形成 Change Unit
- [ ] Change Unit 已还原为 Feature / Feature Variant
- [ ] 跨客户完成聚类
- [ ] 产品化建议带证据、反证、置信度
- [ ] 每个进入主表的候选都已还原成“业务场景 → 产品问题 → 根因 → 优化目标 → 产品能力方案”
- [ ] 最终主表未使用 configuration_candidate/keep_custom 等内部枚举作为主结论
- [ ] 已生成 Product Problem Cards，且主表只使用 ready_for_pm 项
- [ ] 业务语义不足项已进入 needs_business_confirmation，而不是硬生成产品故事
- [ ] 已运行 report_guard.py 且返回 PASS
- [ ] 纯技术实现差异已从“产品方向”中剔除
- [ ] 伪基线明确标注
- [ ] 输出待人工确认事项


# V0.4 额外完成门槛

- [ ] 每个正式产品候选都有 Behavior Delta
- [ ] 已明确“标品当前行为”
- [ ] 已明确“客户版本行为”
- [ ] 已明确“用户可感知差异”
- [ ] 纯代码变化但运行行为不明的项，没有进入产品建议
- [ ] 多客户聚类以 Behavior Delta 为主，而非文件名/类名相似
- [ ] 产品建议描述了“优化后系统应该怎么运行”，而不仅是“做配置化”
