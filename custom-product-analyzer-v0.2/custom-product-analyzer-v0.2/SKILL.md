---
name: custom-product-analyzer
description: 横向分析某个标品应用在多个客户中的定制变体，从技术差异还原业务场景、真实产品问题、Feature Variant 与标品优化方案。输出优先使用产品经理可判断的业务语言，并保留从产品结论回溯到代码证据的链路。适用于 EMAP/Java/JSP/XML 类产品，尤其适合“一个标品应用对应大量客户定制版本”的场景。
---

# Custom Product Analyzer

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

## Stage 6 — Feature Recovery

对 Change Unit 做业务还原。

必须区分四层：

```text
技术差异
↓
Change Unit
↓
Business Feature
↓
Feature Variant
```

示例：

```text
技术：
新增 PYCC / NJ 条件字段

Change Unit：
选课限制增加培养层次和年级

Business Feature：
选课限制规则

Feature Variant：
按培养层次 + 年级控制
```

不要将“字段”“接口”“类”直接作为 Business Feature。

Feature 命名原则：

- 使用业务语言；
- 优先“对象 + 行为/规则”；
- 避免 Java/XML 技术词；
- 无法确认业务语义时标 `agent_inference`；
- 保留技术证据回链。

---

## Stage 7 — Cross-Variant Clustering

将不同客户的 Feature / Feature Variant 聚类。

重点不是“实现代码相似”，而是“是否在解决同一个产品问题”。

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

## Stage 8 — Product × Feature Matrix

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

## Stage 9 — Product Problem Recovery & Productization Analysis

这一阶段必须从“技术变化”继续向上抽象到**产品经理可以直接判断的问题和方案**。

禁止停在下面这种输出：

```text
Feature：学生名单导入验证规则
建议：configuration_candidate
```

这只是内部技术分类，不是最终产品结论。

必须完成下面的翻译链：

```text
技术变化
→ 用户可感知的行为变化
→ 业务场景
→ 使用角色/管理角色
→ 现有标品带来的业务问题
→ 为什么客户不得不定制
→ 共性的产品能力缺口
→ 产品优化目标
→ 可落地的产品方案
```

例如：

```text
技术事实：
多个客户在学生名单导入中增加不同字段校验和业务判断。

不要输出：
“学生名单导入验证规则 → configuration_candidate”

应输出：
产品问题：
标品的学生名单导入校验规则较固定，不同学校在学籍状态、培养层次、名单范围等方面存在不同准入要求，实施时只能通过定制代码补充校验，导致同类需求重复开发。

优化目标：
让管理员能够按学校业务规则配置“哪些学生允许被导入、什么情况阻止导入、异常如何提示”，避免每新增一种校验都改代码。

建议方案：
在学生名单导入功能中增加“导入校验规则配置”，至少支持校验条件、阻断/提醒级别、提示语和适用范围；具体支持哪些维度应根据已出现的客户变体进一步确认。
```

### 9.1 产品问题识别门槛

每个候选项必须先回答：

1. **谁在什么业务场景下遇到问题？**
2. **当前标品为什么不能满足？**
3. **客户通过什么定制绕过了这个限制？**
4. **多个客户的变化是否指向同一个共性问题？**
5. **如果去掉代码/表名/框架名，这个问题还能否用业务语言讲清楚？**

如果第 1、2、5 条无法回答，不得进入“产品优化方向”主表，只能进入：

- `技术差异/实现特例`
- `业务语义不足，待确认`

例如 `hutool 嵌入`、第三方工具类替换、仅有包名/类名变化，默认不是产品问题。

### 9.2 产品问题卡片

对每个真正的产品候选必须生成 `Product Problem Card`：

- `product_problem_title`：一句业务语言标题，禁止技术名；
- `business_scenario`：发生在哪个业务环节；
- `actor`：谁使用/管理；
- `current_standard_behavior`：当前标品如何工作；
- `customer_variations`：客户分别改成了什么；
- `user_or_business_problem`：标品造成的实际限制/成本/风险；
- `root_product_gap`：标品能力层面缺什么，而不是代码缺什么；
- `optimization_goal`：希望产品达到什么状态；
- `proposed_product_capability`：建议建设的产品能力；
- `scope_or_config_dimensions`：目前证据支持哪些可变维度；
- `product_value`：减少什么重复工作或改善什么业务；
- `evidence` / `counter_evidence`；
- `confidence`；
- `human_confirmation_needed`。

### 9.3 内部分类与用户可见表达分离

内部仍可使用：

- `strong_productization_candidate`
- `productization_candidate`
- `configuration_candidate`
- `observe`
- `keep_custom`

但**最终产品报告不得只显示这些枚举**。

用户可见的“建议类型”必须翻译为：

- `strong_productization_candidate` → `高优先级标品优化`
- `productization_candidate` → `建议纳入标品能力`
- `configuration_candidate` → `建议做成可配置能力`
- `observe` → `证据不足，继续观察`
- `keep_custom` → `建议保持定制/技术特例`

并且“建议类型”只能作为辅助标签，主结论必须是**产品问题 + 优化目标 + 具体能力方案**。

### 9.4 产品化判断维度

针对每个 Feature / Feature Cluster，评估：

- repeat_frequency
- cross_customer_generality
- variant_diversity
- maintenance_duplication
- standard_product_gap
- customer_specificity
- implementation_consistency
- baseline_reliability

第一版不要使用伪精确的固定权重公式。

必须考虑反例：

> 高频 ≠ 一定产品化。

例如某些高校政策导致同类定制高频，但本质仍是学校制度差异，则更适合把差异设计成可配置项，而不是把某一种学校规则固定进标品。

详见：

- `references/product-problem-analysis.md`
- `references/productization-rules.md`

---

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

生成：

```text
reports/<canonical_app>-productization-report.md
```

报告必须同时提供两层视图：

## A. 产品经理视图（放最前面）

这一部分默认不展示代码、类名、XML 类型、英文枚举。

首先给出“产品问题与优化建议”主表：

| 产品问题 | 业务场景/影响 | 客户定制共性 | 根因判断 | 优化方向 | 建议类型 | 证据客户 | 置信度 |
|---|---|---|---|---|---|---|---|

要求：

- `产品问题` 必须描述“标品在哪个业务场景存在什么限制”，而不是 Feature 名；
- `根因判断` 必须是产品能力缺口，如“规则写死”“配置粒度不足”“流程节点强绑定”“字段不可扩展”，不能写 Java/XML 原因；
- `优化方向` 必须描述用户未来可以做什么、产品应提供什么能力；
- 技术实现名不得出现在主表标题或产品问题中；
- 无法还原成业务问题的技术变化不得进入主表。

对 P0/P1 或高价值候选，再展开 Product Problem Card：

```text
产品问题：
谁在什么场景下，因标品什么限制而必须采用人工处理或定制。

现有客户怎么改：
A客户……
B客户……
C客户……

根因：
标品在产品能力层面缺少……

优化目标：
未来管理员/教师/学生能够……

建议方案：
产品增加……能力，支持……；当前证据支持的配置维度包括……

产品价值：
减少重复定制/降低实施成本/适应不同学校规则/降低操作风险……

仍需确认：
……
```

## B. 技术证据视图（放后面）

至少包含：

1. 应用概览；
2. Variant Inventory；
3. Baseline 质量分布；
4. 主要 Change Units；
5. Feature Dictionary；
6. Feature Variant 分布；
7. Product × Feature Matrix 摘要；
8. 技术差异/实现特例；
9. 证据索引；
10. 待人工确认问题。

任何产品结论都必须可以追溯到：

```text
客户 → 实际应用 → Baseline → 文件 → 结构化差异 → Change Unit → Feature → 产品问题 → 优化方案
```

---

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
- [ ] 纯技术实现差异已从“产品方向”中剔除
- [ ] 伪基线明确标注
- [ ] 输出待人工确认事项
