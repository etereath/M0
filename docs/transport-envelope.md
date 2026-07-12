# 命令 envelope 与传输映射

`task_command.schema.json` 的完整 body envelope 是跨通道权威契约。文件队列、内部调用和非 HTTP 通道直接传递完整 envelope，不要求或模拟 HTTP Header。

HTTP 网关可以接收 `Idempotency-Key` 和 `X-Actor-Id` 作为传输字段，但它们只是 body 字段的传输副本：

- `Idempotency-Key` 必须等于 `body.idempotency_key`；
- `X-Actor-Id` 必须等于 `body.actor.effective_employee_id`；
- 两边同时存在且不一致时，网关必须拒绝请求并返回 `CONTRACT_HEADER_BODY_MISMATCH`（HTTP 422）；
- 网关不得用 Header 覆盖 body，也不得把 Header 作为非 HTTP 通道的替代字段。

因此 M3、M4 和 M7 可以共享同一份命令 envelope，同时保留 HTTP 的幂等和身份传输约束。
