# 契约治理

1. M0 `v0.1.0` 的业务语义（字段含义、枚举、状态机、权限、错误码和 API 行为）保持冻结。任何后续变化必须先有 Issue，再通过 Pull Request；不得直接提交到 `main`。
2. 所有契约变化的 PR 必须说明影响的模块、兼容性、fixtures 和迁移安排。
3. 新增枚举必须说明旧版本消费者的默认处理方式；新增 Schema 字段应优先设为可选。
4. 删除或改名字段属于破坏性变更，必须按版本规范处理。
5. 状态机和权限变化必须获得架构负责人批准。
6. 不允许借由 fixtures 暗中改变正式契约；fixtures 只能证明已定义的契约行为。
7. 生成代码不能反向成为契约来源。JSON Schema、OpenAPI 和正式文档才是权威输入。
8. OpenAPI 与 JSON Schema 出现冲突时必须阻止合并，先修复冲突并补充对应 fixtures。
9. M1–M5 只能依赖 `v0.1.0` Release、Tag 或固定 commit，不能无条件追踪 `main`。
10. 所有变更必须更新 `CHANGELOG.md`，并在需要时提升 `VERSION` 和创建 Release。
