# Automation Platform Contracts

当前版本：`v0.1.0`（M0 公共契约基线，业务语义已冻结）

本仓库是自动化平台公共契约的唯一权威来源。它维护领域对象、JSON Schema、OpenAPI、公共枚举、状态机、权限矩阵、ID/时间/版本规范、错误码、幂等与审计规则、fixtures，以及 Python 和 TypeScript 参考类型。

M0 的业务语义在 `v0.1.0` 冻结。M1–M5 等并行业务模块必须固定依赖 `v0.1.0` Release、Tag 或 commit，不得依赖 `main`，也不得复制后在本地修改契约。所有后续变更必须先通过 Issue，再通过 Pull Request。

> 其他项目可以提出契约修改，但不能在本地私自改变公共枚举、状态机、字段含义或错误码。只有本仓库发布的正式版本才是有效契约。

## 使用

固定使用 Release 或 Tag，例如：

```text
https://github.com/etereath/M0/releases/tag/v0.1.0
```

不要让业务项目无条件追踪 `main`。需要新增字段、状态或枚举时，请先提交契约变更 Issue，说明使用场景、影响模块、默认处理方式与兼容性；获准后通过 Pull Request 修改此仓库。

## 校验与打包

需要 Python 3.11 及以上版本。安装固定依赖后运行：

```bash
python -m pip install .
make validate
make test
make package
```

`make package` 会重新执行完整校验，并生成 `dist/automation-platform-contracts-v0.1.0.zip`。校验失败时不会生成 Release 包。

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
