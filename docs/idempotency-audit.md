# 幂等、并发和审计规范

## 1. 写接口幂等

所有写接口必须接受 `Idempotency-Key`：

- 聊天消息：`chatmsg:<platform>:<message_id>`；
- 外部平台事件：`external:<event_id>`；
- 定时任务：`schedule:<job_name>:<logical_date>:<scope>`；
- 手工调用：由客户端生成 ULID 或 UUID。

服务端保存：键、请求规范化哈希、响应状态、响应摘要、首次处理时间。

- 相同键 + 相同请求哈希：返回首次结果，标记 `idempotent_replay=true`；
- 相同键 + 不同请求哈希：返回 `IDEMPOTENCY_KEY_REUSED`；
- 失败是否可重试由错误码决定。

## 2. 乐观并发

更新可修改主档时携带 `expected_version` 或 `If-Match`：

- 匹配：更新并令 `version + 1`；
- 不匹配：返回 HTTP 409 与 `CONFLICT_VERSION_MISMATCH`；
- 追加事件不需要更新主档版本，但事件 ID 必须唯一。

## 3. 规范化哈希

- JSON 键按字典序；
- UTF-8；
- 无无意义空格；
- 数值按 JSON 标准序列化；
- 敏感字段在审计哈希前保留，但不得输出到日志正文。

## 4. 审计最低字段

每次写动作记录：动作、操作者、有效员工、来源消息、目标实体、结果、前后哈希、时间和关联 ID。
权限拒绝和非法状态迁移也必须写审计事件。
