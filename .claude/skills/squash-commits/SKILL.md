---
name: squash-commits
description: Squashes local unpushed commits before push, auto-detecting obsidian-git backup commits. Use when cleaning history before push or the user invokes /squash-commits.
disable-model-invocation: true
---

# /squash-commits — 整理提交历史

在推送前将零散本地 commits 合并为干净历史。

---

## 执行流程

### 1. 预检：工作区是否干净

```bash
git status --porcelain
```

- 如果有未提交的改动，提示用户：**"工作区有未提交的改动，squash 前请先 commit 或 stash。"**
- 提供选项：`[s] stash 后继续 / [c] 取消`（stash 用 `git stash push -u -m "pre-squash"`，完成后提示 `git stash pop`）
- 工作区干净则继续
- 预检 merge/rebase：`test -d .git/rebase-merge -o -d .git/rebase-apply -o -f .git/MERGE_HEAD` → 拒绝 squash

### 2. 获取提交信息

```bash
git fetch origin --quiet 2>/dev/null || true
upstream=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "origin/main")
git log --oneline "${upstream}..HEAD"    # 本地未推送 commits
# 若 upstream 不存在，则 git log --oneline -10
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
| obsidian-git | `^vault backup:\s\d{4}-\d{2}-\d{2}(\s\d{2}:\d{2}:\d{2})?` |
| 通用自动备份 | `^(wip|checkpoint|auto commit|automatic backup)\b`（不区分大小写） |
| IDE 自动保存 | `^(temp|save work|snapshot)\b` — **仅提示，默认不自动 fixup** |

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
   [✓] 方法 A: git reset --soft HEAD~N
   [ ] 方法 B: GIT_SEQUENCE_EDITOR 自动化 rebase
```

方法 A/B 细节、§B message 格式、Windows 注意见 [03-git-workflow.md](../../instructions/03-git-workflow.md) §B 与 Squash 章节。

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

执行前：

```bash
git reset --soft HEAD~N
git diff --cached --name-only | xargs -r git add --renormalize
```

```bash
# 方法 A
git commit -m "type(scope): header" -m "- 文件1：改动" -m "- 文件2：改动"

# 或方法 B（Git Bash）
GIT_SEQUENCE_EDITOR="..." git rebase -i "${upstream:-HEAD~N}"
# upstream 不存在时：git rebase -i HEAD~N
```

### 7. 执行后验证

```bash
git log --oneline -3                  # 查看 squash 后的提交
git diff --stat 'HEAD@{1}' HEAD       # PowerShell 须单引号；或优先 Git Bash
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
- squash 后不自动推送；push 前建议 `/vault-audit quick`
- hook / renormalize：见 [06-continuous-review.md](../../instructions/06-continuous-review.md)

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)。方法 B 须在 Git Bash 执行。

## 工作流衔接

| 方向 | Skill |
|------|-------|
| 上游 | [/quick-commit](../quick-commit/SKILL.md) 或多次 `git commit` |
| 下游 | 用户自行 `git push`（本 Skill 不自动推送） |

## 相关文件

- [03-git-workflow.md](../../instructions/03-git-workflow.md)
- [CLAUDE.md](../../CLAUDE.md)
- [../quick-commit/SKILL.md](../quick-commit/SKILL.md)
- [../ingest-note/SKILL.md](../ingest-note/SKILL.md)
