# System Redesign Agent Suite

用于复杂旧系统改版的多 Agent / Skill 组合。

## 一、完整流水线

```text
代码逆向工程（技术事实层）
      ↓
逆向业务模型（业务语义翻译）
      ↓
定制应用分析（业务差异）
      ↓
产品能力抽象
      ↓
TO-BE业务设计
      ↓
UX / IA设计
      ↓
影响与迁移
      ↓
场景验收
```

由 `system-redesign-leader` 负责阶段控制、任务拆分、冲突处理、产品可读性 Gate 和最终验收。

---

## 二、最重要的体系规则：技术事实层与产品业务层分离

### 技术事实层

代码逆向 Agent 可以输出：

- 字段名；
- 表名；
- 方法名；
- 接口；
- 状态码；
- SQL；
- 调用关系；
- 技术实现。

这些用于证明“系统实际上做了什么”。

### 产品业务层

从“逆向业务模型”开始，主输出必须转换为：

- 业务目的；
- 角色；
- 业务对象；
- 业务状态；
- 业务动作；
- 业务规则；
- 业务场景；
- 业务结果；
- 异常和恢复。

字段、表、方法、状态码等只能存在于“技术证据/附录”，不能出现在产品主文档。

详细契约见：

`PRODUCT-READABILITY-CONTRACT.md`

---

## 三、Agent 角色

### 1. 代码逆向工程

职责：提供准确技术事实和证据。

它可以技术化，因为它不是最终产品业务文档。

### 2. 逆向业务模型

仓库已有：`code-to-business-model-cn-optimized-v2`

职责：完成最关键的翻译：

```text
技术事实
→ 业务含义
→ 业务对象/规则/场景/流程
```

如果输出仍是“半中文半代码”，视为失败。

### 3. 定制应用分析

仓库已有：`custom-product-analyzer-v0.4`

职责：比较客户/项目差异。

进入产品抽象前，应把差异归纳成业务差异，例如流程差异、规则差异、权限差异、配置差异，而不是只列字段和代码改动。

### 4. `product-capability-abstraction`

将业务能力和客户差异分类为：

```text
标准 / 配置 / 组合 / 扩展 / 定制 / 废弃
```

### 5. `to-be-business-design`

设计目标业务对象、生命周期、规则、角色、场景和完整流程。

### 6. `product-ux-architecture`

在业务模型稳定后设计工作台、IA、页面结构、任务路径、多身份、数据到行动和AI交互。

### 7. `redesign-impact-migration`

分析新旧业务映射、历史数据、在途业务、配置/权限、客户切换、兼容和回滚。

### 8. `scenario-validation`

使用业务场景和业务规则做产品级验收，不以“字段正确/接口成功”代替业务验收。

---

## 四、SOP 与阶段门

```text
Phase 0 改版立项

Phase 1 AS-IS系统摸底
→ Gate 1A：产品主文档是否可读？
→ Gate 1B：AS-IS业务模型是否完整？

Phase 2 定制差异分析
Phase 3 产品能力抽象
→ Gate 2：产品边界是否稳定？

Phase 4 TO-BE业务设计
Phase 5 UX/IA设计
→ Gate 3：是否达到研发输入条件？

Phase 6 影响与迁移
Phase 7 场景验收
→ Gate 4：是否达到发布/实施准备条件？
```

---

## 五、产品可读性 Gate

以下内容如果出现在产品主文档，默认退回：

```text
SFXS
ZT=99
T_XXX
validateCanEdit()
doAzpy()
A<>B
字段A=1
接口编码
SQL条件
```

除非明确放在“技术证据/技术附录”。

例如：

### 不合格

```text
选择周次 → newzcbh → doAzpy → 写T_XXX
```

### 合格

```text
选择需要整体调整的教学周
→ 系统计算受影响课程
→ 用户预览调整结果
→ 确认执行
→ 更新课程安排并保留调整记录
```

正确但看不懂，对产品仍然没有价值。

---

## 六、Agent 职责边界

### 上游事实不能被下游静默修改

TO-BE发现AS-IS可能错误时：

```text
提交冲突
→ Leader回派补证据
→ 业务逆向重新翻译
→ 更新AS-IS
```

### 不要全 Agent 机械串行

小问题调用最小必要 Agent；完整模块重构才走完整流水线。

### FACT / INFERENCE / DESIGN 分开

- FACT：已证实事实；
- INFERENCE：合理推断；
- DESIGN：未来方案。

---

## 七、推荐主档结构

```text
system-redesign/
├── 00-project/
├── 01-as-is/
├── 02-custom-analysis/
├── 03-product-abstraction/
├── 04-to-be/
├── 05-ux/
├── 06-impact-migration/
├── 07-validation/
└── 08-decisions/
```

Leader维护唯一最终口径。

技术证据建议单独放在各阶段的 `evidence/` 或 `technical-*` 子目录中。

---

## 八、推荐 Agent 配置

| Agent | 主 Skill |
|---|---|
| 改版Leader | system-redesign-leader |
| 代码逆向工程 | 现有 Code→PRD / 代码逆向 Skill |
| 逆向业务模型 | code-to-business-model-cn |
| 定制应用分析 | custom-product-analyzer |
| 产品抽象 | product-capability-abstraction |
| TO-BE设计 | to-be-business-design |
| UX/IA | product-ux-architecture |
| 影响迁移 | redesign-impact-migration |
| 场景验收 | scenario-validation |

建议每个专业 Agent 保持“一项主 Skill + 少量 references”，不要让所有 Agent 都安装全部 Skill。