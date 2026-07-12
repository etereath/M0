# Contributing

所有公共契约变更必须先通过 Issue 说明动机、影响模块、兼容性和迁移方案，再通过 Pull Request 提交。

请勿在业务仓库复制或私自修改枚举、状态机、字段含义或错误码。新增字段应优先可选；新增枚举必须说明旧客户端的默认处理方式。提交前运行 `make validate` 和 `make test`。

生成代码仅是参考产物，不能反向成为 Schema、OpenAPI 或文档的来源。详情见 [docs/governance.md](docs/governance.md)。
