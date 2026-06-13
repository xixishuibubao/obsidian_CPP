# 计划：F-杂项 拆分重构（修订版）

## 背景

原 `F-杂项/` 有 4 个子目录共 14 篇笔记。用户决定：
- **删除** `01.开发工具/`（4 篇：MobaXterm、CLion、VS2022、Qt）及 `03.数据库/`（空占位）
- **保留** `02.版本管理/`（4 篇）和 `04.语言与标记/`（6 篇）
- 将保留下来的内容提升为独立顶层模块，消除 F-杂项

## 新结构

```
G-版本管理/             ← F-杂项/02.版本管理/ 提升
├── 1. git.md
├── 2. log规范.md
├── 3. git bisect.md
└── 4. 分支策略.md

H-语言与标记/           ← F-杂项/04.语言与标记/ 提升
├── 1. Markdown.md
├── 2. CSS.md
├── 3. XML.md
├── 4. PlantUML学习资料.md
├── 5. UML语法.md
└── 6. 常用英语.md
```

`F-杂项/` 整目录删除（内容全部迁出后为空）。

## 安全分析

### Wiki 链接
所有跨目录引用使用 `[[filename]]` 短格式，移动后 Obsidian 按文件名自动解析。

**唯一需注意**：`C-Linux生态/01.Linux环境/2. 动态库与静态库.md` 第 3 行引用了 `[[3. VS2022|VS2022 动态库与静态库]]`，VS2022 笔记将被删除 → 需移除该引用行。

其余外部引用（E-AI 中的 `[[1. git]]`、`[[5. UML语法]]`、`[[6. 常用英语]]`）自动解析无误。

### 图片路径
`H-语言与标记/1. Markdown.md` 中 2 处 `../../picture/cpplogo.png` 需改为 `../picture/cpplogo.png`。
开发工具目录删除，其图片引用不再需要处理。

## 执行步骤

### Step 1: 创建新目录
```bash
mkdir G-版本管理 H-语言与标记
```

### Step 2: 移动文件（git mv）
```bash
git mv "F-杂项/02.版本管理/"*.md G-版本管理/
git mv "F-杂项/04.语言与标记/"*.md H-语言与标记/
```

### Step 3: 删除不要的目录（git rm -rf）
```bash
git rm -rf "F-杂项/01.开发工具/"
git rm -rf "F-杂项/03.数据库/"
```

### Step 4: 删除空 F-杂项 目录
```bash
rmdir "F-杂项/"
```
（若 `F-杂项/` 无任何残留文件）

### Step 5: 修复引用和图片路径
- **Edit** `C-Linux生态/01.Linux环境/2. 动态库与静态库.md`：
  删除或注释第 3 行的 `> Windows 下 DLL 与静态库的使用参见：[[3. VS2022|VS2022 动态库与静态库]]`
- **Edit** `H-语言与标记/1. Markdown.md`：
  2 处 `../../picture/` → `../picture/`

### Step 6: 更新索引文件
1. **CLAUDE.md**（第 115 行附近）：
   - 将 `F-杂项/             ← 开发工具 · Git · 语言/标记 · （数据库 🚧 占位）` 
   - 替换为 G-版本管理 和 H-语言与标记 两行
2. **`.claude/instructions/01-repo-structure.md`**：
   - 删除 F-杂项 整节，新增 G-版本管理 和 H-语言与标记 章节
   - 更新总笔记数（删除 4 篇后从 ~80 → ~76）
3. **README.md**（第 73-78 行）：替换 F-杂项 目录树为 G+H
4. **readme/README_EN.md**（第 72-77 行）：同上英文版

### Step 7: .gitkeep 维护
```powershell
powershell -File .git\hooks\auto-gitkeep.ps1
```

### Step 8: 本地提交
```bash
git add -A
git commit -m "refactor(结构): F-杂项 拆分重构，删除开发工具与数据库

变更：
- 删除 F-杂项/01.开发工具/（MobaXterm, CLion, VS2022, Qt 共 4 篇）
- 删除 F-杂项/03.数据库/（空占位）
- G-版本管理: 从 F-杂项/02.版本管理 提升（4 篇）
- H-语言与标记: 从 F-杂项/04.语言与标记 提升（6 篇）
- F-杂项 整体移除
- 修复 Markdown.md 图片路径 (../../picture/ → ../picture/)
- 移除 VS2022 断裂 wikilink 引用"
```

## 验证清单

- [ ] `G-版本管理/` 包含 4 个 .md 文件
- [ ] `H-语言与标记/` 包含 6 个 .md 文件
- [ ] `F-杂项/` 目录已不复存在
- [ ] `F-杂项/01.开发工具/` 已删除
- [ ] `F-杂项/03.数据库/` 已删除
- [ ] Markdown.md 中图片路径已改为 `../picture/`
- [ ] `C-Linux生态/01.Linux环境/2. 动态库与静态库.md` 中 VS2022 引用已移除
- [ ] CLAUDE.md 的 Directory Overview 已更新
- [ ] 01-repo-structure.md 已更新
- [ ] README.md / README_EN.md 目录树已更新
- [ ] `.gitkeep` 已全部补齐
- [ ] `grep -r "F-杂项" --include="*.md" . | grep -v ".git/"` 只保留 git log 历史
