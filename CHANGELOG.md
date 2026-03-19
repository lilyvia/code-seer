# 版本历史 (Changelog)

本文件记录安全审计技能的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.0.0] - 2024-03-18

### 新增功能

#### 核心功能
- **安全扫描引擎**: 基于 AST-grep 的静态代码分析引擎
- **多语言支持**: 支持 Java、Go、Python、PHP、C# 五种编程语言
- **9类漏洞检测**: 完整覆盖 OWASP Top 10 核心漏洞类型
- **调用链追踪**: 支持从漏洞入口到危险操作的完整调用链路分析
- **误报过滤系统**: 基于白名单、上下文分析和污点追踪的误报过滤
- **风险计算器**: 多因素风险评分算法

#### 漏洞检测规则 (41条规则)
- **SQL注入**: 5种语言各3-5个检测模式
- **XSS跨站脚本**: JavaScript/TypeScript 和 PHP 检测规则
- **命令执行**: 5种语言的 eval/exec 检测
- **反序列化漏洞**: Python、Java、PHP、C# 检测规则
- **路径穿越**: 任意文件读取/上传/删除检测
- **SSRF**: 服务器端请求伪造检测
- **XXE**: XML外部实体注入检测
- **鉴权缺陷**: 未授权访问、水平/垂直越权检测
- **硬编码密钥**: API密钥、密码、私钥检测

#### 报告系统
- **Markdown 报告**: 中文格式，包含6个必需字段
  - 复现步骤
  - 漏洞入口
  - 调用链追踪
  - 风险等级
  - 修复建议
  - 疑似误报说明
- **JSON 报告**: 结构化数据输出
- **SARIF 报告**: 符合 SARIF v2.1.0 标准，支持 GitHub Code Scanning

#### 中文支持
- 所有报告输出使用中文
- 中文漏洞描述和修复建议
- 中文错误提示和日志
- 中文文档（README、SKILL.md、CHANGELOG）

### 技术特性

#### 污点分析引擎 (`taint_tracker.py`)
- 定义 Source（用户输入入口点）
- 定义 Sink（危险操作）
- 定义 Sanitizer（安全函数）
- 变量赋值追踪
- 函数参数追踪

#### 调用图构建器 (`call_graph.py`)
- 函数定义提取
- 函数调用提取
- 双向调用图构建
- 跨文件分析支持

#### 误报过滤器 (`fp_filter.py`)
- **白名单过滤器**: 安全包装器、测试文件过滤
- **数据流过滤器**: 检测参数化查询和安全模式
- **上下文过滤器**: 分析验证检查代码

#### AST-grep 集成 (`ast_grep_wrapper.py`)
- YAML 规则执行
- JSON 输出解析
- 错误处理

### 文档

#### 新增文档
- `README.md`: 完整的安装和使用指南（中文）
- `SKILL.md`: OpenCode 技能定义文件（中文）
- `CHANGELOG.md`: 版本历史记录（本文件）
- `references/cwe-mappings.md`: CWE 漏洞映射和中文描述
- `references/remediation-guide.md`: 修复指南和代码示例

#### 规则文档
- 41条 YAML 规则文件，全部包含中文描述
- 每个规则包含：id、name、severity、cwe、description、remediation

### 测试

#### 测试样本
- 9类漏洞的测试代码样本
- 覆盖5种编程语言
- 用于验证检测规则有效性

### 项目结构

```
security-audit/
├── SKILL.md                    # 技能定义
├── README.md                   # 项目文档
├── CHANGELOG.md                # 版本历史
├── scripts/                    # 核心脚本 (10个 Python 文件)
├── references/                 # 参考文档
│   ├── rules/                  # 41条 AST-grep 规则
│   ├── cwe-mappings.md         # CWE 映射
│   └── remediation-guide.md    # 修复指南
└── test-samples/               # 测试样本
```

### 依赖

#### 必需依赖
- Python 3.8+
- Node.js 16+
- AST-grep CLI (`@ast-grep/cli`)

#### Python 包
- 无外部依赖（仅使用标准库）

### 性能指标

- **检测覆盖率**: 9类漏洞 × 5种语言 = 45种检测场景
- **误报率目标**: < 10%
- **检测率目标**: > 80%（基于 Hello-Java-Sec 测试）

### 已知限制

- 仅支持静态分析，不支持运行时分析
- 内置规则不支持自定义配置
- 仅支持批量代码审计，不支持实时检测
- 扫描速度在大规模代码库可能需要优化

### 后续计划

#### 版本 1.1.0 (计划中)
- [ ] 添加更多框架特定的检测规则（Spring、Django、Flask 等）
- [ ] 优化大规模代码库的扫描性能
- [ ] 添加更多语言的支持（Ruby、Rust）

#### 版本 2.0.0 (规划中)
- [ ] 增量扫描支持
- [ ] 性能优化

---

## 版本对比

| 版本 | 发布日期 | 漏洞类型 | 支持语言 | 规则数量 |
|-----|---------|---------|---------|---------|
| 1.0.0 | 2024-03-18 | 9类 | 5种 | 41 |

---

## 贡献者

感谢以下贡献者参与本项目的开发：

- OpenCode 安全审计团队

## 参考资源

- [AST-grep 文档](https://ast-grep.github.io/)
- [CWE 官方网站](https://cwe.mitre.org/)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [SARIF 规范](https://sarifweb.azurewebsites.net/)

---

[1.0.0]: https://github.com/opencode/security-audit/releases/tag/v1.0.0
