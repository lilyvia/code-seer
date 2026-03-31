---
name: security-audit
description: |
  源码安全审计技能，基于规则库进行综合分析，必要时按需调用辅助工具（如 python3、ast-grep、grep 等）进行佐证与批量分析，确保结论来自多源证据的综合判断。
  适用于跨语言、跨项目的源码安全审计，输出中文报告供人工复核与落地修复。
  兼容 Java、Go、Python、PHP、C# 等语言，覆盖 9 类漏洞类型。
  AI执行Python脚本获取辅助分析结果，经AI综合分析后生成带日期的最终审计报告，文件名格式为 `security_audit_report_YYYYMMDD.md`，无需人工介入。
metadata:
  version: "1.0.2"
  languages: "Java, Go, Python, PHP, C#"
  scan_modes: "静态分析, AST分析"
  vulnerabilities: "SQL注入, XSS, 命令执行, 反序列化, 路径穿越, SSRF, XXE, 鉴权缺陷, 硬编码密钥"
---

# 源码安全审计

安全审计顾问与执行器。通过对代码、依赖与配置的综合分析，结合规则库进行漏洞定位、证据对比与风险评估。

## 什么时候使用
- 需要对代码库进行全面的安全审计、风险排序与复现性分析时使用。
- 需要生成结构化、中文化的审计报告，以便人工复核与修复落地。

## 如何工作
1. **执行Python扫描**：调用 `python3 scripts/security_scanner.py <目标路径> --format markdown -o /tmp/security_scan_report.md`，**必须先将扫描结果落地到 /tmp/ 目录**，然后再读取分析。
2. **AI深度分析**：AI基于Markdown扫描报告，结合源代码审查、规则库、污点追踪进行综合分析。
3. **生成AI审计报告**：AI基于多源证据生成带日期的最终审计报告（`security_audit_report_YYYYMMDD.md`）。

## 审计流程
1. **目标识别**：确定分析对象、范围与关键文件。
2. **执行Python扫描**：`python3 scripts/security_scanner.py <目标路径> --format markdown -o /tmp/security_scan_report.md`，扫描结果落地到 `/tmp/` 后读取分析。
3. **AI深度分析**：基于Markdown扫描报告验证候选漏洞，补充代码上下文分析，识别遗漏漏洞，评估漏洞真实性和风险等级。
4. **规则对照**：基于 9 类漏洞、5 种语言的规则集进行交叉验证。
5. **佐证与复现**：按需执行 python3、ast-grep (sg)、ripgrep (rg)、grep 等工具获取多源证据。
6. **误报自动确认**：对疑似误报进行深度复核，自动分析代码上下文、数据流和防护措施。
7. **生成AI审计报告**：生成带日期的最终审计报告（`security_audit_report_YYYYMMDD.md`），包含 6 个必需字段。

## Python 脚本执行规范

### Bash 超时配置
```bash
# 所有 bash 命令必须使用 10 分钟超时，使用 -o 参数将报告落地到 /tmp/
bash(command="python3 scripts/security_scanner.py /path/to/project --format markdown -o /tmp/security_scan_report.md", timeout=600000)
```

### 主扫描命令（必须落地 /tmp/ 目录）
```bash
# 综合扫描模式（落地 Markdown 报告到 /tmp/ 供AI读取分析）
python3 scripts/security_scanner.py <目标路径> --mode comprehensive --format markdown -o /tmp/security_scan_report.md

# 污点追踪分析（落地到 /tmp/）
python3 scripts/taint_tracker.py --target <文件> --entry <入口函数> -o /tmp/taint_analysis.md

# 调用链追踪（落地到 /tmp/）
python3 scripts/call_chain_tracer.py --target <文件> --start <起始行> -o /tmp/call_chain.md

# 误报过滤分析（落地到 /tmp/）
python3 scripts/fp_filter.py --findings /tmp/security_scan_report.md -o /tmp/fp_analysis.md
```

### 脚本列表
- `security_scanner.py` - 主扫描器
- `report_generator.py` - 报告生成器
- `ast_grep_wrapper.py` - AST-grep 包装器
- `call_chain_tracer.py` - 调用链追踪器
- `taint_tracker.py` - 污点追踪引擎
- `fp_filter.py` - 误报过滤器
- `risk_calculator.py` - 风险计算器

## 输出要求
- **输出语言**：中文
- **报告性质**：AI审计报告（非Python脚本原始输出）
- **报告文件**：`security_audit_report_YYYYMMDD.md`
- **报告字段**（6项）：
  1. **复现步骤**：包含 HTTP 请求包
  2. **漏洞入口**：漏洞的入口点和攻击向量
  3. **调用链**：从入口到危险操作的完整调用链
  4. **风险等级**：严重/高危/中危/低危
  5. **修复建议**：具体的修复代码示例
  6. **疑似误报说明**：误报可能性分析和判断依据

## HTTP 请求包规范

```
### 漏洞复现 HTTP 请求

**请求方法**: POST
**目标 URL**: `http://target.com/api/users`
**漏洞参数**: `username`

**完整请求包（Raw）**:
```http
POST /api/users HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 45

username=admin' OR '1'='1'--&password=test
```

**预期响应**:
- 状态码: 200 OK
- 响应体包含所有用户信息（证明SQL注入成功）
```

## 误报自动确认机制

### 疑似误报识别标准
- 置信度低于 0.7
- 代码中存在潜在的安全防护函数调用
- 调用链中存在数据验证/过滤节点

### 误报判定标准
- **确认为误报**：明确的数据验证/过滤逻辑；使用参数化查询；输出编码/转义处理；调用链不可达
- **保留为漏洞**：用户输入未经验证直接传递到危险函数；调用链完整且可达；无有效的防护措施
- **保持可疑**：上下文复杂无法确定；存在模糊的防护逻辑

## 能力边界与灵活性
- **Python扫描报告**：Markdown格式扫描报告必须落地到 `/tmp/` 目录后再读取分析，报告不直接作为最终输出
- **AI生成最终报告**：AI基于Python辅助数据 + 源代码深度分析 + 规则库验证，生成独立的AI审计报告
- **自动化原则**：疑似误报的深度复核必须自动完成，不得要求人工介入确认

## 使用示例

```bash
# 1. 执行Python安全扫描（必须落地到 /tmp/ 目录，使用 -o 参数避免进度信息混入报告）
python3 scripts/security_scanner.py /path/to/project --mode comprehensive --format markdown -o /tmp/security_scan_report.md

# 2. 从 /tmp/ 读取扫描报告，AI基于报告内容 + 源代码深度分析，生成最终审计报告

# 3. 如需对特定文件深度分析（落地到 /tmp/）
python3 scripts/taint_tracker.py --target /path/to/project/app.py --entry process_user_input -o /tmp/taint_analysis.md

# 4. 验证疑似误报（落地到 /tmp/）
python3 scripts/fp_filter.py --findings /tmp/security_scan_report.md --deep-analysis -o /tmp/fp_analysis.md
```

### 报告输出位置
- **AI最终审计报告**：`security_audit_report_YYYYMMDD.md`，保存于当前工作目录
- **Python扫描报告**：必须落地到 `/tmp/` 目录，使用 `-o` 参数输出，避免进度信息混入报告
  ```bash
  python3 scripts/security_scanner.py /path/to/project --format markdown -o /tmp/security_scan_report.md
  cat /tmp/security_scan_report.md
  ```
