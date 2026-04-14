# 源码安全审计

OpenCode 安全审计技能，基于 AST-grep 规则库进行自动化安全漏洞检测与分析，支持 5 种编程语言，覆盖 9 类常见漏洞类型。

> ⚠️ **注意**：此工具专为 AI 助手设计，用于自动化代码安全审计。终端用户请勿直接使用，应通过 OpenCode 等 AI 工具调用。

## 功能特性

### 支持的漏洞类型

| 漏洞类型 | CWE ID | 风险等级 | 检测规则文件 |
|---------|--------|---------|-------------|
| SQL注入 | CWE-89 | 严重 | `sql-injection-{lang}.yml` |
| XSS跨站脚本 | CWE-79 | 高危 | `xss-{lang}.yml` |
| 命令执行 | CWE-78 | 严重 | `command-exec-{lang}.yml` |
| 反序列化漏洞 | CWE-502 | 严重 | `deserialization-{lang}.yml` |
| 路径穿越 | CWE-22 | 高危 | `path-traversal-{lang}.yml` |
| SSRF | CWE-918 | 高危 | `ssrf-{lang}.yml` |
| XXE | CWE-611 | 中危 | `xxe-{lang}.yml` |
| 鉴权缺陷 | CWE-287/306 | 中危 | `auth-defects-{lang}.yml` |
| 硬编码密钥 | CWE-798 | 高危 | `hardcoded-secrets-{lang}.yml` |

### 支持的语言

- **Java** (`.java`) - 完整的安全规则集
- **Go** (`.go`) - Go语言特定API检测
- **Python** (`.py`) - Python框架和库支持
- **PHP** (`.php`) - PHP常见漏洞模式
- **C#** (`.cs`) - .NET平台安全检测

## 使用方法

此安全审计技能通过 OpenCode 等 AI 工具调用。用户只需提供目标代码路径，AI 将自动完成以下流程：

1. **执行 AST-grep 扫描** - AI 自动调用 ast-grep CLI 进行批量扫描
2. **深度分析漏洞** - 基于扫描结果验证候选漏洞，评估真实性和风险等级
3. **误报自动确认** - 对疑似误报进行深度复核，分析代码上下文和数据流
4. **生成审计报告** - 输出中文安全报告，包含复现步骤、调用链、修复建议

### AI 调用示例

```
用户: 审计 /path/to/project 的安全漏洞

AI: 我将为您进行安全审计，步骤如下：
     1. 使用 AST-grep 扫描目标代码
     2. 分析扫描结果，验证漏洞
     3. 生成安全审计报告

     [AI 自动执行扫描和分析...]

     审计完成！生成报告: security_audit_report_20250409.md
```

## 审计报告格式

AI 生成的安全审计报告包含以下必需字段：

1. **复现步骤** - 包含 HTTP 请求包示例
2. **漏洞入口** - 漏洞的入口点和攻击向量
3. **调用链** - 从入口到危险操作的完整调用链
4. **风险等级** - 严重/高危/中危/低危
5. **修复建议** - 具体的修复代码示例
6. **疑似误报说明** - 误报可能性分析和判断依据

### 报告示例

```markdown
# 安全审计报告

**生成时间**: 2025-04-09 14:30:00

## 执行摘要

### 扫描概览
- **扫描目标**: `/path/to/project`
- **扫描文件数**: 156 个
- **扫描耗时**: 12.5 秒

### 漏洞统计
| 风险等级 | 数量 | 占比 |
|---------|------|------|
| 🔴 严重 | 1 | 25.0% |
| 🟠 高危 | 1 | 25.0% |
| 🟡 中危 | 1 | 25.0% |
| 🟢 低危 | 1 | 25.0% |

## 🔴 严重

### 1. SQL注入漏洞

#### 📋 基本信息
- **规则ID**: `sql-injection-python`
- **CWE编号**: CWE-89
- **文件位置**: `app/database.py:42`
- **置信度**: 95%

#### 📝 漏洞描述
用户输入直接拼接到SQL查询中，存在SQL注入风险...

#### 🔍 复现步骤
```http
POST /api/users HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

username=admin' OR '1'='1'--&password=test
```

#### 🔗 调用链
```
+-- 漏洞入口
|   get_user
|   (app/views.py:25)
|
+-- 中间调用
|   [1] fetch_user_data
|       (app/service.py:38)
|
+-- 危险操作
    query_user
    (app/database.py:42)
```

#### 🔧 修复建议
```python
# 修复前（存在漏洞）
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")

# 修复后（安全）
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```
```

## 项目结构

```
security-audit/
├── SKILL.md                    # 技能定义文件，AI审计流程核心文档
├── README.md                   # 本文件
├── references/                 # 参考文档和规则
│   ├── rules/                  # AST-grep 规则文件 (45+ 个规则)
│   │   ├── sql-injection-*.yml # SQL注入规则
│   │   ├── command-exec-*.yml  # 命令执行规则
│   │   ├── xss-*.yml          # XSS规则
│   │   ├── path-traversal-*.yml # 路径穿越规则
│   │   ├── ssrf-*.yml         # SSRF规则
│   │   ├── xxe-*.yml          # XXE规则
│   │   ├── deserialization-*.yml # 反序列化规则
│   │   ├── auth-defects-*.yml    # 鉴权缺陷规则
│   │   └── hardcoded-secrets-*.yml # 硬编码密钥规则
│   ├── cwe-mappings.md        # CWE 漏洞映射表
│   └── remediation-guide.md   # 漏洞修复指南
└── test-samples/              # 测试样本代码
    ├── sqli_*.py/*.php/*.go/*.java/*.cs    # SQL注入示例
    ├── python_cmd_exec.py     # Python命令执行示例
    ├── php_cmd_exec.php       # PHP命令执行示例
    └── ...                    # 其他漏洞类型示例
```

## 规则说明

每个规则文件使用 YAML 格式定义，用于 AST-grep 引擎检测特定漏洞模式。

### 规则示例

`sql-injection-python.yml`:

```yaml
id: sql-injection-python
severity: CRITICAL
cwe: CWE-89
language: python
message: 发现潜在的SQL注入漏洞
description: |
  用户输入直接拼接到SQL查询字符串中，存在SQL注入风险。
  攻击者可能通过构造特殊输入操控SQL查询逻辑。
remediation: |
  使用参数化查询替代字符串拼接：
  ```python
  cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
  ```

rule:
  pattern: |
    cursor.execute($QUERY)
  constraints:
    QUERY:
      contains: "f'"
```

### 规则文件命名规范

- `{vulnerability-type}-{language}.yml`
- 例如: `sql-injection-python.yml`, `command-exec-java.yml`

### 规则字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 规则唯一标识符 | `sql-injection-python` |
| `severity` | 严重程度 | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `cwe` | CWE编号 | `CWE-89` |
| `language` | 目标语言 | `python`, `java`, `go`, `php`, `csharp` |
| `message` | 简短描述 | 发现潜在的SQL注入漏洞 |
| `description` | 详细描述 | 漏洞原理、风险场景等 |
| `remediation` | 修复建议 | 具体代码示例 |
| `rule` | 检测规则 | AST-grep匹配模式 |

## 参考文档

- **SKILL.md** - AI审计流程详细说明（面向AI助手）
- **references/cwe-mappings.md** - CWE 漏洞分类映射表
- **references/remediation-guide.md** - 各类漏洞的修复指南

## 贡献指南

1. 复刻本仓库
2. 创建特性分支 (`git checkout -b feature/new-rule`)
3. 提交更改 (`git commit -m 'feat: add new rule'`)
4. 推送到分支 (`git push origin feature/new-rule`)
5. 创建拉取请求

## 相关链接

- [AST-grep 官方文档](https://ast-grep.github.io/)
- [CWE 官方网站](https://cwe.mitre.org/)
- [OWASP Top 10](https://owasp.org/Top10/)

## 许可证

MIT License
