# 状态机规范

## 1. 任务状态机

### 1.1 核心路径

```text
SIMPLE:     DRAFT → READY → ASSIGNED → ACCEPTED → IN_PROGRESS → SUBMITTED → COMPLETED
CONTROLLED: DRAFT → PENDING_APPROVAL → READY → ASSIGNED → ACCEPTED → IN_PROGRESS → SUBMITTED → NEEDS_REVIEW → COMPLETED
```

附加路径：

- `ASSIGNED → READY`：全部分配被拒绝或取消；
- `IN_PROGRESS → BLOCKED → IN_PROGRESS`：阻塞与恢复；
- `SUBMITTED → NEEDS_REVIEW`：需要证据或负责人验收；
- `NEEDS_REVIEW → IN_PROGRESS`：验收不通过，退回返工；
- 任意非终态可由授权人员转为 `CANCELLED`；
- `COMPLETED` 和 `CANCELLED` 为终态。

### 1.2 聚合规则

- `ASSIGNED`：至少有一条有效分配；
- `ACCEPTED`：已接受分配数达到 `minimum_accept_count`；
- `IN_PROGRESS`：至少一位已接受人员开始执行；
- `SUBMITTED`：执行者提交完成；
- `COMPLETED`：满足自动验收规则，或授权人员验收通过；
- `is_overdue`：`due_at < now` 且任务不在终态，是派生字段，不写入 `status`。

### 1.3 Agent 限制

- 外部会话代理可在有效身份和权限上下文中提交命令，但状态迁移由任务服务执行；
- 外部会话代理不得自行修改截止时间；
- 外部会话代理不得批准 `CONTROLLED` 任务；
- 复杂任务的关键状态变化需要 OWNER/MANAGER 确认。

## 2. 项目状态机

```text
PROPOSED → PLANNING → ACTIVE ↔ PAUSED → COMPLETED
                         └────────────→ CANCELLED
```

- `COMPLETED`、`CANCELLED` 只能由 OWNER/MANAGER 执行；
- Agent 只能新增 `STATUS_SUGGESTION`，不能直接改变项目状态；
- 项目进度保留 `progress_percent_confirmed` 和 `progress_percent_suggested` 两个字段，后者不能覆盖前者。

## 3. 里程碑状态机

```text
PLANNED → ACTIVE ↔ BLOCKED → COMPLETED
      └────────────────────→ CANCELLED
```

## 4. 审批状态机

```text
PENDING → APPROVED
        → REJECTED
        → CANCELLED
        → EXPIRED
```

审批解析必须校验 `payload_hash` 与待执行载荷一致；载荷改变后原审批失效，必须新建审批。
