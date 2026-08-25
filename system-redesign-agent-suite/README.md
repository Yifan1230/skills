# System Redesign Agent Suite

用于复杂旧系统改版的多 Agent / Skill 组合。

## 一、完整流水线

```text
代码逆向工程
      ↓
逆向业务模型
      ↓
定制应用分析
      ↓
产品能力抽象
      ↓
TO-BE业务设计
      ↓
UX/IA设计
      ↓
影响与迁移
      ↓
场景验收
```

由 `system-redesign-leader` 负责阶段控制、任务拆分、冲突处理和Gate验收。

---

## 二、你仓库中已有的上游能力

### 代码逆向工程

用途：获取现有系统技术事实、页面/API/字段/状态/隐藏逻辑等。

### 逆向业务模型

仓库已有：`code-to-business-model-cn-optimized-v2`

用途：从源码还原AS-IS业务对象、生命周期、规则、分支、场景和完整流程。

### 定制应用分析

仓库已有：`custom-product-analyzer-v0.4`

用途：比较不同客户/项目定制，发现重复差异和标品机会。

---

## 三、本次新增 Skill

### 1. `system-redesign-leader`

总控。

负责：
- 阶段判断
- Agent调度
- Gate
- 冲突
- Decision Log
- 主档

### 2. `product-capability-abstraction`

产品抽象。

负责把AS-IS和定制差异分类为：

```text
标准
配置
组合
扩展
定制
废弃
```

### 3. `to-be-business-design`

目标业务模型设计。

负责：
- 对象
- 生命周期
- 规则
- 角色
- 场景
- 完整流程

### 4. `product-ux-architecture`

业务模型稳定后进行体验设计。

负责：
- 角色任务
- 工作台
- IA
- 页面结构
- 多身份
- 数据到行动
- AI业务交互

### 5. `redesign-impact-migration`

负责旧系统升级：
- 对象/状态映射
- 历史数据
- 在途业务
- 配置/权限迁移
- 接口/报表影响
- 灰度/兼容/回滚

### 6. `scenario-validation`

产品级验收。

负责：
- AS-IS/TO-BE场景兼容
- 业务规则覆盖
- 状态/权限/配置覆盖
- 迁移验收
- 回归范围

---

## 四、SOP与阶段门

```text
Phase 0 改版立项

Phase 1 AS-IS系统摸底
→ Gate 1：现状是否足够清楚？

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

## 五、Agent职责边界

### 上游事实不能被下游静默修改

例如TO-BE Agent发现AS-IS结论可能错误时，应：

```text
提交冲突
→ Leader回派补证据
→ 更新AS-IS
```

而不是在TO-BE文档中直接改写旧系统事实。

### 不要全Agent机械串行

小问题只调用最小必要Agent。

完整模块重构才走完整流水线。

### FACT / INFERENCE / DESIGN分开

- FACT：已证实事实
- INFERENCE：合理推断
- DESIGN：未来方案

---

## 六、推荐主档结构

```text
system-redesign/
├── 00-project/
├── 01-as-is/
├── 02-custom-analysis/
├── 03-product-abstraction/
├── 04-to-be/
├── 05-impact-migration/
├── 06-validation/
└── 07-decisions/
```

Leader维护唯一最终口径。

---

## 七、推荐Agent配置

| Agent | 主Skill |
|---|---|
| 改版Leader | system-redesign-leader |
| 代码逆向工程 | 现有Code→PRD/代码逆向Skill |
| 逆向业务模型 | code-to-business-model-cn |
| 定制应用分析 | custom-product-analyzer |
| 产品抽象 | product-capability-abstraction |
| TO-BE设计 | to-be-business-design |
| UX/IA | product-ux-architecture |
| 影响迁移 | redesign-impact-migration |
| 场景验收 | scenario-validation |

建议每个专业Agent保持“一项主Skill + 少量辅助reference”，不要让所有Agent都安装所有Skill。