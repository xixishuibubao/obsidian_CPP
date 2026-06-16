#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan and fix unlabeled fenced code blocks in Obsidian vault."""

import os
import re
from collections import defaultdict

VAULT_ROOT = r'C:/Users/lichao/Desktop/code/study_cpp'
EXCLUDE_DIRS = {'.git', '.claude', '.obsidian', 'node_modules'}


def detect_language(code_lines):
    """Detect programming language from code content."""
    if not code_lines:
        return 'plain'

    code = '\n'.join(code_lines)

    # C/C++ patterns
    c_cpp_patterns = [
        r'#\s*include\s*[<"]', r'int\s+main\s*\(', r'void\s+\w+\s*\(',
        r'class\s+\w+', r'struct\s+\w+\s*\{', r'namespace\s+\w+',
        r'using\s+namespace', r'#\s*define\s+\w+', r'typedef\s+',
        r'std::', r'template\s*<', r'public:\s',
        r'private:\s', r'protected:\s', r'extern\s+"C"',
        r'#\s*ifndef\s+\w+', r'#\s*pragma\s+once', r'virtual\s+\w+\s*\(',
        r'constexpr', r'noexcept', r'override\s*;',
        r'printf\s*\(', r'fprintf\s*\(', r'sprintf\s*\(',
        r'FILE\s*\*', r'fopen\s*\(', r'malloc\s*\(', r'free\s*\(',
        r'sizeof\s*\(', r'__attribute__\s*\(\(',
    ]

    # Shell patterns
    shell_patterns = [
        r'^\s*\$ ', r'^#!', r'^\s*g\+\+', r'^\s*gcc', r'^\s*gdb',
        r'^\s*make\s', r'^\s*cmake', r'^\s*git\s+', r'^\s*cd\s+',
        r'^\s*mkdir\s+', r'^\s*rm\s+', r'^\s*ls\s', r'^\s*cat\s+',
        r'^\s*echo\s+', r'^\s*export\s+', r'^\s*chmod\s+',
        r'^\s*sudo\s+', r'^\s*docker\s+', r'^\s*pip\s+',
        r'^\s*ssh\s+', r'^\s*scp\s+', r'^\s*tar\s+',
        r'^\s*wget\s+', r'^\s*curl\s+', r'^\s*find\s+',
        r'^\s*grep\s+', r'^\s*sed\s+', r'^\s*awk\s+',
        r'^\s*perf\s+', r'^\s*valgrind\s+', r'^\s*ps\s',
        r'^\s*kill\s+', r'^\s*top\s', r'^\s*htop\s',
        r'^\s*uname\s+', r'^\s*lscpu', r'^\s*dd\s+',
        r'^\s*apt\s+', r'^\s*objdump', r'^\s*nm\s+',
        r'^\s*ldd\s+', r'^\s*readelf\s+', r'^\s*patchelf\s+',
        r'^\s*aarch64-linux-gnu-', r'^\s*arm-linux-gnueabihf-',
        r'^\s*\./configure', r'^\s*go\s+', r'^\s*python3?\s+',
        r'^\s*nproc\s*$', r'^\s*ninja\s+',
    ]

    # Makefile patterns
    makefile_patterns = [
        r'^\w[\w.]*\s*:\s+\w', r'^\s*\$\(',
        r'^\s*\.PHONY', r'CROSS_COMPILE\s*[=?:]\+?=',
        r'CFLAGS\s*[=?:]\+?=', r'LDFLAGS\s*[=?:]\+?=',
        r'CC\s*[=?:]\+?=', r'CXX\s*[=?:]\+?=',
        r'AR\s*[=?:]\+?=', r'obj-m', r'kbuild',
    ]

    # Python patterns
    python_patterns = [
        r'^\s*def\s+\w+\s*\(', r'^\s*class\s+\w+\s*:',
        r'^\s*import\s+\w+', r'^\s*from\s+\w+\s+import',
        r'^\s*print\s*\(', r'^\s*self\s*\.',
        r'^\s*except\s+\w+\s+as\s', r'^\s*with\s+\w+',
        r'^\s*async\s+def\s', r'^\s*@\w+\.\w+\.',
    ]

    # PlantUML patterns
    plantuml_patterns = [
        r'@startuml', r'@enduml', r'participant\s', r'actor\s',
        r'usecase\s', r'boundary\s', r'entity\s',
        r'state\s+\w+\s*\{', r'note\s+(left|right|top|bottom)\s+of',
        r'activate\s+\w+', r'deactivate\s+\w+',
        r'alt\s+', r'else\s+', r'opt\s+', r'loop\s+',
        r'group\s+', r'box\s+', r'autonumber',
        r'left\s+skins?in\s', r'top\s+to\s+bottom\s+direction',
    ]

    # CSS patterns
    css_patterns = [
        r'^\s*[\w.#]+\s*\{', r'^\s*color\s*:', r'^\s*background',
        r'^\s*margin\s*:', r'^\s*padding\s*:', r'^\s*font-',
        r'^\s*border\s*:', r'^\s*display\s*:', r'^\s*position\s*:',
        r'^\s*@media', r'^\s*\.\w+\s*\{', r'^\s*#\w+\s*\{',
    ]

    # Lua patterns
    lua_patterns = [
        r'^\s*function\s+\w+\(', r'^\s*local\s+\w+\s*=',
        r'^\s*end\s*$', r'^\s*--\s*\[\[',
    ]

    # XML patterns
    xml_patterns = [
        r'<\?xml', r'<!DOCTYPE\s', r'<\w+\s+xmlns',
    ]

    # INI patterns
    ini_patterns = [
        r'^\[.*\]\s*$', r'^\s*\w+\s*=\s*\w+',
    ]

    # Check each language

    # Lua (check before C since Lua has function/end patterns)
    lua_score = 0
    for pat in lua_patterns:
        if re.search(pat, code, re.MULTILINE):
            lua_score += 1
    if lua_score >= 2:
        return 'lua'

    # C/C++
    cpp_score = 0
    c_score = 0
    for pat in c_cpp_patterns:
        if re.search(pat, code, re.MULTILINE):
            # Classify as C++ specific or C specific
            if pat in ['class\s+\w+', 'namespace\s+\w+', 'using\s+namespace',
                       'std::', 'template\s*<', 'public:\s', 'private:\s',
                       'protected:\s', 'constexpr', 'noexcept',
                       'override\s*;']:
                cpp_score += 2
            else:
                c_score += 1
                cpp_score += 1
    if cpp_score >= 2:
        # Differentiate C vs C++
        if re.search(r'(class\s+\w+|namespace|std::|template\s*<)', code):
            return 'cpp'
        return 'c'

    # Python
    for pat in python_patterns:
        if re.search(pat, code, re.MULTILINE):
            return 'python'

    # PlantUML
    for pat in plantuml_patterns:
        if re.search(pat, code):
            return 'plantuml'

    # Makefile
    for pat in makefile_patterns:
        if re.search(pat, code, re.MULTILINE):
            return 'makefile'

    # CSS
    for pat in css_patterns:
        if re.search(pat, code, re.MULTILINE):
            return 'css'

    # Shell
    for pat in shell_patterns:
        if re.search(pat, code, re.MULTILINE):
            return 'bash'

    # XML
    for pat in xml_patterns:
        if re.search(pat, code):
            return 'xml'

    # INI
    ini_section = re.search(r'^\[.*\]\s*$', code, re.MULTILINE)
    ini_kv = re.search(r'^\s*\w+\s*=\s*\w+', code, re.MULTILINE)
    if ini_section and ini_kv:
        return 'ini'

    # Default: plain text
    return 'plain'


def main():
    """Main entry point."""
    # Phase 1: Scan all files
    all_blocks = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        files.sort()
        for f in files:
            if not f.endswith('.md'):
                continue
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()

            in_fence = False
            fence_start = -1
            fence_lang = ''

            for i, raw in enumerate(lines):
                line = raw.rstrip('\n\r ')

                if in_fence:
                    if line == '```':
                        # closing fence
                        if fence_lang == '':
                            # unlabeled block
                            code_lines = [lines[k].rstrip() for k in range(fence_start + 1, i)]
                            lang = detect_language(code_lines)
                            all_blocks.append((fpath, fence_start, i, lang, code_lines))
                        in_fence = False
                        fence_start = -1
                        fence_lang = ''
                    continue

                if line == '```':
                    fence_start = i
                    fence_lang = ''
                    in_fence = True
                elif line.startswith('```') and len(line) > 3:
                    fence_start = i
                    fence_lang = line[3:].strip()
                    in_fence = True

    # Phase 2: Summary
    lang_counts = {}
    for _, _, _, lang, _ in all_blocks:
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    print('=== Unlabeled Fenced Code Blocks ===')
    print(f'Total: {len(all_blocks)}')
    print('By language:')
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        print(f'  {lang}: {count}')
    print()

    # Group by file
    by_file = defaultdict(list)
    for fpath, start_line, end_line, lang, code_lines in all_blocks:
        rel = os.path.relpath(fpath, VAULT_ROOT)
        preview = ' '.join(l[:60] for l in code_lines[:2] if l.strip())
        by_file[rel].append((start_line, end_line, lang, len(code_lines), preview))

    print('=== Files with unlabeled blocks ===')
    for rel, blocks in sorted(by_file.items()):
        print(f'\n{rel}:')
        for start, end, lang, count, preview in blocks:
            print(f'  L{start+1} [{lang}] ({count} lines) | {preview[:80]}')

    # Phase 3: Apply fixes
    print('\n\n=== Applying fixes ===')
    fixed_count = 0
    for fpath, start_line, end_line, lang, code_lines in all_blocks:
        with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()

        # Verify the line is still ```
        current_line = lines[start_line].rstrip('\n\r ')
        if current_line != '```':
            print(f'  SKIP (line changed): {os.path.relpath(fpath, VAULT_ROOT)}:{start_line+1}')
            continue

        # Replace ``` with ```lang
        old = lines[start_line]
        lines[start_line] = f'```{lang}\n'
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.writelines(lines)
        fixed_count += 1

    print(f'\nFixed {fixed_count} blocks out of {len(all_blocks)}')


if __name__ == '__main__':
    main()
