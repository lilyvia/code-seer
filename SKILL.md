---
name: security-audit
description: |
  源码安全审计技能，基于规则库进行综合分析，必要时按需调用辅助工具（如 python3、ast-grep、grep 等）进行佐证与批量分析，确保结论来自多源证据的综合判断。
  适用于跨语言、跨项目的源码安全审计，输出中文报告供人工复核与落地修复。
  兼容 Java、Go、Python、PHP、C# 等语言，覆盖 9 类漏洞类型。
  AI执行Python脚本获取辅助分析结果，经AI综合分析后生成带日期的最终审计报告，文件名格式为 `security_audit_report_YYYYMMDD.md`，无需人工介入。
license: MIT
compatibility: opencode
metadata:
  version: "1.0.1"
  languages: "Java, Go, Python, PHP, C#"
  scan_modes: "静态分析, AST分析"
  vulnerabilities: "SQL注入, XSS, 命令执行, 反序列化, 路径穿越, SSRF, XXE, 鉴权缺陷, 硬编码密钥"
---

# 源码安全审计

安全审计顾问与执行器。通过对代码、依赖与配置的综合分析，结合规则库进行漏洞定位、证据对比与风险评估。必要时可按需调用辅助工具（如 python3、ast-grep、grep 等）进行佐证分析。

## 什么时候使用
- 需要对代码库进行全面的安全审计、风险排序与复现性分析时使用。
- 需要生成结构化、中文化的审计报告，以便人工复核与修复落地。
- 需要跨语言、跨框架的规则对照与证据链构建时使用。

## 如何工作
- 读取代码、依赖、配置与上下文信息，基于内置规则库进行初步分析。
- 运用推理对潜在风险进行综合评估，形成候选风险点与证据链。
- **执行Python扫描脚本**：调用 `python3 scripts/security_scanner.py <目标路径>` 执行自动化安全扫描，**获取辅助分析结果**（包括候选漏洞、调用链、置信度等）。
- **AI综合分析**：AI结合Python脚本的辅助分析结果、源代码审查、规则库匹配进行深度分析，而非直接复制Python报告。
- **生成AI审计报告**：AI基于多源证据生成带日期的最终审计报告（`security_audit_report_YYYYMMDD.md`），包含完整的复现步骤、漏洞入口、调用链、风险等级、修复建议和误报分析。
- 如需额外证据与复现路径，按需调用辅助工具（如 python3、ast-grep、grep）进行佐证分析。
- 提供可追踪的调用链信息，便于审计透明化与复核。

## 审计流程
1. **目标识别**：确定分析对象、范围与关键文件。
2. **执行Python扫描**：调用 `python3 scripts/security_scanner.py <目标路径> --format json` 执行自动化扫描，**获取辅助分析数据**（候选漏洞列表、调用链、置信度等）。
3. **AI深度分析**：AI基于Python辅助数据，结合源代码审查、规则库、污点追踪进行综合分析：
   - 验证Python发现的候选漏洞
   - 补充代码上下文分析
   - 识别Python遗漏的漏洞
   - 评估漏洞真实性和风险等级
4. **规则对照**：基于 9 类漏洞、5 种语言的规则集进行交叉验证。
5. **佐证与复现**：按需执行 python3、ast-grep、grep 等工具获取多源证据。
6. **误报自动确认**：对疑似误报进行深度复核，自动分析代码上下文、数据流和防护措施，无需人工介入。
7. **生成AI审计报告**：AI生成带日期的最终审计报告（`security_audit_report_YYYYMMDD.md`），包含 6 个必需字段，并标注可信度与可疑性等级。

## Python 脚本执行规范

### 主扫描命令
```bash
# 基础扫描（生成 Markdown 报告）
python3 scripts/security_scanner.py <目标路径> --format markdown

# 综合扫描模式（更全面但较慢）
python3 scripts/security_scanner.py <目标路径> --mode comprehensive --format markdown

# 生成 JSON 报告（用于程序处理）
python3 scripts/security_scanner.py <目标路径> --format json

# 生成 SARIF 报告（用于 CI/CD 集成）
python3 scripts/security_scanner.py <目标路径> --format sarif
```

### 报告生成脚本
```bash
# 生成示例报告
python3 scripts/report_generator.py

# 查看其他脚本用法
python3 scripts/ast_grep_wrapper.py --help
python3 scripts/call_chain_tracer.py --help
python3 scripts/taint_tracker.py --help
```

### 脚本位置
所有脚本位于 `scripts/` 目录：
- `security_scanner.py` - 主扫描器，必须优先调用
- `report_generator.py` - 报告生成器
- `ast_grep_wrapper.py` - AST-grep 包装器
- `call_chain_tracer.py` - 调用链追踪器
- `taint_tracker.py` - 污点追踪引擎
- `fp_filter.py` - 误报过滤器
- `risk_calculator.py` - 风险计算器

## 输出要求
- **输出语言**：中文。
- **报告性质**：**AI审计报告**（非Python脚本原始输出），是AI基于Python辅助分析、代码审查、规则库综合判断后的最终报告。
- **报告文件**：AI审核完成后生成带日期的 Markdown 格式报告文件，文件名格式为 `security_audit_report_YYYYMMDD.md`（例如：`security_audit_report_20240319.md`）。
- **报告字段**：需包含以下 6 项
  1) **复现步骤**：详细的漏洞复现步骤，包含 HTTP 请求包（见下文 HTTP 请求包规范）
  2) **漏洞入口**：漏洞的入口点和攻击向量
  3) **调用链**：从入口到危险操作的完整调用链
  4) **风险等级**：严重/高危/中危/低危
  5) **修复建议**：具体的修复代码示例
  6) **疑似误报说明**：误报可能性分析和判断依据
- **风险等级分级**：采用多维证据综合评估（Python辅助数据 + AI代码分析 + 规则库验证），证据不足时降级为可疑点，避免盲目高报。

## HTTP 请求包规范（复现步骤必需）

复现步骤中必须包含详细的 HTTP 请求包，格式如下：

### 请求包格式示例
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
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml
Content-Length: 45
Connection: close

username=admin' OR '1'='1'--&password=test
```

**预期响应**:
- 状态码: 200 OK
- 响应体包含所有用户信息（证明SQL注入成功）
```

### HTTP 请求包要求
1. **必须包含**：请求方法、完整 URL、所有请求头、请求体
2. **Raw 格式**：提供完整的 HTTP 原始请求包，可直接用 Burp Suite、curl 或 Python requests 复现
3. **漏洞参数**：明确标注哪个参数存在漏洞
4. **Payload 说明**：解释 payload 的构造原理
5. **预期响应**：描述成功利用后的响应特征

## 误报自动确认机制（无人工介入）

### 疑似误报识别标准
当满足以下任一条件时，标记为"疑似误报"并触发深度复核：
1. 置信度低于 0.7
2. 代码中存在潜在的安全防护函数调用
3. 调用链中存在数据验证/过滤节点
4. 漏洞模式匹配但上下文不完整

### 深度复核流程（自动执行）
```
1. 初步检测发现疑似漏洞
   ↓
2. 触发深度复核机制
   ↓
3. 数据流分析（自动）
   - 使用污点追踪分析数据流向
   - 检查是否存在净化操作
   - 验证用户输入是否真正到达危险函数
   ↓
4. 上下文验证（自动）
   - 检查前后 10 行代码的防护逻辑
   - 搜索 sanitization/validation/escape 等防护函数
   - 分析条件分支和异常处理
   ↓
5. 调用链完整性检查（自动）
   - 构建完整调用图
   - 验证入口到出口的可达性
   - 检查中间层是否有拦截
   ↓
6. 综合判定（自动）
   ✓ 确认为真实漏洞 → 更新置信度，保留并上报
   ✗ 确认为误报 → 记录原因，降级为信息项
   ? 无法确定 → 降低置信度，保留可疑标记
```

### 自动复核工具调用
```bash
# 污点追踪分析
python3 scripts/taint_tracker.py --target <文件> --entry <入口函数>

# 调用链追踪
python3 scripts/call_chain_tracer.py --target <文件> --start <起始行>

# 误报过滤分析
python3 scripts/fp_filter.py --findings <发现结果文件>
```

### 误报判定标准
- **确认为误报**：
  - 明确的数据验证/过滤逻辑
  - 使用参数化查询或预编译语句
  - 输出编码/转义处理
  - 调用链不可达（有条件提前返回）

- **保留为漏洞**：
  - 用户输入未经验证直接传递到危险函数
  - 调用链完整且可达
  - 无有效的防护措施

- **保持可疑**：
  - 上下文复杂无法确定
  - 存在模糊的防护逻辑
  - 需要运行时验证

## 数据处理规则
- 本地分析为主，确保所有分析在本地完成，不对外发送代码或数据。
- 规则库仅作匹配与比对参考，结论基于综合分析与证据链。

## 能力边界与灵活性
- **Python脚本作为辅助**：审核开始时，调用 `python3 scripts/security_scanner.py <目标路径> --format json` 获取辅助分析数据（候选漏洞、调用链、置信度），**但Python报告不直接作为最终输出**。
- **AI生成最终报告**：AI基于Python辅助数据 + 源代码深度分析 + 规则库验证，生成独立的AI审计报告，包含完整的6个字段和HTTP请求包。
- 可以阅读代码、结合规则库、按需执行 python3、ast-grep、grep 来获取佐证证据，但结论应来自综合分析结果，而非单次脚本输出。
- 不强制依赖目录结构或特定脚本入口，适应不同实现与工作流。
- 保留 9 类漏洞、5 种语言、6 个报告字段、中文输出要求，以及低误报优先策略。
- **自动化原则**：疑似误报的深度复核必须自动完成，不得要求人工介入确认。

## 使用示例

### 完整审计流程
```bash
# 1. 执行Python安全扫描（获取辅助分析数据）
python3 scripts/security_scanner.py /path/to/project --mode comprehensive --format json

# 2. AI基于Python辅助数据 + 源代码深度分析，生成最终审计报告
#    报告文件名：security_audit_report_YYYYMMDD.md（例如：security_audit_report_20240319.md）

# 3. 如需对特定文件深度分析（辅助）
python3 scripts/taint_tracker.py --target /path/to/project/app.py --entry process_user_input

# 4. 验证疑似误报（辅助）
python3 scripts/fp_filter.py --findings findings.json --deep-analysis
```

### 报告说明
- **Python辅助报告**：JSON格式，包含候选漏洞、调用链、置信度等原始分析数据，供AI参考
- **AI最终审计报告**：Markdown格式（`security_audit_report_YYYYMMDD.md`），包含完整的6个字段和HTTP请求包
- **关系**：AI审计报告 ≠ Python报告，AI基于Python数据进行综合判断、去重、补漏、验证后生成独立报告

### 报告输出位置
- **AI最终审计报告**：`security_audit_report_YYYYMMDD.md`（例如：`security_audit_report_20240319.md`），保存于当前工作目录
  - 日期格式：YYYYMMDD（4位年份 + 2位月份 + 2位日期）
  - 格式：Markdown，包含完整的6个字段和HTTP请求包
- **Python辅助报告**：可通过 `--format json` 输出到stdout或重定向到文件（供AI参考，不直接对外交付）
  ```bash
  python3 scripts/security_scanner.py /path/to/project --format json > /tmp/python_aux_report.json
  ```
