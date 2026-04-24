# Code Seer

Code Seer - 基于 ast-grep 规则库与 LLM 深度分析的自动化源码安全审计技能。

> **定位**：Code Seer 是 AI 助手的安全审计技能，通过 OpenCode 等 AI 工具调用，实现从扫描到报告的全自动化流程。

---

## 核心设计

**LLM 主导，ast-grep 辅助**

- ast-grep 仅用于快速定位可疑模式，无法理解业务逻辑
- LLM 主动阅读代码、追踪数据流、分析调用链、验证漏洞真实性
- 所有 ast-grep 命中结果必须经过 LLM 上下文审查

---

## 功能特性

### 支持的漏洞类型

| 漏洞类型 | CWE ID | 风险等级 | 检测规则 |
|---------|--------|---------|---------|
| SQL注入 | CWE-89 | 严重 | `sql-injection-{lang}.yml` |
| XSS跨站脚本 | CWE-79 | 高危 | `xss-{lang}.yml` |
| 命令执行 | CWE-78 | 严重 | `command-exec-{lang}.yml` |
| 反序列化漏洞 | CWE-502 | 严重 | `deserialization-{lang}.yml` |
| 路径穿越 | CWE-22 | 高危 | `path-traversal-{lang}.yml` |
| SSRF | CWE-918 | 高危 | `ssrf-{lang}.yml` |
| XXE | CWE-611 | 中危 | `xxe-{lang}.yml` |
| 鉴权缺陷 | CWE-287/306 | 中危 | `auth-defects-{lang}.yml` |
| 硬编码密钥 | CWE-798 | 高危 | `hardcoded-secrets-{lang}.yml` |
| SSTI | CWE-1336 | 严重 | `ssti-{lang}.yml` |
| NoSQL注入 | CWE-943 | 严重 | `nosql-injection-{lang}.yml` |
| 原型污染 | CWE-915 | 高危 | `prototype-pollution-{lang}.yml` |
| JNDI注入 | CWE-74/20 | 严重 | `jndi-injection-{lang}.yml` |
| 开放重定向 | CWE-601 | 中危 | `open-redirect-{lang}.yml` |

### 支持的语言

- **Java** (`.java`)
- **Go** (`.go`)
- **Python** (`.py`)
- **PHP** (`.php`)
- **C#** (`.cs`)
- **JavaScript/TypeScript** (`.js`/`.ts`)
- **Ruby** (`.rb`)
- **Rust** (`.rs`)
- **MyBatis Mapper XML** (`.xml`)

---

## 安装

### 前置依赖

- [ast-grep](https://ast-grep.github.io/) - AST 模式匹配引擎

### 安装 Code Seer

#### OpenCode

**方式一：使用安装脚本**

```bash
# 克隆仓库
git clone <repository-url> code-seer
cd code-seer

# 安装到 OpenCode 技能目录
./opencode-install.sh
```

**方式二：手动安装**

```bash
# 克隆仓库
git clone <repository-url> code-seer
cd code-seer

# 手动复制到 OpenCode 技能目录
mkdir -p ~/.config/opencode/skills/code-seer
cp SKILL.md ~/.config/opencode/skills/code-seer/
cp -r references/ ~/.config/opencode/skills/code-seer/
```

安装脚本/手动复制会将 `SKILL.md` 和 `references/` 复制到 `~/.config/opencode/skills/code-seer/`。

#### Claude Code

```bash
# 克隆仓库
git clone <repository-url> code-seer
cd code-seer

# 安装到 Claude Code 技能目录
mkdir -p ~/.claude/skills/code-seer
cp SKILL.md ~/.claude/skills/code-seer/
cp -r references/ ~/.claude/skills/code-seer/
```

#### Codex

```bash
# 克隆仓库
git clone <repository-url> code-seer
cd code-seer

# 安装到 Codex 技能目录
mkdir -p ~/.codex/skills/code-seer
cp SKILL.md ~/.codex/skills/code-seer/
cp -r references/ ~/.codex/skills/code-seer/
```

#### 其他 CLI 工具

对于其他支持自定义技能的 CLI 工具，手动复制 `SKILL.md` 和 `references/` 到对应的 skills 目录即可：

```bash
mkdir -p ~/.your-tool/skills/code-seer
cp SKILL.md ~/.your-tool/skills/code-seer/
cp -r references/ ~/.your-tool/skills/code-seer/
```

---

## 使用方法

Code Seer 设计为 AI 技能，用户只需向 AI 助手发出审计请求：

```
用户: 审计 /path/to/project 的安全漏洞

AI: 我将使用 Code Seer 为您进行安全审计：
     1. 执行 AST-grep 扫描
     2. LLM 深度分析漏洞
     3. 生成安全审计报告

     [AI 自动执行...]

     审计完成！生成报告: security_audit_report_20260421.md
```

AI 自动完成以下流程：
1. **AST-grep 扫描** - 批量扫描可疑代码模式
2. **LLM 深度分析** - 追踪数据流、验证漏洞真实性
3. **误报过滤** - 自动复核疑似误报
4. **生成报告** - 输出中文安全报告

---

## 项目结构

```
code-seer/
├── SKILL.md                    # AI 技能定义（审计流程核心）
├── README.md                   # 本文件
├── opencode-install.sh         # OpenCode 技能安装脚本
├── scripts/
│   └── test_rules.py           # 规则测试脚本
├── references/
│   ├── rules/                  # AST-grep 规则文件 (100 条)
│   │   ├── sql-injection-*.yml
│   │   ├── command-exec-*.yml
│   │   ├── xss-*.yml
│   │   ├── path-traversal-*.yml
│   │   ├── ssrf-*.yml
│   │   ├── xxe-*.yml
│   │   ├── deserialization-*.yml
│   │   ├── auth-defects-*.yml
│   │   ├── hardcoded-secrets-*.yml
│   │   ├── ssti-*.yml
│   │   ├── nosql-injection-*.yml
│   │   ├── prototype-pollution-*.yml
│   │   ├── jndi-injection-*.yml
│   │   └── open-redirect-*.yml
│   ├── cwe-mappings.md         # CWE 漏洞映射表
│   └── remediation-guide.md    # 漏洞修复指南
└── test-samples/               # 测试样本代码
    ├── sqli_*.py/*.php/*.go/*.java/*.cs
    ├── python_cmd_exec.py
    ├── php_cmd_exec.php
    └── ...
```

---

## 规则说明

### 规则字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 规则唯一标识 | `sql-injection-python` |
| `severity` | 严重程度 | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `cwe` | CWE 编号 | `CWE-89` |
| `language` | 目标语言 | `python`, `java`, `go`, `php`, `csharp`, `javascript`, `ruby`, `rust` |
| `message` | 简短描述 | 发现潜在的SQL注入漏洞 |
| `description` | 详细描述 | 漏洞原理、风险场景 |
| `remediation` | 修复建议 | 具体代码示例 |
| `rule` | 检测规则 | AST-grep 匹配模式 |

### 命名规范

- 格式：`{vulnerability-type}-{language}.yml`
- 示例：`sql-injection-python.yml`, `command-exec-java.yml`

---

## 许可证

MIT License
