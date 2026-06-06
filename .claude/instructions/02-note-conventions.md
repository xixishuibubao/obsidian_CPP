# 笔记内容规范

## 标题编号体系

所有笔记使用一致的数字编号体系：

```markdown
# 1. 主标题
## 1.1 二级标题
### 1.1.1 三级标题
#### 1.1.1.1 四级标题
```

- 不以 `#` 开头的文件需要补全
- 标题内不混用 `**` 加粗标记
- 不使用自动编号或手动中文编号（一、二、三）

## 跨笔记引用

使用 Obsidian wikilink 语法：

```markdown
[[文件名]]                          → 显示为文件名
[[文件名|自定义显示文字]]             → 显示为自定义文字
[[9. ssh免密登录|SSH 免密登录]]       → 显示为 "SSH 免密登录"
```

- `文件名` 不含 `.md` 扩展名
- 使用 `|` 分隔显示文字
- 文章内的其他完整路径引用（如 `03.Linux环境与工具/8. 常用指令.md`）为纯文本引用，非可点击链接

## 代码块

使用 fenced code blocks 并标注语言：

- `c` — C 语言代码
- `C++` — C++ 代码
- `bash` — Shell 命令
- `powershell` — PowerShell 命令
- `makefile` — Makefile
- `go` — Go 代码
- `lua` — Lua 代码
- `python` — Python 代码
- `java` — Java 代码
- `sql` — SQL 语句
- `plain` / `Plain` — 纯文本（不要使用无标注的缩进代码块）

## 图片

```markdown
![描述文字](picture/文件名.png)
```

- 统一使用小写 `.png` 引用，即使磁盘上是 `.PNG`
- 图片放在根目录 `/picture/` 下

## 其他约定

- **无 YAML frontmatter**：笔记不使用 `---` 分隔的元数据块、tags 或 aliases
- **无 Obsidian `#tag`**：不使用标签语法
- **无 Obsidian `%%` 注释**：不包含隐藏注释块
- **双语写作**：技术术语用英文，解释说明用中文
- **跨平台发布**：如需发布到飞书/公众号，使用 [markdown.lovejade.cn](https://markdown.lovejade.cn/) 转换（选择"公众号"模式）

## 文件命名

```
数字. 空格 + 名称.md
```

示例：`1. C++基础.md`、`2. 代码规范.md`、`8. 常用指令.md`

目录和文件均遵循此规范。
