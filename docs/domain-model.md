# 领域模型与模块边界

## 1. 任务域

- `Employee`：人员身份、角色、技能和管理范围；
- `TaskTemplate`：重复简单任务的规则；
- `Task`：每次实际任务实例；
- `Assignment`：任务与执行人的多对多关系；
- `TaskUpdate`：员工反馈和状态事实；
- `Project`：复杂项目主档；
- `ProjectUpdate`：项目进度、风险、阻塞和建议；
- `Milestone`：复杂项目里程碑。

约束：任务状态由 `TaskService` 聚合分配和更新事件后计算，适配器不得自行设置。

## 2. 库存域

- `Item`：物料主档；
- `Lot`：批次和有效期；
- `InventoryTransaction`：不可变库存流水；
- `InventoryBalance`：由流水派生的余额；
- `RestockRequest`：补货建议和采购跟踪。

约束：所有数量输入为正数，库存流水类型决定余额方向。余额不能成为唯一事实来源。

## 3. 决策和审批域

- `AgentProposal`：Agent 的独立建议；
- `ApprovalRequest`：高风险动作的审批快照；
- `AuditEvent`：所有写动作和拒绝动作的审计事件。

## 4. 同步域

- `SyncMapping`：本地 ID 与飞书记录 ID 映射；
- `SyncEvent`：一次同步尝试；
- `SyncConflict`：需要人工裁决的双边修改。

实现模块必须遵守这些领域边界，但具体平台、部署和适配器映射仅在 private 内部映射仓库维护。
