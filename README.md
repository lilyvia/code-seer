# 安全审计技能

OpenCode 安全审计技能，用于检测代码中的9类安全漏洞，支持5种编程语言。

## 项目介绍

本安全审计技能基于 AST-grep 静态分析引擎，提供深度安全漏洞检测能力。支持完整的调用链追踪、误报过滤和中文报告生成。

### 支持的漏洞类型 (9类)

| 漏洞类型 | CWE ID | 风险等级 | 说明 |
|---------|--------|---------|------|
| SQL注入 | CWE-89 | 严重 | 用户输入直接拼接到SQL查询中 |
| XSS跨站脚本 | CWE-79 | 高危 | 未过滤的用户输入输出到页面 |
| 命令执行 | CWE-78 | 严重 | 执行用户控制的系统命令 |
| 反序列化漏洞 | CWE-502 | 严重 | 不安全的反序列化操作 |
| 路径穿越 | CWE-22 | 高危 | 任意文件读取/上传/删除 |
| SSRF | CWE-918 | 高危 | 服务器端请求伪造 |
| XXE | CWE-611 | 中危 | XML外部实体注入 |
| 鉴权缺陷 | CWE-287/306 | 中危 | 未授权访问、水平/垂直越权 |
| 硬编码密钥 | CWE-798 | 高危 | API密钥、密码等敏感信息硬编码 |

### 支持的语言 (5种)

- **Java** - 完整的Java安全规则集
- **Go** - Go语言特定API检测
- **Python** - Python框架和库支持
- **PHP** - PHP常见漏洞模式
- **C#** - .NET平台安全检测

## 安装说明

### 系统要求

- Python 3.8+
- Node.js 16+ (用于 AST-grep)

### 安装步骤

#### 1. 克隆项目

```bash
cd /path/to/opencode
git clone <repository-url>
cd security-audit
```

#### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 3. 安装 AST-grep CLI

```bash
npm install -g @ast-grep/cli
```

或者使用 npx:

```bash
npx @ast-grep/cli --version
```

#### 4. 验证安装

```bash
python scripts/security_scanner.py --help
```

输出示例:
```
usage: security_scanner.py [-h] [--mode {quick,comprehensive}]
                          [--format {markdown,json,sarif}]
                          [--fail-on {严重,高危,中危,低危}]
                          target

安全审计扫描器 - 检测代码中的安全漏洞

positional arguments:
  target                要扫描的代码目录路径

options:
  -h, --help            显示帮助信息
  --mode {quick,comprehensive}
                        扫描模式
  --format {markdown,json,sarif}
                        输出格式
  --fail-on {严重,高危,中危,低危}
                        发现指定等级及以上漏洞时返回错误码
```

## 快速开始

### 基础扫描

```bash
# 扫描当前目录
python scripts/security_scanner.py .

# 扫描指定项目
python scripts/security_scanner.py /path/to/your/project

# 使用综合扫描模式（更慢但更全面）
python scripts/security_scanner.py /path/to/project --mode comprehensive
```

### 生成报告

```bash
# 生成 Markdown 报告（默认）
python scripts/security_scanner.py /path/to/project --format markdown

# 生成 JSON 报告
python scripts/security_scanner.py /path/to/project --format json

# 生成 SARIF 报告（用于 CI/CD 集成）
python scripts/security_scanner.py /path/to/project --format sarif
```

### 快速演示

```bash
# 使用示例报告生成器
cd security-audit
python scripts/report_generator.py
```

这将生成一个示例安全报告，展示报告的完整格式。

## 使用方法

### 命令行参数

```
python scripts/security_scanner.py <目标路径> [选项]
```

| 参数 | 说明 | 可选值 | 默认值 |
|-----|------|--------|--------|
| `target` | 要扫描的代码目录或文件 | - | 必需 |
| `--mode` | 扫描模式 | quick, comprehensive | quick |
| `--format` | 输出格式 | markdown, json, sarif | markdown |
| `--fail-on` | 指定等级以上漏洞返回错误码 | 严重, 高危, 中危, 低危 | - |

### 扫描模式

**快速模式 (quick)**
- 仅扫描核心漏洞模式
- 扫描速度较快
- 适合日常开发和 CI 快速检查

**综合模式 (comprehensive)**
- 启用所有漏洞规则
- 启用调用链追踪
- 启用误报过滤分析
- 适合发布前的安全审计

### 输出格式

**Markdown 格式** (推荐用于人工审查)
- 中文安全报告
- 包含漏洞描述、代码片段、修复建议
- 调用链可视化 (ASCII 艺术图)
- 疑似误报说明

**JSON 格式** (推荐用于程序处理)
- 结构化数据输出
- 易于集成到其他工具
- 包含完整的漏洞元数据

**SARIF 格式** (推荐用于 CI/CD)
- 符合 SARIF v2.1.0 标准
- GitHub Code Scanning 兼容
- 支持代码流追踪

### 示例输出

```markdown
# 安全审计报告

**生成时间**: 2024-03-18 10:30:00

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

### 1. SQL注入漏洞 🔴 严重

#### 📋 基本信息
- **规则ID**: `sql-injection-python`
- **CWE编号**: CWE-89
- **文件位置**: `app/database.py:42`
- **置信度**: 95%

#### 📝 漏洞描述
用户输入直接拼接到SQL查询中，存在SQL注入风险...

#### 🔍 复现步骤
1. 访问用户详情页面
2. 在URL参数中输入 `?id=1 OR 1=1`
3. 观察是否返回所有用户数据

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
1. 使用参数化查询
2. 对用户输入进行类型校验
3. 使用ORM框架
```

## 配置选项

### 环境变量

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| `SECURITY_AUDIT_MODE` | 默认扫描模式 | `quick` |
| `SECURITY_AUDIT_OUTPUT` | 默认输出格式 | `markdown` |
| `SECURITY_AUDIT_RULES_PATH` | 自定义规则路径 | `references/rules/` |

### 规则配置

规则文件位于 `references/rules/` 目录，使用 YAML 格式:

```yaml
id: sql-injection-python
severity: CRITICAL
cwe: CWE-89
message: 发现SQL注入漏洞
description: |
  用户输入直接拼接到SQL查询中，可能导致数据库被攻击。
remediation: |
  使用参数化查询替代字符串拼接：
  ```python
  cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
  ```
```

### 忽略文件

扫描器会自动跳过以下文件:

- `.git/` 目录
- `node_modules/` 目录
- `__pycache__/` 目录
- 包含 `test` 的文件名
- `.gitignore` 中指定的文件

## 示例输出

### 控制台输出

```
发现 156 个待扫描文件
扫描完成。发现 4 个漏洞。

=== 漏洞统计 ===
🔴 严重: 1 个
🟠 高危: 1 个
🟡 中危: 1 个
🟢 低危: 1 个

✅ 报告已保存到: /path/to/security_audit_report.md
```

### JSON 输出示例

```json
{
  "target": "/path/to/project",
  "files_scanned": 156,
  "findings": [
    {
      "rule_id": "sql-injection-python",
      "name": "SQL注入漏洞",
      "severity": "严重",
      "cwe": "CWE-89",
      "file_path": "app/database.py",
      "line_number": 42,
      "confidence": 0.95,
      "description": "用户输入直接拼接到SQL查询中..."
    }
  ]
}
```

## 故障排除

### 常见问题

#### 1. AST-grep 未安装

**错误信息**:
```
ast-grep: command not found
```

**解决方法**:
```bash
npm install -g @ast-grep/cli
```

#### 2. Python 版本过低

**错误信息**:
```
SyntaxError: invalid syntax
```

**解决方法**:
确保 Python 版本 >= 3.8:
```bash
python --version
# 升级 Python 到 3.8+
```

#### 3. 权限不足

**错误信息**:
```
PermissionError: [Errno 13] Permission denied
```

**解决方法**:
```bash
# 检查目录权限
ls -la /path/to/project

# 使用 sudo（不推荐）
sudo python scripts/security_scanner.py /path/to/project

# 或者修改目录权限
chmod -R 755 /path/to/project
```

#### 4. 扫描结果为空

**可能原因**:
- 目标目录不包含支持的文件类型
- 所有文件都被 .gitignore 排除
- 代码中没有检测到漏洞

**解决方法**:
```bash
# 检查文件类型
find /path/to/project -name "*.py" -o -name "*.java" -o -name "*.go"

# 使用 --no-ignore 选项（开发测试用）
# 修改 discover_files 函数跳过过滤
```

#### 5. 报告中文乱码

**解决方法**:
```bash
# 设置 UTF-8 编码
export PYTHONIOENCODING=utf-8

# 或者使用 Python 3 运行
python3 scripts/security_scanner.py /path/to/project
```

### 调试模式

```bash
# 启用详细日志
python -v scripts/security_scanner.py /path/to/project

# 测试单个规则
ast-grep scan --rule references/rules/sql-injection-python.yml /path/to/test.py
```

### 获取帮助

- 查看 SKILL.md 了解详细使用说明
- 查看 references/cwe-mappings.md 了解漏洞分类
- 查看 references/remediation-guide.md 了解修复建议

## 项目结构

```
security-audit/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 本文件
├── CHANGELOG.md                # 版本历史
├── scripts/                    # Python 脚本
│   ├── security_scanner.py     # 主扫描器
│   ├── ast_grep_wrapper.py     # AST-grep 包装器
│   ├── taint_tracker.py        # 污点追踪引擎
│   ├── call_graph.py           # 调用图构建器
│   ├── call_chain_tracer.py    # 调用链追踪器
│   ├── fp_filter.py            # 误报过滤器
│   ├── risk_calculator.py      # 风险计算器
│   ├── report_generator.py     # 报告生成器
│   └── sarif_formatter.py      # SARIF 格式化器
├── references/                 # 参考文档和规则
│   ├── rules/                  # AST-grep 规则文件
│   │   ├── sql-injection-*.yml
│   │   ├── xss-*.yml
│   │   ├── command-exec-*.yml
│   │   └── ...
│   ├── cwe-mappings.md         # CWE 漏洞映射
│   └── remediation-guide.md    # 修复指南
└── test-samples/               # 测试样本
    ├── sqli_python.py
    ├── xss_php.php
    └── ...
```

## 许可证

MIT许可证

## 贡献指南

1. 复刻本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建拉取请求

## 相关链接

- [AST-grep 文档](https://ast-grep.github.io/)
- [CWE 官方网站](https://cwe.mitre.org/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [SARIF 规范](https://sarifweb.azurewebsites.net/)
