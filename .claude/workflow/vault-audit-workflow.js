// ============================================================
// vault-audit-workflow.js
// Vault 语义审查 Workflow — 并行审查 A–G 7 大模块
//
// 使用方式：
//   1) 主会话运行 vault-audit.py full --json 获取机械审计结果
//   2) 将 JSON 通过 args.mechanical_json 传入本 Workflow
//   3) Workflow 执行语义审查、对抗性验证，生成汇总报告
//
// 预算感知：
//   args.budget_level 控制审查深度：
//     "high"   — S1/S2/S3 全面审查 + 对抗性验证（默认）
//     "medium" — S1/S2 审查，跳过验证
//     "low"    — 仅 S1 高优先级审查，跳过验证
//
// 错误容忍：
//   单个模块 agent 失败不影响其他模块（.filter(Boolean)）
//   失败模块在报告中标明
// ============================================================

export const meta = {
  name: 'vault-audit-semantic',
  description:
    '并行审查 A–G 7 大模块的语义正确性，对 S1 发现做对抗性核实，汇总为结构化报告供主会话修复环使用',
  phases: [
    { title: 'Pre-flight', detail: '校验输入、创建临时目录、准备模块数据' },
    { title: 'Parallel Semantic Review', detail: '7 个 agent 分别审查 A–G 模块，写入独立临时文件' },
    { title: 'Adversarial Verification', detail: '对 S1 发现做 refute 核实，排除误报（budget 充足时执行）' },
    { title: 'Report Generation', detail: '合并机械 + 语义 + 验证结果，输出审计报告 Markdown' },
    { title: 'Cleanup & Return', detail: '清理临时文件，返回结构化结果给主会话' },
  ],
}

// ============================================================
// 常量
// ============================================================

const VAULT_ROOT = '.'

// 临时目录：每个 agent 写入独立 JSON 文件，绝无写冲突
const TEMP_DIR = '.claude/workflow/temp'

// A–G 模块定义（笔记数于 2026-07-07 实测）
const MODULES = [
  { id: 'A', name: 'A-编程语言',        count: 8 },
  { id: 'B', name: 'B-构建与脚本',      count: 10 },
  { id: 'C', name: 'C-Linux生态',       count: 34 },
  { id: 'D', name: 'D-系统与架构',      count: 12 },
  { id: 'E', name: 'E-AI与Agent协同开发', count: 11 },
  { id: 'F', name: 'F-版本管理',        count: 4 },
  { id: 'G', name: 'G-语言与标记',      count: 3 },
]

// 审查深度级别
const BUDGET_HIGH = 'high'
const BUDGET_MEDIUM = 'medium'
const BUDGET_LOW = 'low'

// ============================================================
// Phase 1: Pre-flight
// ============================================================

phase('Pre-flight')

log('=== Phase 1: Pre-flight ===')

// 确定预算级别
const budgetLevel = args.budget_level || BUDGET_HIGH
log('Budget level: ' + budgetLevel)

// 确定报告日期（从 args 或 Workflow 内置 __date__）
const reportDate =
  args.report_date || (typeof __date__ !== 'undefined' ? __date__ : 'unknown-date')
const REPORT_PATH = '.claude/plan/' + reportDate + '-vault-audit-report.md'
log('Report path: ' + REPORT_PATH)

// 创建临时目录
await agent('mkdir -p ' + TEMP_DIR, {
  label: 'init-temp-dir',
  isolation: 'worktree',
})

// 获取机械审计结果
// 优先从 args.mechanical_json 读取（主会话预跑 vault-audit.py 传入）
// 回退到直接运行 vault-audit.py full --json
const mechanicalInput = args.mechanical_json || {}

let mechanical
if (mechanicalInput.mode) {
  mechanical = mechanicalInput
  log('Using mechanical JSON from args')
} else {
  log('No mechanical JSON provided via args, running vault-audit.py')
  mechanical = await agent(
    [
      'cd ' + VAULT_ROOT,
      'python .claude/skills/vault-audit/scripts/vault-audit.py full --json',
    ].join(' && '),
    {
      label: 'run-mechanical-audit',
      isolation: 'worktree',
      schema: {
        type: 'object',
        properties: {
          mode: { type: 'string' },
          p0: { type: 'number' },
          p1: { type: 'number' },
          p2: { type: 'number' },
          issues: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                severity: { type: 'string' },
                id: { type: 'string' },
                message: { type: 'string' },
              },
              required: ['severity', 'id', 'message'],
            },
          },
        },
        required: ['mode', 'p0', 'p1', 'p2', 'issues'],
      },
    },
  )
}

log(
  'Mechanical audit: P0=' + mechanical.p0 +
  ' P1=' + mechanical.p1 +
  ' P2=' + mechanical.p2,
)

// 按模块分组机械问题（兼容有无 per_module 字段两种输入）
const perModuleIssues = buildPerModuleIssues(mechanical)

function buildPerModuleIssues(mech) {
  // 如果机械结果已有 per_module 分组，直接使用
  if (mech.per_module) {
    return mech.per_module
  }

  // 否则从 issues 数组中按文件路径首段模块名分组
  const result = {}
  for (const mod of MODULES) {
    result[mod.name] = {
      files_count: 0,
      p0: 0,
      p1: 0,
      p2: 0,
      issues: [],
      files_with_issues: [],
    }
  }

  for (const issue of mech.issues || []) {
    const match = issue.message.match(/^([A-G]-[^/]+)/)
    if (match && result[match[1]]) {
      const mod = result[match[1]]
      mod.issues.push(issue)
      mod['p' + issue.severity.slice(1).toLowerCase()]++
      const fileMatch = issue.message.match(/([A-G]-[^:]+?\.md)/)
      if (fileMatch && !mod.files_with_issues.includes(fileMatch[1])) {
        mod.files_with_issues.push(fileMatch[1])
      }
    }
  }

  return result
}

log('Pre-flight complete: ' + MODULES.length + ' modules ready')

// ============================================================
// Phase 2: Parallel Semantic Review
// ============================================================

phase('Parallel Semantic Review')

log('=== Phase 2: Parallel Semantic Review ===')
log('Launching ' + MODULES.length + ' parallel agents')

// 根据预算级别构造审查指令
function buildReviewInstructions(level) {
  if (level === BUDGET_LOW) {
    return (
      '\n## 预算约束（低预算模式）\n' +
      '由于 token 预算有限，请聚焦 **S1（明显错误）** 审查：\n\n' +
      '### S1 — 明显错误（必须修复）\n' +
      '- 事实性错误（API 用法错误、数据错误、命令参数错误等）\n' +
      '- 指向已删除文件的 wikilink\n' +
      '- 代码示例无法运行或明显过时\n' +
      '- 与 vault 当前结构矛盾的引用\n\n' +
      '对 S2 和 S3 请在 findings 中标记 "deferred: low budget" 即可。\n'
    )
  }

  if (level === BUDGET_MEDIUM) {
    return (
      '\n## 审查维度（中等预算 — S1 + S2）\n\n' +
      '### S1 — 明显错误（必须修复）\n' +
      '- 事实性错误（API 用法错误、数据错误、命令参数错误等）\n' +
      '- 指向已删除文件的 wikilink\n' +
      '- 代码示例无法运行或明显过时\n' +
      '- 与 vault 当前结构矛盾的引用\n\n' +
      '### S2 — 过时可参考\n' +
      '- 内容正确但绑定特定版本/工程\n' +
      '- 缺少中英双语对照（双分区不完整）\n' +
      '- 交叉引用可优化\n' +
      '- 缺少日期标注或"已过时"提示\n\n' +
      'S3 跳过，标记 "deferred: medium budget"。\n'
    )
  }

  // high (default) — 完整审查
  return (
    '\n## 审查维度（每篇笔记逐项核对）\n\n' +
    '### S1 — 明显错误（必须修复）\n' +
    '- 事实性错误（API 用法错误、数据错误、命令参数错误等）\n' +
    '- 指向已删除文件的 wikilink（机械 M1 未覆盖到的动态链接）\n' +
    '- 代码示例无法运行或明显过时\n' +
    '- 与 vault 当前结构矛盾的引用\n\n' +
    '### S2 — 过时可参考\n' +
    '- 内容正确但绑定特定版本/工程\n' +
    '- 缺少中英双语对照（双分区不完整）\n' +
    '- 交叉引用可优化\n' +
    '- 缺少日期标注或"已过时"提示\n\n' +
    '### S3 — 需重写（记入 backlog）\n' +
    '- 结构混乱，难以阅读\n' +
    '- 内容严重过时，需要全部重写\n' +
    '- 与其他笔记严重重复，需要合并\n'
  )
}

const reviewInstructions = buildReviewInstructions(budgetLevel)

// 核心并行 fan-out：7 个 agent 同时审查各自模块
const moduleReviews = await parallel(
  MODULES.map(
    (mod) => () => {
      const modMechanical =
        perModuleIssues[mod.name] || {
          files_count: 0, p0: 0, p1: 0, p2: 0,
          issues: [], files_with_issues: [],
        }
      const mechanicalIssuesJSON = JSON.stringify(
        {
          issues: modMechanical.issues || [],
          p0: modMechanical.p0,
          p1: modMechanical.p1,
          p2: modMechanical.p2,
        },
        null,
        2,
      )

      const filesWithIssues = modMechanical.files_with_issues || []

      const prompt = [
        '你是一个知识库语义审查专家。请审查模块 **' + mod.name + '** 的全部笔记。',
        '',
        '## 模块信息',
        '- 模块路径：`' + mod.name + '`',
        '- 笔记总数：' + mod.count + ' 篇',
        '',
        '## 审查方法',
        '1. 使用 `ls -R ' + mod.name + '/` 或其他 shell 命令枚举模块内全部 .md 文件',
        '2. 逐个读取每篇笔记的文件内容',
        '3. 对照审查维度逐项核对',
        '4. 优先阅读机械审计已报问题的文件',
        '',
        '## 本模块机械审计预检结果',
        '```json',
        mechanicalIssuesJSON,
        '```',
        '',
        filesWithIssues.length > 0
          ? '## 机械问题文件速查\n' + filesWithIssues.map((f) => '- `' + f + '`').join('\n')
          : '## 机械问题文件速查\n（本模块无机械问题）',
        '',
        reviewInstructions,
        '',
        '## 重要规则',
        '1. 严格只评估 `' + mod.name + '/` 内的文件，不要跨越到其他模块',
        '2. 不要修改任何文件！只输出分析 JSON',
        '3. S1 发现必须附带具体修复建议（可操作的编辑指令）',
        '4. S2 发现给出改进方向即可',
        '5. S3 发现简要说明重写原因',
        '6. 优先关注机械审计已报问题的文件',
        '7. 如果某文件没有问题，标记 level="ok" 并留空 findings 数组',
        '',
        '## 输出格式（严格 JSON，不要用代码块包裹）',
        '{',
        '  "module": "' + mod.name + '",',
        '  "files": [',
        '    {',
        '      "path": "' + mod.name + '/子目录/文件名.md",',
        '      "title": "笔记标题（# 1. 后的内容）",',
        '      "level": "ok|S1|S2|S3",',
        '      "findings": ["具体发现1", "具体发现2"],',
        '      "fix_suggestion": "修复建议（S3 填 \\"需重写\\"）",',
        '      "related_mechanical": ["M1断链: xxx"]',
        '    }',
        '  ],',
        '  "summary": { "total": ' + mod.count + ', "ok": 0, "S1": 0, "S2": 0, "S3": 0 }',
        '}',
      ].join('\n')

      return agent(prompt, {
        label: 'review-' + mod.id,
        schema: {
          type: 'object',
          properties: {
            module: { type: 'string' },
            files: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  path: { type: 'string' },
                  title: { type: 'string' },
                  level: { type: 'string', enum: ['ok', 'S1', 'S2', 'S3'] },
                  findings: { type: 'array', items: { type: 'string' } },
                  fix_suggestion: { type: 'string' },
                  related_mechanical: { type: 'array', items: { type: 'string' } },
                },
                required: ['path', 'level'],
              },
            },
            summary: {
              type: 'object',
              properties: {
                total: { type: 'number' },
                ok: { type: 'number' },
                S1: { type: 'number' },
                S2: { type: 'number' },
                S3: { type: 'number' },
              },
              required: ['total', 'ok', 'S1', 'S2', 'S3'],
            },
          },
          required: ['module', 'files', 'summary'],
        },
      })
    },
  ),
)

// 过滤失败的 agent（null = 失败/超时）
const validReviews = moduleReviews.filter(Boolean)
const failedModules = MODULES.filter(
  (m) => !validReviews.find((r) => r.module === m.name),
)

log(
  'Parallel review complete: ' + validReviews.length +
  '/' + MODULES.length + ' modules succeeded',
)
if (failedModules.length > 0) {
  log('WARNING: Failed modules: ' + failedModules.map((m) => m.name).join(', '))
}

// 将每个模块的结果写入独立临时文件
const writeResults = await parallel(
  validReviews.map(
    (review) => () => {
      const modEntry = MODULES.find((m) => m.name === review.module)
      const modId = modEntry ? modEntry.id : 'X'
      const tempFile = TEMP_DIR + '/module-' + modId + '.json'
      const jsonContent = JSON.stringify(review, null, 2)

      return agent(
        [
          "cat > '" + tempFile + "' << 'JSONEOF'",
          jsonContent,
          'JSONEOF',
          "echo 'Written: " + tempFile + "'",
        ].join('\n'),
        {
          label: 'write-' + modId,
          isolation: 'worktree',
        },
      )
    },
  ),
)
log(
  'Written ' + writeResults.filter(Boolean).length +
  ' module result files to ' + TEMP_DIR,
)

// 汇总统计数据
const totalReviewed = validReviews.reduce((s, r) => s + (r.summary.total || 0), 0)
const totalOk = validReviews.reduce((s, r) => s + (r.summary.ok || 0), 0)
const totalS1 = validReviews.reduce((s, r) => s + (r.summary.S1 || 0), 0)
const totalS2 = validReviews.reduce((s, r) => s + (r.summary.S2 || 0), 0)
const totalS3 = validReviews.reduce((s, r) => s + (r.summary.S3 || 0), 0)
log(
  'Semantic summary: OK=' + totalOk +
  ' S1=' + totalS1 +
  ' S2=' + totalS2 +
  ' S3=' + totalS3,
)

// ============================================================
// Phase 3: Adversarial Verification
// ============================================================

phase('Adversarial Verification')

log('=== Phase 3: Adversarial Verification ===')

let verifiedFindings = []

// 低预算模式或没有 S1 发现时跳过验证
if (budgetLevel === BUDGET_LOW) {
  log('Low budget mode: skipping adversarial verification')
} else if (totalS1 === 0) {
  log('No S1 findings, skipping verification')
} else {
  // 收集所有 S1 发现
  const allS1Findings = []
  for (const review of validReviews) {
    for (const file of review.files) {
      if (file.level === 'S1') {
        allS1Findings.push({
          module: review.module,
          path: file.path,
          findings: file.findings || [],
          fix_suggestion: file.fix_suggestion || '',
        })
      }
    }
  }

  log('Found ' + allS1Findings.length + ' S1 findings, launching verifications')

  // 按模块分组，每组一个验证 agent
  const s1ByModule = {}
  for (const f of allS1Findings) {
    if (!s1ByModule[f.module]) {
      s1ByModule[f.module] = []
    }
    s1ByModule[f.module].push(f)
  }

  const verificationAgents = Object.entries(s1ByModule).map(
    ([modName, findings]) => () => {
      const findingsJSON = JSON.stringify(findings, null, 2)

      return agent(
        [
          '你是一个对抗性验证专家。请核实以下 **' + modName + '** 模块的 S1（明显错误）发现是否属实。',
          '',
          '## 待核实列表',
          '```json',
          findingsJSON,
          '```',
          '',
          '## 验证方法',
          '对于每条发现：',
          '1. 读取对应笔记文件，确认上下文',
          '2. 如果发现是正确的（确实是错误）→ marked: "CONFIRMED"',
          '3. 如果发现是误报（文件内容实际上正确）→ marked: "REFUTED"',
          '4. 如果不确定 → marked: "UNCLEAR"',
          '',
          '## 输出格式（严格 JSON，不要用代码块包裹）',
          '{',
          '  "module": "' + modName + '",',
          '  "verifications": [',
          '    {',
          '      "file": "文件路径",',
          '      "finding": "原发现描述",',
          '      "marked": "CONFIRMED|REFUTED|UNCLEAR",',
          '      "reason": "核实依据（引用具体文件内容）"',
          '    }',
          '  ]',
          '}',
        ].join('\n'),
        {
          label: 'verify-' + modName.substring(0, 4),
          schema: {
            type: 'object',
            properties: {
              module: { type: 'string' },
              verifications: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    file: { type: 'string' },
                    finding: { type: 'string' },
                    marked: { type: 'string', enum: ['CONFIRMED', 'REFUTED', 'UNCLEAR'] },
                    reason: { type: 'string' },
                  },
                  required: ['file', 'finding', 'marked', 'reason'],
                },
              },
            },
            required: ['module', 'verifications'],
          },
        },
      )
    },
  )

  const verificationResults = await parallel(verificationAgents)
  const validVerifications = verificationResults.filter(Boolean)

  verifiedFindings = validVerifications.flatMap((v) => v.verifications || [])

  const confirmed = verifiedFindings.filter((f) => f.marked === 'CONFIRMED').length
  const refuted = verifiedFindings.filter((f) => f.marked === 'REFUTED').length
  const unclear = verifiedFindings.filter((f) => f.marked === 'UNCLEAR').length
  log(
    'Verification complete: CONFIRMED=' + confirmed +
    ' REFUTED=' + refuted +
    ' UNCLEAR=' + unclear,
  )

  // 写入验证结果到临时文件
  await agent(
    [
      "cat > '" + TEMP_DIR + "/verification.json' << 'JSONEOF'",
      JSON.stringify(verifiedFindings, null, 2),
      'JSONEOF',
      "echo 'Written: " + TEMP_DIR + "/verification.json'",
    ].join('\n'),
    {
      label: 'write-verification',
      isolation: 'worktree',
    },
  )
}

// ============================================================
// Phase 4: Report Generation
// ============================================================

phase('Report Generation')

log('=== Phase 4: Report Generation ===')

// 构建分模块摘要表格行
const moduleTableRows = validReviews
  .map((r) => {
    const mod = MODULES.find((m) => m.name === r.module)
    const mid = mod ? mod.id : '?'
    return (
      '| ' + mid + ' | ' + r.module + ' | ' + r.summary.total +
      ' | ' + r.summary.ok + ' | ' + r.summary.S1 +
      ' | ' + r.summary.S2 + ' | ' + r.summary.S3 + ' |'
    )
  })
  .join('\n')

const failedModuleRows =
  failedModules.length > 0
    ? failedModules
        .map(
          (m) =>
            '| ' + m.id + ' | ' + m.name +
            ' | — | — | — | — | — | FAILED |',
        )
        .join('\n')
    : ''

// 构建 S1 详细列表
let s1Details = '（无 S1 发现）'
if (totalS1 > 0) {
  const lines = []
  for (const review of validReviews) {
    const s1Files = review.files.filter((f) => f.level === 'S1')
    for (const f of s1Files) {
      const findings = (f.findings || []).join('; ')
      lines.push('- **' + f.path + '**: ' + findings)
      if (f.fix_suggestion) {
        lines.push('  - 修复建议: ' + f.fix_suggestion)
      }
    }
  }
  s1Details = lines.join('\n')
}

// 构建已验证的 S1 表格
let verifiedS1Table = '（无需验证或无 S1 发现）'
if (verifiedFindings.length > 0) {
  const rows = verifiedFindings
    .map(
      (f) =>
        '| ' + f.file + ' | ' + f.finding.substring(0, 60) +
        '... | ' + f.marked + ' | ' + f.reason.substring(0, 60) + '... |',
    )
    .join('\n')
  verifiedS1Table =
    '| 文件 | 发现 | 结果 | 依据 |\n|------|------|------|------|\n' + rows
}

// 构建机械问题分组
const p0Issues = (mechanical.issues || []).filter((i) => i.severity === 'P0')
const p1Issues = (mechanical.issues || []).filter((i) => i.severity === 'P1')
const p2Issues = (mechanical.issues || []).filter((i) => i.severity === 'P2')

const p0List =
  p0Issues.length > 0
    ? p0Issues.map((i) => '- [' + i.id + '] ' + i.message).join('\n')
    : '（无 P0 问题）'
const p1List =
  p1Issues.length > 0
    ? p1Issues.map((i) => '- [' + i.id + '] ' + i.message).join('\n')
    : '（无 P1 问题）'
const p2List =
  p2Issues.length > 0
    ? p2Issues.map((i) => '- [' + i.id + '] ' + i.message).join('\n')
    : '（无 P2 问题）'

// S2/S3 汇总
const s2Lines = []
const s3Lines = []
for (const review of validReviews) {
  for (const f of review.files) {
    if (f.level === 'S2') {
      s2Lines.push('- **' + f.path + '**: ' + (f.findings || []).join('; '))
    } else if (f.level === 'S3') {
      s3Lines.push(
        '- **' + f.path + '**: ' + (f.findings || []).join('; ') +
        ' — ' + (f.fix_suggestion || '需重写'),
      )
    }
  }
}
const s2Details = s2Lines.length > 0 ? s2Lines.join('\n') : '（无 S2 发现）'
const s3Details = s3Lines.length > 0 ? s3Lines.join('\n') : '（无 S3 发现）'

// 失败模块说明
const failedSection =
  failedModules.length > 0
    ? '## 未完成模块\n\n' +
      failedModules
        .map((m) => '- **' + m.name + '**（审查失败，需重跑 Workflow 或单独审查）')
        .join('\n') +
      '\n'
    : ''

// 验证结果 JSON
const verificationJSON =
  verifiedFindings.length > 0
    ? JSON.stringify(verifiedFindings, null, 2)
    : '未执行验证（无 S1 发现或低预算模式）'

// 报告 prompt
const reportPrompt = [
  '你是 vault 审计报告撰写专家。',
  '请根据以下数据生成一份完整的 Markdown 审计报告。',
  '',
  '## 报告路径',
  REPORT_PATH,
  '',
  '## 模板要求',
  '请严格按照以下模板结构输出纯 Markdown（不要用代码块包裹全文）：',
  '',
  '# Vault Audit Report — ' + reportDate,
  '',
  '> 模式: workflow（机械 + 并行语义审查）',
  '> 脚本: vault-audit.py + .claude/workflow/vault-audit-workflow.js',
  '> 预算级别: ' + budgetLevel,
  '',
  '## 摘要',
  '',
  '| 类别 | 计数 | 状态 |',
  '|------|------|------|',
  '| P0（机械） | ' + mechanical.p0 + ' | |',
  '| P1（机械） | ' + mechanical.p1 + ' | |',
  '| P2（机械） | ' + mechanical.p2 + ' | |',
  '| S1（语义） | ' + totalS1 + ' | |',
  '| S2（语义） | ' + totalS2 + ' | |',
  '| S3（语义） | ' + totalS3 + ' | |',
  '',
  '## 机械问题',
  '',
  '### P0',
  p0List,
  '',
  '### P1',
  p1List,
  '',
  '### P2',
  p2List,
  '',
  '## 分模块语义审查',
  '',
  '| 模块 ID | 模块名 | 笔记数 | OK | S1 | S2 | S3 | 结论 |',
  '|---------|--------|--------|----|----|----|----|------|',
  moduleTableRows,
  failedModuleRows,
  '',
  '## S1 发现详情',
  s1Details,
  '',
  '## 对抗性验证结果',
  verifiedS1Table,
  '',
  '## S2 改进建议',
  s2Details,
  '',
  '## S3 需重写 / 未决项',
  s3Details,
  '',
  failedSection,
  '## 修复批次建议',
  '',
  '| 批次 | 优先级 | 说明 |',
  '|------|--------|------|',
  '| B0 | 基础设施 | 换行符统一（git add --renormalize）、.gitkeep 更新 |',
  '| B1 | P0/P1 机械 | 断链修复、图片修复、索引漂移、标题格式 |',
  '| B2 | 结构 P2 / S1 | 序号冲突、孤立笔记、已确认的 S1 语义错误 |',
  '| B3 | S2 改进 | 过时标注、双语补充、交叉引用优化 |',
  '| B4 | S3 重写 | backlog 项（由用户决策） |',
  '',
  '## 输入数据',
  '',
  '### 机械审计摘要',
  '- 审计模式: ' + mechanical.mode,
  '- P0: ' + mechanical.p0 + ', P1: ' + mechanical.p1 + ', P2: ' + mechanical.p2,
  '- 总问题数: ' + (mechanical.issues || []).length,
  '',
  '### 各模块语义审查结果',
  validReviews
    .map(
      (r) =>
        '#### ' + r.module +
        '\n- 总笔记: ' + r.summary.total +
        '\n- OK: ' + r.summary.ok +
        '\n- S1: ' + r.summary.S1 +
        '\n- S2: ' + r.summary.S2 +
        '\n- S3: ' + r.summary.S3,
    )
    .join('\n\n'),
  '',
  failedModules.length > 0
    ? '### 失败模块\n' +
      failedModules.map((m) => '- ' + m.name + '（agent 超时/失败，需重跑）').join('\n')
    : '',
  '',
  '### 对抗性验证结果',
  '```json',
  verificationJSON,
  '```',
  '',
  '## 要求',
  '1. 输出纯 Markdown，不要用代码块包裹全文',
  '2. 所有机械问题按 P0/P1/P2 分组列出具体文件',
  '3. 每个模块的 S1 发现列出到具体笔记和问题描述',
  '4. 修复批次按严重度排序',
  '5. 失败模块在表格中标注 FAILED，并在末尾特别说明',
  '6. 确保 Markdown 表格对齐、格式正确',
  '7. 不要写当前日期时间，用报告文件名中的日期即可',
].join('\n')

const report = await agent(reportPrompt, {
  label: 'generate-report',
})

// 写入报告文件
await agent(
  [
    "cat > '" + REPORT_PATH + "' << 'REPORTEOF'",
    report,
    'REPORTEOF',
    "echo 'Report written: " + REPORT_PATH + "'",
  ].join('\n'),
  {
    label: 'write-report',
    isolation: 'worktree',
  },
)

log('Report written to ' + REPORT_PATH)

// ============================================================
// Phase 5: Cleanup & Return
// ============================================================

phase('Cleanup & Return')

log('=== Phase 5: Cleanup & Return ===')

// 清理临时文件
await agent("rm -f '" + TEMP_DIR + "'/*.json", {
  label: 'cleanup-temp',
  isolation: 'worktree',
})

log('Temporary files cleaned')

// 计算验证统计
const confirmedCount = verifiedFindings.filter((f) => f.marked === 'CONFIRMED').length
const refutedCount = verifiedFindings.filter((f) => f.marked === 'REFUTED').length
const unclearCount = verifiedFindings.length - confirmedCount - refutedCount

// 返回结构化结果给主会话
return {
  meta: {
    workflow: 'vault-audit-semantic',
    budget_level: budgetLevel,
    report_date: reportDate,
    report_path: REPORT_PATH,
  },

  mechanical: {
    p0: mechanical.p0,
    p1: mechanical.p1,
    p2: mechanical.p2,
    issue_count: (mechanical.issues || []).length,
    mode: mechanical.mode,
  },

  semantic: {
    modules_reviewed: validReviews.length,
    modules_total: MODULES.length,
    failed_modules: failedModules.map((m) => m.name),
    total_notes_reviewed: totalReviewed,
    total_ok: totalOk,
    total_S1: totalS1,
    total_S2: totalS2,
    total_S3: totalS3,
  },

  verification: {
    performed: verifiedFindings.length > 0,
    total: verifiedFindings.length,
    confirmed: confirmedCount,
    refuted: refutedCount,
    unclear: unclearCount,
  },

  module_reviews: validReviews.map((r) => ({
    module: r.module,
    summary: r.summary,
    s1_files: r.files
      .filter((f) => f.level === 'S1')
      .map((f) => ({
        path: f.path,
        findings: f.findings,
        fix_suggestion: f.fix_suggestion,
      })),
    s2_files: r.files
      .filter((f) => f.level === 'S2')
      .map((f) => ({
        path: f.path,
        findings: f.findings,
      })),
    s3_files: r.files
      .filter((f) => f.level === 'S3')
      .map((f) => ({
        path: f.path,
        findings: f.findings,
      })),
  })),

  verified_findings: verifiedFindings,
  report_path: REPORT_PATH,
}
