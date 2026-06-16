---
name: squash-commits
description: 推送前整理本地 commits — 展示提交列表，自动检测备份提交，选择策略后执行 squash
---

# /squash-commits — 整理提交历史

在推送前将零散本地 commits 合并为干净历史。

---

## 执行流程

### 1. 预检：工作区是否干净

```bash
git status --porcelain
```

- 如果有未提交的改动，提示用户：**"工作区有未提交的改动，squash 可能导致变更丢失。请先 commit 或 stash。"**
- 提供选项：`[s] stash 后继续 / [c] 取消`
- 工作区干净则继续

### 2. 获取提交信息

```bash
git log --oneline origin/main..HEAD    # 获取本地未推送 commits
# 如果 origin/main 不存在，则使用 git log --oneline -10
```

展示给用户：

```
未推送的本地提交 (共 3 个):
  a1b2c3d feat: 第一步改动
  e4f5g6h fix: 调整命名
  h7i8j9k docs: 修复 typo
```

### 3. 自动检测备份提交

扫描 commit message 中匹配以下模式的备份提交：

| 来源 | 匹配模式 |
|------|---------|
| obsidian-git | `vault backup: \d{4}-\d{2}-\d{2}` |
| 通用自动备份 | `auto commit`, `automatic backup`, `wip`, `checkpoint`（不区分大小写） |
| IDE 自动保存 | `temp`, `save work`, `snapshot`（不区分大小写） |

将检测结果用以下 Schema 结构化输出：

```
备份检测 Schema:
{
  total_commits: number,              // 本地未推送提交总数
  backup_commits: [{                  // 检测到的备份提交
    sha: string,
    message: string,
    source: "obsidian-git" | "auto" | "ide" | "unknown"
  }],
  meaningful_commits: number,         // 有意义的提交数
  recommendation: string              // 建议策略描述
}
```

标记检测结果：

```
检测到 [2] 个自动备份提交:
  x1y2z3a vault backup: 2026-06-06 14:00:00     ← obsidian-git
  b2c3d4e wip: 临时保存                          ← 通用备份

推荐策略: 将备份提交标记为 fixup，合并到最近的有意义提交
```

### 4. 询问策略

```
? 选择 squash 策略:
   ──
   [✓] 方法 A: git reset --soft HEAD~N（简单场景，合并为 1 个提交）
   [ ] 方法 B: GIT_SEQUENCE_EDITOR 自动化 rebase（复杂场景，保留多个有意义提交）
   ──
```

**方法 A** 适合：连续微提交 → 合并为 1 个。

```
  将合并 3 个提交为 1 个:
    feat: 完整功能描述

  输入新的 commit message (留空使用第一个提交的 message):
```

**方法 B** 适合：有意义的多个提交想保留、部分需要合并。

使用 `GIT_SEQUENCE_EDITOR` 环境变量实现非交互式 rebase：

```bash
# 原理：通过环境变量注入自动化编辑脚本，将指定提交标记为 fixup
GIT_SEQUENCE_EDITOR="sed -i 's/^pick \(x1y2z3a\|b2c3d4e\)/fixup \1/'" git rebase -i HEAD~N
```

```
  将打开自动化 rebase 编辑：
  pick a1b2c3d feat: 第一步改动       ← 保留
  fixup x1y2z3a vault backup: ...     ← 自动 fixup（备份提交）
  fixup e4f5g6h fix: 调整命名          ← 手动标记的 fixup
  fixup b2c3d4e wip: 临时保存          ← 自动 fixup（备份提交）
  fixup h7i8j9k docs: 修复 typo        ← 手动标记的 fixup
```

如果有检测到备份提交，自动标记为 `fixup` 并展示；有意义的提交交由用户选择如何标记。

### 5. 执行前确认

```
? 将执行以下操作:
  git reset --soft HEAD~3
  git commit -m "feat: 完整功能描述"

  [Y] 确认执行
  [e] 编辑 commit message
  [n] 取消
```

### 6. 执行

```bash
# 方法 A
git reset --soft HEAD~N
git commit -m "type(scope): description"

# 或方法 B
GIT_SEQUENCE_EDITOR="..." git rebase -i HEAD~N
```

### 7. 执行后验证

```bash
git log --oneline -3                  # 查看 squash 后的提交
git diff --stat HEAD@{1} HEAD          # 对比 squash 前后的 diff 是否一致
```

验证后展示：

```
✓ squash 成功:
  清理前: a1b2c3d, e4f5g6h, h7i8j9k (3 个提交)
  清理后: x9y8z7w (1 个提交)
  ──
  diff 一致性检查: ✓ 通过（变更内容与 squash 前一致）
```

如果 squash 后 diff 与 squash 前不一致（极少情况，可能是冲突解决导致），警告用户并展示差异。

## 使用时机

- 准备推送前
- 本地有多个零散提交想整理时
- obsidian-git 产生了多个备份提交需要清理时
- 工作区有 stash 或未提交变更时——先处理它们再 squash

## 注意事项

- **执行前必须要求用户确认** — squash 是破坏性操作
- **执行前必须检查工作区是否干净** — 脏工作区 + squash 可能导致变更丢失
- 备份提交检测使用正则匹配，支持 obsidian-git、通用备份、IDE 自动保存等模式
- 如果当前分支无远程跟踪分支（`origin/main` 不存在），使用 `git log --oneline -N` 展示最近 N 个
- squash 后不自动推送，留给用户最终决定
- 如果只有一个未推送提交，提示「只有一个提交，无需 squash」，询问是否仍要执行
- **不要跳过 pre-commit hooks 或使用 `--no-verify`** — 除非用户明确要求
- squash 后做 diff 一致性验证，确保没有意外引入或丢失变更
