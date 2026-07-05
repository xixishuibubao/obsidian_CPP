# 工具链配置（Tier 1 运行时）

Agent 执行 Python / Node / Perl 等脚本前，须读取 `.claude/toolchain.json`；缺失或 `generated_at` 超过 7 天则运行 `/probe-toolchain`。

Shell 终端策略见 [04-shell-config.md](04-shell-config.md)（bash vs PowerShell）；本文件管 **工具二进制路径**（python/node/perl 等）。

## Tier 1 工具（影响 exit code）

| 工具 | 用途 | 阻塞级别 |
|------|------|----------|
| python | 复杂脚本、JSON 处理 | 任务需要时 |
| node | JS 工具链 | 任务需要时 |
| perl | 构建脚本、Strawberry 模块环境 | 任务需要 `.pl` 时 |
| git / bash | vault 脚本、grep 审计 | 推荐 |

## 可选工具（写入 manifest，不影响 exit code）

| 工具 | 用途 | 说明 |
|------|------|------|
| jq | Shell 管道 JSON 查询 | 本 vault 主脚本用 Python `json`；缺失可忽略 |

manifest 中 optional 工具有 `"tier": "optional"` 字段。

## Pin 优先级

1. 项目 `.claude/toolchain.local.json`（gitignore）
2. 全局 `~/.claude/toolchain.local.json`
3. 项目约束：`.python-version`、`package.json` → `engines.node`
4. 自动探测（Perl：**Strawberry 优先于 Git 内置**）

pin 格式见 [.claude/toolchain.example.json](../toolchain.example.json)。

## 探测与刷新

脚本优先级：**Python > Bash > PowerShell**

```bash
python .claude/skills/probe-toolchain/scripts/probe-toolchain.py
bash .claude/skills/probe-toolchain/scripts/probe-toolchain.sh    # 包装
```

产出：`.claude/toolchain.json`（gitignore，机器快照）。

**exit code**（仅 Tier 1）：0=全部 ok；1=Tier 1 存在 missing；2=Tier 1 存在 ambiguous。optional 工具（如 `jq`）缺失不改变 exit code。

## Agent 执行范式

```powershell
# 读取 manifest 后使用绝对路径
& "C:\...\python.exe" script.py
```

```bash
# 读 toolchain.json 优先用 Python（本 vault 脚本优先级）
PYTHON="$(python -c "import json; print(json.load(open('.claude/toolchain.json'))['tools']['python']['selected']['path'])")"
"$PYTHON" script.py
```

禁止假设 `python`/`node`/`perl` 在 PATH 中可用。

## status 含义

| status | 行为 |
|--------|------|
| `ok` | 使用 `selected.path` |
| `not_in_path` | 仍用 `selected.path`；可向用户展示 `fix_hint` 加 PATH |
| `missing` | 展示 `fix_hint`，停止或换方案 |
| `ambiguous` | 展示 candidates，请用户写入 `toolchain.local.json` 后重跑 probe |

## Perl 特例

- `selected.flavor=strawberry`：完整 CPAN 环境，构建脚本首选
- `selected.flavor=git`：Git 内置 Perl，模块可能不全；`fix_hint` 建议安装 [Strawberry Perl](https://strawberryperl.com/) 并 pin
- 多 Strawberry 安装目录 → `ambiguous`，必须 pin

## 初始化链

```
init-win-env → probe-toolchain → init-git-convention → init-note-vault
```

Skill：[probe-toolchain/SKILL.md](../skills/probe-toolchain/SKILL.md)

## 相关文件

- [04-shell-config.md](04-shell-config.md)
- [05-agent-coordination.md](05-agent-coordination.md)
- [probe-toolchain/scripts/probe-toolchain.py](../skills/probe-toolchain/scripts/probe-toolchain.py)
