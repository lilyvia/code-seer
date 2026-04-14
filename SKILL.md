---
name: security-audit
description: |
  源码安全审计技能，基于ast-grep规则库进行综合分析，直接调用ast-grep CLI进行批量扫描，结合AI代码审查进行漏洞定位与风险评估。
  适用于跨语言、跨项目的源码安全审计，输出中文报告供人工复核与落地修复。
  兼容 Java、Go、Python、PHP、C#、JavaScript/TypeScript 等语言，覆盖 9 类漏洞类型。
  AI基于ast-grep扫描结果与源代码深度分析生成带日期的最终审计报告。
metadata:
  version: "0.0.1"
  languages: "Java, Go, Python, PHP, C#, JavaScript, TypeScript"
  scan_modes: "静态分析, AST分析"
  vulnerabilities: "SQL注入, XSS, 命令执行, 反序列化, 路径穿越, SSRF, XXE, 鉴权缺陷, 硬编码密钥"
---

# 源码安全审计

安全审计顾问与执行器。通过对代码、依赖与配置的综合分析，结合ast-grep规则库进行漏洞定位、证据对比与风险评估。

## 审计流程

1. **目标识别**：确定分析对象、范围与关键文件
2. **执行ast-grep扫描**：使用 `ast-grep scan --json` 扫描目标代码
3. **AI深度分析**：基于扫描结果验证候选漏洞，评估漏洞真实性和风险等级
4. **误报自动确认**：对疑似误报进行深度复核，自动分析代码上下文和数据流
5. **生成AI审计报告**：输出 `security_audit_report_YYYYMMDD.md`，包含6个必需字段

## ast-grep 扫描规范

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

### 控制扫描输出大小

大型代码库的完整扫描可能产生数十MB输出，应控制大小便于AI处理：

**策略1: 分层扫描（推荐）**
```bash
# 第一层：仅扫描高危规则（输出约50-200KB）
ast-grep scan -r references/rules/command-exec-csharp.yml \
  -r references/rules/sql-injection-csharp.yml \
  -r references/rules/deserialization-csharp.yml \
  -r references/rules/xxe-csharp.yml /path/to/project --json

# 第二层：添加中危规则（输出约200-500KB）
ast-grep scan -r references/rules/ssrf-csharp.yml \
  -r references/rules/path-traversal-csharp.yml /path/to/project --json
```

**策略2: 限制单规则匹配数（最快）**
```bash
# 每个规则最多返回20个匹配，避免单规则产生过大输出
for rule in references/rules/*csharp.yml; do
  ast-grep scan -r "$rule" /path/to/project --json | head -1000 >> /tmp/scan_results.json
done
```

**策略3: 按文件分批扫描**
```bash
# 先扫描关键文件（如Controller、Service层）
find /path/to/project -name "*Controller*.cs" -o -name "*Service*.cs" | \
  xargs -I {} ast-grep scan -c sgconfig.yml {} --json
```

**输出大小参考**
| 扫描范围 | 预估大小 | 扫描时间 | 适用场景 |
|---------|---------|---------|----------|
| 仅高危规则（4个） | 50-200KB | 10-30秒 | 快速安全评估 |
| 高危+中危（7个） | 200-500KB | 30-60秒 | 标准审计 |
| 单规则限制20个 | 100-300KB | 5-15秒 | AI快速分析 |
| 完整扫描 | 10MB-50MB+ | 数分钟 | 仅必要时使用 |

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
- **报告字段**：
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

- **确认为误报**：数据验证/过滤逻辑、参数化查询、输出编码、调用链不可达
- **保留为漏洞**：用户输入未经验证直接传递到危险函数、调用链完整且可达
- **保持可疑**：上下文复杂无法确定、存在模糊的防护逻辑

## 能力边界

- **ast-grep扫描**：直接使用ast-grep CLI进行批量扫描，AI解析JSON输出
- **AI生成最终报告**：AI基于扫描结果+源代码深度分析+规则库验证生成报告
- **自动化原则**：疑似误报的深度复核自动完成，不得要求人工介入确认

## 使用示例

```bash
# 创建项目配置并扫描（使用相对路径，假设规则在当前项目中）
cat > /path/to/project/sgconfig.yml << 'EOF'
ruleDirs:
  - references/rules
EOF
cd /path/to/project && ast-grep scan --json > /tmp/scan_results.json

# 分层扫描示例：先扫高危，再决定是否需要全量
ast-grep scan -r references/rules/command-exec-csharp.yml \
  -r references/rules/sql-injection-csharp.yml /path/to/project --json > /tmp/critical.json

# 如果高危扫描发现问题较少，再进行完整扫描
[ $(cat /tmp/critical.json | wc -l) -lt 1000 ] && \
  ast-grep scan -c sgconfig.yml /path/to/project --json > /tmp/full.json

# 辅助验证
rg -n "execute|query|raw" --type cs /path/to/project
```

**报告输出**：AI最终审计报告保存为 `security_audit_report_YYYYMMDD.md`，ast-grep扫描结果输出到 `/tmp/scan_results.json`
