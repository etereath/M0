# M1–M5 依赖策略

M0 `v0.1.0` 是当前冻结的公共契约基线。M1、M2、M3、M4 和 M5 必须固定依赖该 Release、Tag 或 commit SHA。

允许：

- 下载 `https://github.com/etereath/M0/releases/tag/v0.1.0`；
- 使用 `v0.1.0` 作为包、子模块或 vendored artifact 的固定版本；
- 在构建清单中记录固定 commit SHA，并通过升级 PR 变更。

禁止：

- 直接依赖 `main` 或其他浮动分支；
- 将 Schema、枚举、状态机或错误码复制后在业务仓库中修改；
- 通过本地补丁绕过公共契约校验。

若业务模块发现契约缺口，应在 M0 创建 Issue，说明影响模块、兼容性和迁移方案；只有通过 PR 并发布新版本后，业务模块才可提交依赖升级。
