# 统一错误码

| 错误码 | HTTP | 可重试 | 含义 |
|---|---:|---:|---|
| `AUTH_UNAUTHENTICATED` | 401 | 否 | 缺少或无效认证 |
| `IDENTITY_UNMAPPED` | 403 | 否 | 聊天身份未映射到员工 |
| `AUTHZ_FORBIDDEN` | 403 | 否 | 操作者无权执行动作 |
| `VALIDATION_FAILED` | 400 | 否 | 请求不符合 JSON Schema 或业务字段约束 |
| `ENTITY_NOT_FOUND` | 404 | 否 | 目标实体不存在 |
| `TASK_REFERENCE_AMBIGUOUS` | 409 | 否 | 员工回复可能对应多个任务，需要追问 |
| `IDEMPOTENCY_KEY_REUSED` | 409 | 否 | 同一幂等键用于不同请求 |
| `CONFLICT_VERSION_MISMATCH` | 409 | 是 | 乐观锁版本不匹配 |
| `STATE_TRANSITION_INVALID` | 409 | 否 | 非法状态迁移 |
| `APPROVAL_REQUIRED` | 409 | 否 | 缺少有效审批 |
| `APPROVAL_PAYLOAD_CHANGED` | 409 | 否 | 审批哈希与当前载荷不一致 |
| `SYNC_CONFLICT` | 409 | 否 | 云端与本地同时修改，需人工解决 |
| `EXTERNAL_PLATFORM_RATE_LIMITED` | 429 | 是 | 外部平台限流 |
| `EXTERNAL_PLATFORM_UNAVAILABLE` | 503 | 是 | 外部平台暂不可用 |
| `STORAGE_TEMPORARILY_UNAVAILABLE` | 503 | 是 | 本地存储暂不可用 |
| `APPROVED_EXECUTION_REJECTED` | 409 | 否 | 已批准执行申请被拒绝 |
| `CONTRACT_HEADER_BODY_MISMATCH` | 422 | 否 | HTTP Header 与命令 body envelope 不一致 |
| `INTERNAL_ERROR` | 500 | 视情况 | 未分类内部错误 |

错误响应必须符合 `schemas/error_response.schema.json`，不得把密钥、密码、Token 或完整堆栈返回给普通调用方。
