---
name: init-git-convention
description: Injects Conventional Commits workflow into a project — generates CLAUDE.md sections and git instruction files. Use when initializing a new repo or invoking /init-git-convention.
disable-model-invocation: true
---

# /init-git-convention — Git 工作流规范初始化

为任意项目注入 Conventional Commits + 整洁 Git 工作流。模板见 [reference.md](reference.md)。

---

## 执行流程

### 0. 预检

```bash
git --version
git rev-parse --git-dir 2>NUL
```

未安装 git 或不在仓库内 → 提示退出。

**上游**：若 `.claude/toolchain.json` 缺失，先运行 `/probe-toolchain`。

### 1. 询问偏好

- Commit 描述语言：中文 / English（默认中文）
- 项目类型：个人笔记 / 开源库 / 企业项目（影响 scope 示例）

### 2–5. 生成文件

| 输出 | 说明 |
|------|------|
| `CLAUDE.md` | Git Workflow + Self-Management 段落（模板见 reference.md） |
| `.claude/instructions/NN-git-workflow.md` | 扫描取下一编号；Squash 细则对齐本 vault [03-git-workflow.md](../../instructions/03-git-workflow.md) |
| `.claude/settings.json` | 合并 git 相关权限（reference.md §settings.json） |

已有 Git 段落时询问追加/覆盖/跳过。

### 6. 验证与 handoff

展示生成文件列表；建议 commit：`chore(claude): 初始化 Git 工作流规范`

> Git 规范已注入。建议下一步：`/init-note-vault`

## Bootstrap

`init-win-env` → `probe-toolchain` → **init-git-convention** → `init-note-vault`

## 注意事项

- instructions 编号动态扫描，勿硬编码 `01-`
- settings.json 合并保留用户已有配置
- 本 vault 已有权威 [03-git-workflow.md](../../instructions/03-git-workflow.md)，补跑时以合并为主

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)

## 相关文件

- [reference.md](reference.md)
- [03-git-workflow.md](../../instructions/03-git-workflow.md)
- [../probe-toolchain/SKILL.md](../probe-toolchain/SKILL.md)
- [../init-note-vault/SKILL.md](../init-note-vault/SKILL.md)
- [../quick-commit/SKILL.md](../quick-commit/SKILL.md)
