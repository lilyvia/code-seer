---
name: security-audit
description: |
  源码安全审计技能。AI作为主导审计者，通过LLM深度代码分析挖掘安全漏洞，ast-grep仅作为辅助筛选工具用于快速定位可疑代码模式。
  适用于跨语言、跨项目的源码安全审计，输出中文报告供人工复核与落地修复。
  兼容 Java、Go、Python、PHP、C#、JavaScript/TypeScript 等语言，覆盖 9 类漏洞类型。
  AI基于源代码深度分析生成带日期的最终审计报告。
metadata:
  version: "0.0.1"
  languages: "Java, Go, Python, PHP, C#, JavaScript, TypeScript"
  scan_modes: "静态分析, AST分析, LLM深度代码审查"
  vulnerabilities: "SQL注入, XSS, 命令执行, 反序列化, 路径穿越, SSRF, XXE, 鉴权缺陷, 硬编码密钥"
---

# 源码安全审计

安全审计顾问与执行器。通过对代码、依赖与配置的综合分析，识别漏洞、验证证据与评估风险。

**核心原则：LLM是审计的主导者，ast-grep只是辅助工具。**

- ast-grep只能匹配已知模式，无法发现复杂业务逻辑漏洞、逻辑绕过、上下文相关的安全问题
- LLM必须主动阅读代码、追踪数据流、分析调用链、验证漏洞真实性和可达性
- 所有ast-grep命中结果都必须经过LLM的上下文审查，不得直接作为漏洞结论

## 审计流程

1. **目标识别**：确定分析对象、范围与关键文件
2. **ast-grep辅助扫描**：使用 `ast-grep scan --json` 扫描目标代码，快速定位可疑模式
3. **LLM主动代码审查**：AI主动阅读源代码，基于安全知识挖掘漏洞，不依赖ast-grep结果
4. **漏洞验证**：对可疑代码进行数据流分析、调用链追踪、上下文验证，确认漏洞真实性和可达性
5. **误报自动确认**：对疑似误报进行深度复核，自动分析代码上下文和数据流
6. **生成AI审计报告**：输出 `security_audit_report_YYYYMMDD.md`，包含6个必需字段。报告需先列出**确认的真实漏洞**，再单独列出**疑似误报项**，两者不得混排。如果目标项目是git仓库，报告中必须写明分析的git commit hash

## LLM主动安全审计方法论

### 1. 数据流分析（Taint Analysis）

追踪用户输入从入口点到危险函数的完整路径：

- **识别入口点**：HTTP请求参数、请求体、请求头、Cookie、文件上传、环境变量、数据库读取、外部API响应
- **追踪传播**：变量赋值、函数参数传递、返回值、对象属性复制、字符串拼接、模板渲染
- **识别汇聚点（Sink）**：SQL执行函数、命令执行函数、文件操作函数、HTTP请求函数、HTML输出、反序列化函数、XML解析函数
- **判断条件**：如果入口点数据未经充分验证/过滤/编码直接到达汇聚点，则存在漏洞

### 2. 调用链追踪

分析从漏洞入口到危险操作的完整调用链：

```
+-- 漏洞入口
|   handler(req, res)
|   (routes/user.js:15)
|
+-- 中间调用
|   [1] validateInput(input)
|       (utils/validator.js:8)
|   [2] processUser(data)
|       (services/user.js:42)
|
+-- 危险操作
    execQuery(sql)
    (db/connection.js:67)
```

- 逐层阅读相关函数实现
- 确认数据在传递过程中是否被净化
- 确认调用链是否可达（是否存在提前返回、条件分支阻止到达sink）

### 3. 上下文验证

对ast-grep命中或可疑代码进行深度上下文分析：

- **上游验证**：数据来源是什么？是否来自用户可控输入？
- **中游验证**：传递过程中是否有验证、过滤、转义、参数化查询、白名单校验？
- **下游验证**：危险函数的执行环境、权限、是否有多层防护？
- **业务逻辑验证**：是否存在逻辑绕过、条件竞争、权限检查缺失、默认配置风险？

### 4. 漏洞挖掘策略

LLM应主动采用以下策略挖掘项目中的安全漏洞：

| 策略 | 说明 |
|------|------|
| **入口点枚举** | 识别所有接收外部输入的接口、函数、配置项 |
| **危险函数清单** | 识别项目中使用的所有危险API和第三方库函数 |
| **模式扩展** | ast-grep规则无法覆盖的变体写法、框架特定API、业务逻辑漏洞 |
| **跨文件追踪** | 追踪变量和函数在多个文件间的传递，不局限于单文件分析 |
| **配置审查** | 检查安全相关配置（CORS、认证中间件、路由权限、依赖版本） |
| **依赖分析** | 检查package.json、requirements.txt等是否存在已知漏洞依赖 |

## ast-grep 扫描规范

**重要：ast-grep仅作为辅助工具，不能替代LLM的主动分析。**

ast-grep的局限性：
- 只能匹配语法模式，无法理解业务逻辑
- 容易产生误报（如硬编码测试密钥、内部使用的安全代码）
- 容易漏报（如框架特定API、间接调用、复杂条件绕过）
- 无法进行跨文件的数据流和调用链分析

### 项目配置

创建 `sgconfig.yml` 配置文件（相对于审计项目根目录）：
```yaml
ruleDirs:
  - references/rules
```

或使用绝对路径（当规则已安装到 OpenCode 技能目录时）：
```yaml
ruleDirs:
  - ~/.config/opencode/skills/security-audit/references/rules
```

### 扫描命令

```bash
# 使用项目配置扫描
cd /path/to/project && ast-grep scan --json > /tmp/scan_results.json

# 或指定配置文件路径
ast-grep scan -c /path/to/sgconfig.yml /path/to/project --json

# 使用单个规则文件
ast-grep scan -r references/rules/sql-injection-csharp.yml /path/to/project --json
```

### 规则文件

规则位于 `references/rules/` 目录：
- `sql-injection-{lang}.yml` - SQL注入
- `command-exec-{lang}.yml` - 命令执行
- `xss-{lang}.yml` - XSS
- `path-traversal-{lang}.yml` - 路径穿越
- `ssrf-{lang}.yml` - SSRF
- `xxe-{lang}.yml` - XXE
- `deserialization-{lang}.yml` - 反序列化
- `auth-defects-{lang}.yml` - 鉴权缺陷
- `hardcoded-secrets-{lang}.yml` - 硬编码密钥

支持语言：python, java, go, php, csharp, javascript, typescript

## 输出要求

- **输出语言**：中文
- **报告文件**：`security_audit_report_YYYYMMDD.md`
- **Git信息**：如果目标项目是git仓库，报告头部必须包含 `Git Commit Hash: <hash>`
- **报告结构**：
  1. **确认的真实漏洞**：按风险等级排序，逐项列出经AI验证的漏洞
  2. **疑似误报项**：单独成章，列出经复核后认为可能为误报的项，不得与真实漏洞混排
- **报告字段（每处真实漏洞/疑似误报均须包含）**：
  1. **复现步骤**：包含HTTP请求包
  2. **漏洞入口**：漏洞的入口点和攻击向量
  3. **调用链**：从入口到危险操作的完整调用链
  4. **风险等级**：严重/高危/中危/低危
  5. **修复建议**：具体的修复代码示例
  6. **疑似误报说明**：误报可能性分析和判断依据

## HTTP请求包规范

```http
POST /api/users HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 45

username=admin' OR '1'='1'--&password=test
```

## 误报判定

- **确认为误报**：数据验证/过滤逻辑、参数化查询、输出编码、调用链不可达、硬编码仅用于测试环境
- **保留为漏洞**：用户输入未经验证直接传递到危险函数、调用链完整且可达、硬编码出现在生产代码或配置中
- **保持可疑**：上下文复杂无法确定、存在模糊的防护逻辑

## 能力边界

- **ast-grep扫描**：仅作为辅助工具，用于快速定位可疑代码模式
- **LLM主动分析**：AI必须主动阅读代码、追踪数据流、分析调用链、验证漏洞
- **AI生成最终报告**：AI基于源代码深度分析+规则库参考生成报告
- **自动化原则**：疑似误报的深度复核自动完成，不得要求人工介入确认

## 使用示例

```bash
# 创建项目配置并扫描（使用相对路径，假设规则在当前项目中）
cat > /path/to/project/sgconfig.yml << 'EOF'
ruleDirs:
  - references/rules
EOF
cd /path/to/project && ast-grep scan --json > /tmp/scan_results.json

# 辅助验证
rg -n "execute|query|raw" --type cs /path/to/project

# 获取git commit hash（如果是git仓库）
cd /path/to/project && git rev-parse HEAD
```

**报告输出**：AI最终审计报告保存为 `security_audit_report_YYYYMMDD.md`，ast-grep扫描结果输出到 `/tmp/scan_results.json`。如果目标项目是git仓库，报告头部必须包含 `Git Commit Hash: <hash>`。
