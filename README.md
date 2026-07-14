# Automation Platform Contracts

当前正式版本：`v0.2.0`（`v0.2.1` 为仅文档修正的补丁发布）；历史冻结基线：`v0.1.0`。

本仓库是自动化平台公共契约的唯一权威来源。它维护领域对象、JSON Schema、OpenAPI、公共枚举、状态机、权限矩阵、ID/时间/版本规范、错误码、幂等与审计规则、fixtures，以及 Python 和 TypeScript 参考类型。

M0 的 `v0.1.0` 业务语义已冻结，当前正式契约版本为 `v0.2.0`；`v0.2.1` 只修正文档，不改变契约语义。新启动的 M1–M5 等并行业务项目推荐固定依赖 `v0.2.0` Release、Tag 或 commit；已经基于 `v0.1.0` 开发的模块不必立即升级，可以继续固定依赖 `v0.1.0`。所有项目都不得依赖 `main`，也不得复制后在本地修改契约。所有后续变更必须先通过 Issue，再通过 Pull Request。

> 其他项目可以提出契约修改，但不能在本地私自改变公共枚举、状态机、字段含义或错误码。只有本仓库发布的正式版本才是有效契约。

## 使用

固定使用 Release 或 Tag，例如：

```text
https://github.com/etereath/M0/releases/tag/v0.2.0
```

不要让业务项目无条件追踪 `main`。需要新增字段、状态或枚举时，请先提交契约变更 Issue，说明使用场景、影响模块、默认处理方式与兼容性；获准后通过 Pull Request 修改此仓库。

## 从 v0.1.0 升级到 v0.2.0

升级前请确认：

- `POST /v1/projects` 使用 `schemas/projects/project_create.schema.json`；`project_id`、`version`、`status`、`created_at` 和 `updated_at` 等服务端生成字段不应由客户端提交；
- 任务命令以请求体中的 `idempotency_key` 和 `actor` 作为跨通道权威字段；HTTP 的 `Idempotency-Key` 和 `X-Actor-Id` 只是传输层副本，分别必须与 `body.idempotency_key` 和 `body.actor.actor_id` 一致；
- Header 与 body 不一致时，服务端应返回 HTTP 422 和 `CONTRACT_HEADER_BODY_MISMATCH`。

## 校验与打包

需要 Python 3.11 及以上版本。安装固定依赖后运行：

```bash
python -m pip install .
make validate
make test
make package
```

`make package` 会重新执行完整校验，并生成与当前版本匹配的 `dist/automation-platform-contracts-v0.2.1.zip`。校验失败时不会生成 Release 包。

## 兼容性与版本

本仓库遵循语义化版本：

- PATCH：文档、样例或不改变含义的修正；
- MINOR：新增兼容字段、Schema 或接口；
- MAJOR：删除字段、改变字段或枚举含义、改变状态机，或其他破坏性变更。

新增字段应优先为可选字段。当前仍处于 1.0 之前，契约可能演进，但每项变化仍必须记录在 [CHANGELOG.md](CHANGELOG.md) 中。完整规则见 [docs/versioning.md](docs/versioning.md) 与 [docs/governance.md](docs/governance.md)。

## 目录

- `openapi/`：OpenAPI 3.1 契约；
- `schemas/`：JSON Schema Draft 2020-12 的唯一权威文件；
- `docs/`：领域模型、枚举、状态机、权限、规范和治理文档；
- `fixtures/`：必须接受和必须拒绝的示例；
- `generated/`：从契约派生的参考类型，不是契约来源；
- `scripts/`：可重复校验、引用检查、校验和与发布打包脚本。
