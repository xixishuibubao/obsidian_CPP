# Git 工作流规范

## 同步方式

主要使用 [obsidian-git](https://github.com/Vinzent03/obsidian-git) 插件在 Obsidian 内部提交和推送。插件的 `Custom Git binary path` 设置必须指向 `git.exe`（不是 `git-bash.exe`）。

## 提交信息格式

必须遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <description>
```

> **description 默认使用简体中文**，`type(scope):` 头部保持英文。中文项目优先中文 log。
> **description 必须简述具体改动内容**（如"修复 ConfigLoader 空指针崩溃"），不得用"修复若干问题""优化多处"等无信息量的概括。变更涉及多个文件时，在 body 中逐项列出各文件的具体变更原因。

### 常用类型

| 类型 | 用途 |
|------|------|
| `feat` | 新增内容/功能 |
| `fix` | 修复错误 |
| `docs` | 文档类变更 |
| `style` | 格式、空格、命名规范 |
| `refactor` | 结构调整，无功能变化 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 工具配置、依赖 |
| `ci` | CI 配置 |
| `build` | 构建系统 |

### scope（可选）

使用目录名或主题名，例如 `docs(03.Linux环境与工具)`、`docs(go)`、`fix(git)`。

## 本地提交流程

根据阶段选择不同的详细程度：

### A. 工作中间态提交（频繁，扼要）

AI 逐次改动或日常小修时，每次改动后立即提交，message 用精炼的一句话概括核心改动即可，**不要求逐文件列举**：

```bash
git commit -m "fix(E-AI): 修正索引中的计数错误"
git commit -m "docs(linux): 补充 tmux 常用快捷键表格"
```

- 目的：快速存档，记录进度
- 扼要不等于模糊 —— 需体现具体改了**什么**，只是不必展开**每个文件**各改了啥

### B. Squash 终态提交（推远端前，详细）

Squash 合并后、或直接使用 `/quick-commit` 时，必须展开为逐文件的详细 log：

```bash
docs(E-AI): 新增 Skill 总览笔记，同步更新仓库结构索引与笔记计数

- .claude/instructions/01-repo-structure.md：E-AI 模块笔记计数 4→5，目录描述追加 Skill 总览条目
- 03.工具与配置/5. Claude Code Skill 能力总览与推荐清单.md：新建笔记，梳理 6 类 Skill 能力
- 03.工具与配置/1. 工具与配置索引.md：追加 Skill 总览笔记链接
```

| 手段 | 详细程度 | 适用场景 |
|------|----------|----------|
| 逐次 `git commit` | 扼要 1 行 | AI 每步改动后/日常小修 |
| `/quick-commit` | 逐文件详细 | 准备结束一段工作时 |
| Squash 后重写 | 逐文件详细 | 推远端前整理历史 |

## 推远端前整理

在 push 到远端之前，必须将多次本地 commit 合并为干净的提交历史：

### 方法 A：git reset --soft（推荐，简单场景）

```bash
# 假设有 3 个本地提交：
#   commit A: 第一步修改
#   commit B: 第二步修改
#   commit C: 修复 typo

# 合为一个：
git reset --soft HEAD~3
git commit -m "feat(scope): 完整的功能描述"
```

### 方法 B：git rebase -i（复杂场景，保留多个有意义提交）

```bash
git rebase -i origin/main
# 将 fixup/squash 标记应用到需要合并的提交
```

### 处理 obsidian-git 自动备份提交

Obsidian 插件可能产生无意义的自动备份提交。使用以下命令将其合并到前一个有意义的提交：

```bash
git rebase -i HEAD~N
# 将备份提交标记为 fixup
```

## .gitignore 策略

```
.obsidian/*                        # 忽略所有 Obsidian 配置
!.obsidian/community-plugins.json  # 但保留插件列表
!.obsidian/core-plugins.json       # 和核心插件配置
!.obsidian/plugins/obsidian-git/*  # 和 Git 插件配置
!.obsidian/themes/**/*             # 和主题配置
```

忽略大文件（`.mp4`, `.pdf`, `.zip` 等）和编辑器临时文件。

## 空目录追踪

通过 `.gitkeep` 文件追踪空目录：
- 空目录自动生成 `.gitkeep`
- 目录有内容后删除冗余 `.gitkeep`
- 参见 `README.md` 中的 pre-commit hook 脚本
