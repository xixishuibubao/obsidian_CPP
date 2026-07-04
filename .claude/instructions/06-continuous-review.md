# 知识库持续审查

## 总则

在全库一次性审查完成后，通过轻量持续机制防止知识库退化。核心原则：**左移审查** — 在问题进入仓库前拦截，而非堆积后一次性清理。

---

## 1. Pre-commit 自检（Agent 自觉执行）

每次 `git commit` 前，依序执行以下步骤：

**Step 0 — 换行符统一**（避免仅换行符改动的提交）：
```bash
git add --renormalize .
```

**Step 1 — 完整性检查**：
```bash
# 1) 标题格式 — 应全部为 # N. 格式
echo "=== 标题格式 ==="
grep -rnP '^# \d' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'README' | grep -v '99\.'

# 2) YAML frontmatter — 不应存在
echo "=== YAML frontmatter ==="
grep -rlnP '^---$' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/' | grep -v 'CLAUDE.md'

# 3) 代码块语言标注 — 不应有无标注的 fenced block
echo "=== 无标注代码块 ==="
grep -rnP '^\x60\x60\x60\s*$' --include='*.md' . | grep -v '\.git/' | grep -v '\.claude/'
```

> **原则**：发现异常先修复再提交。以上检查项随时间积累可增补。

---

## 2. 增量审查流程（核心）

每次创建或修改笔记后、commit 前，由当前 Agent 自动执行。

### 触发时机
- 用户要求新建笔记时
- 用户要求修改现有笔记后
- 批量编辑后、commit 前

### 执行步骤

1. **定位变更**：运行 `git diff --cached --name-only` 或 `git diff --name-only` 获取变更的 `.md` 文件列表
2. **逐文件审查**：对每个变更文件执行以下 7 项检查

### 7 项审查清单

| # | 检查项 | 规范要求 | 修复方式 |
|---|--------|----------|----------|
| 1 | **标题格式** | `# 1.` 开头，`## 1.N` 二级编号，`###` 三级可选编号 | 直接修改标题行 |
| 2 | **YAML / #tag** | 无 `---` frontmatter，无 `#tag` | 删除违规行 |
| 3 | **代码块标注** | fenced block 首行 ``` 后紧跟语言名（c/cpp/bash/python 等） | 补全语言标注 |
| 4 | **wikilink 断裂** | 目标文件存在；跨模块用全路径 `[[目录/子目录/文件名\|显示]]` | 修正路径或补全文件 |
| 4b | **表格内 wikilink 别名** | 表格行内不得出现 `[[路径\|显示]]`；单元格用纯文本或 `[[路径]]` | 见 [02-note-conventions.md](02-note-conventions.md)「Markdown 表格中的 wikilink」 |
| 5 | **双语写作** | 技术术语用英文，解释说明用中文 | 调整语序/用词 |
| 6 | **交叉引用** | 链接到同模块或跨模块相关笔记 | 追加 `[[wikilink]]` |
| 7 | **薄厚格式** | 新笔记应有 `【核心精简提纲】` + `【完整拓展详情】` 双分区 | 补充缺失分区 |

### 扩展 4 项（全库审计，见 [08-vault-audit.md](08-vault-audit.md)）

| # | 检查项 | 规范要求 | 修复方式 |
|---|--------|----------|----------|
| 8 | **索引同步** | 改目录笔记数时更新 `01-repo-structure.md` + README | 重算 `find … -name '*.md'` |
| 9 | **删除/移动** | 删/移笔记后跑 M1 断链扫描 | `bash .claude/skills/vault-audit/scripts/vault-audit.sh quick` |
| 10 | **陈旧词表** | 正文不含已删专题名（1126/DriverSO 等） | 改通用示例或删引用 |
| 11 | **语义一致** | 大改技术段落后核对相邻笔记无矛盾 | module 模式语义审查 |

### 修复原则
- 发现即修复，直接编辑文件
- 格式/链接/代码块等机械问题 **必须修复** 后方可提交
- 内容类问题（准确性、交叉引用）评估修复成本，小改直接修、大改记入待办

---

## 3. 与相关工作流的关系

- **全库审计** → `.claude/plan/YYYY-MM-DD-vault-audit-report.md`（由 `/vault-audit` 生成，细则见 [08-vault-audit.md](08-vault-audit.md)）
- **增量审查** → 本文档，每次修改后执行
- **笔记创建** → 按 [02-note-conventions.md](02-note-conventions.md) 格式新建，之后执行增量审查
- **Git 工作流** → 按 [03-git-workflow.md](03-git-workflow.md) 提交

---

## 4. 本文件维护

- 审查项随知识库规范演进而调整
- 发现新的常见问题类型可增补到 7+4 项清单中
- 保持简洁，检查命令优先用 bash one-liner
