---
name: probe-toolchain
description: Probes Tier 1 dev tools (Python, Node, Git, Bash, Strawberry Perl) and optional jq; writes toolchain.json. Use when setting up a machine, command not found, or invoking /probe-toolchain.
disable-model-invocation: true
---

# /probe-toolchain — 工具链依赖探测

写入 `.claude/toolchain.json`。Pin、Agent 范式、status 含义见 [09-toolchain-config.md](../../instructions/09-toolchain-config.md)。

## 脚本（Python 优先）

优先级：**Python > Bash > PowerShell**

```bash
python .claude/skills/probe-toolchain/scripts/probe-toolchain.py
bash .claude/skills/probe-toolchain/scripts/probe-toolchain.sh    # 包装
```

**exit code**（仅 Tier 1）：0=ok；1=Tier 1 missing；2=Tier 1 ambiguous。`jq` 等 optional 工具不影响 exit code。

## 执行流程

1. 在 vault 根运行上述命令 → 读终端摘要 + `.claude/toolchain.json`
2. `ambiguous` → 展示 candidates，写入 `.claude/toolchain.local.json` 后重跑（格式见 [.claude/toolchain.example.json](../../toolchain.example.json)）
3. `missing` → 展示 JSON 中 `fix_hint`，不自动安装

## 工作流衔接

| 方向 | Skill |
|------|-------|
| 上游 | [/init-win-env](../init-win-env/SKILL.md) |
| 下游 | [/init-git-convention](../init-git-convention/SKILL.md) |

> 探测完成。建议下一步：`/init-git-convention`

**Cursor**：见 [README §Cursor 等效调用](../README.md#cursor-等效调用全-skill-通用)

## 参考

- [09-toolchain-config.md](../../instructions/09-toolchain-config.md)
- [04-shell-config.md](../../instructions/04-shell-config.md)
