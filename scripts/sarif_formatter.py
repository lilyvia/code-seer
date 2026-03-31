#!/usr/bin/env python3
"""
SARIF v2.1.0 输出格式化器
用于生成符合GitHub Code Scanning规范的SARIF报告
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


# 漏洞类型到SARIF规则的映射表
VULNERABILITY_RULES: Dict[str, Dict[str, Any]] = {
    "sql-injection-python": {
        "id": "sql-injection-python",
        "name": "SQL注入漏洞",
        "shortDescription": {
            "text": "应用程序未对用户输入进行充分过滤，导致恶意SQL语句被执行"
        },
        "fullDescription": {
            "text": "SQL注入是一种代码注入攻击，攻击者通过在输入字段中插入恶意SQL语句，从而操控数据库查询。这可能导致数据泄露、数据篡改或数据库完全失控。"
        },
        "help": {
            "text": "修复建议：\n1. 使用参数化查询或预编译语句\n2. 对用户输入进行严格的验证和过滤\n3. 使用ORM框架代替原始SQL\n4. 限制数据库账户权限\n5. 启用Web应用防火墙(WAF)"
        },
        "cwe": ["CWE-89"],
    },
    "command-exec-python": {
        "id": "command-exec-python",
        "name": "命令执行漏洞",
        "shortDescription": {
            "text": "应用程序将用户输入直接传递给系统命令执行函数"
        },
        "fullDescription": {
            "text": "命令执行漏洞允许攻击者在服务器上执行任意系统命令。当应用程序未对用户输入进行充分验证就将其传递给系统命令函数时，攻击者可以注入恶意命令，获得服务器控制权限。"
        },
        "help": {
            "text": "修复建议：\n1. 避免直接使用系统命令执行函数\n2. 使用白名单严格验证输入\n3. 使用安全的API替代shell命令\n4. 对输入进行转义处理\n5. 限制进程执行权限"
        },
        "cwe": ["CWE-78"],
    },
    "xss-python": {
        "id": "xss-python",
        "name": "跨站脚本攻击(XSS)",
        "shortDescription": {
            "text": "应用程序未对用户输入进行HTML转义直接输出到页面"
        },
        "fullDescription": {
            "text": "跨站脚本攻击(XSS)允许攻击者向Web页面注入恶意脚本。当应用程序将用户输入未经过滤地输出到HTML页面时，攻击者的脚本会在受害者浏览器中执行，可能导致会话劫持、钓鱼攻击等。"
        },
        "help": {
            "text": "修复建议：\n1. 对所有用户输入进行HTML转义\n2. 使用内容安全策略(CSP)\n3. 使用安全的模板引擎自动转义\n4. 对JavaScript上下文使用适当的编码\n5. 验证和净化用户输入"
        },
        "cwe": ["CWE-79"],
    },
    "path-traversal-python": {
        "id": "path-traversal-python",
        "name": "路径遍历漏洞",
        "shortDescription": {
            "text": "应用程序允许用户控制文件路径访问任意文件"
        },
        "fullDescription": {
            "text": "路径遍历(目录遍历)漏洞允许攻击者访问存储在Web根目录之外的文件和目录。通过构造包含'..'序列的文件路径，攻击者可以读取或写入服务器上的任意文件。"
        },
        "help": {
            "text": "修复建议：\n1. 使用白名单限制可访问的文件\n2. 规范化路径并验证是否在允许范围内\n3. 使用安全的文件访问API\n4. 禁止路径中的特殊字符(如../)\n5. 将用户文件存储在专用目录"
        },
        "cwe": ["CWE-22"],
    },
    "ssrf-python": {
        "id": "ssrf-python",
        "name": "服务器端请求伪造(SSRF)",
        "shortDescription": {
            "text": "应用程序允许攻击者控制服务器发起任意网络请求"
        },
        "fullDescription": {
            "text": "服务器端请求伪造(SSRF)允许攻击者利用服务器发起对内部网络或外部系统的请求。攻击者可以访问内部服务、云元数据端点，或作为跳板攻击其他系统。"
        },
        "help": {
            "text": "修复建议：\n1. 对目标URL进行白名单验证\n2. 禁用对内网地址的访问\n3. 使用URL解析库验证主机名\n4. 限制响应大小和超时时间\n5. 在DMZ网络中部署请求服务"
        },
        "cwe": ["CWE-918"],
    },
    "deserialization-python": {
        "id": "deserialization-python",
        "name": "不安全反序列化",
        "shortDescription": {
            "text": "应用程序反序列化不受信任的数据"
        },
        "fullDescription": {
            "text": "不安全的反序列化允许攻击者通过操纵序列化数据执行任意代码。当应用程序反序列化来自不可信来源的数据时，攻击者可以构造恶意载荷，在反序列化过程中触发代码执行。"
        },
        "help": {
            "text": "修复建议：\n1. 避免反序列化不可信数据\n2. 使用安全的序列化格式(JSON代替pickle)\n3. 对序列化数据进行数字签名验证\n4. 在反序列化前进行模式验证\n5. 在隔离环境中运行反序列化操作"
        },
        "cwe": ["CWE-502"],
    },
    "hardcoded-secret-python": {
        "id": "hardcoded-secret-python",
        "name": "硬编码密钥",
        "shortDescription": {
            "text": "代码中直接包含密码、密钥等敏感信息"
        },
        "fullDescription": {
            "text": "硬编码密钥是指将密码、API密钥、令牌等敏感信息直接写入源代码中。这会导致凭证泄露，攻击者可以通过读取代码获取这些敏感信息，从而访问受保护资源。"
        },
        "help": {
            "text": "修复建议：\n1. 使用环境变量存储敏感信息\n2. 使用密钥管理服务(AWS KMS等)\n3. 使用配置文件并排除在版本控制外\n4. 定期轮换密钥\n5. 使用密钥扫描工具检测提交"
        },
        "cwe": ["CWE-798", "CWE-259"],
    },
    "weak-cryptography-python": {
        "id": "weak-cryptography-python",
        "name": "弱加密算法",
        "shortDescription": {
            "text": "使用已知弱点的加密算法或协议"
        },
        "fullDescription": {
            "text": "弱加密算法是指已知存在安全漏洞的加密算法，如MD5、SHA1、DES等。使用这些算法可能导致数据被破解，敏感信息泄露，或者通信被中间人攻击。"
        },
        "help": {
            "text": "修复建议：\n1. 使用强加密算法(AES-256, SHA-256等)\n2. 保持加密库更新到最新版本\n3. 使用安全的随机数生成器\n4. 遵循最新的加密最佳实践\n5. 定期评估加密方案"
        },
        "cwe": ["CWE-327"],
    },
}

# 风险等级到SARIF等级的映射
SEVERITY_MAPPING: Dict[str, str] = {
    "严重": "error",
    "高危": "error",
    "中危": "warning",
    "低危": "note",
}


@dataclass
class CodeLocation:
    """代码位置信息"""
    file_path: str
    line_number: int
    column_offset: int = 1
    code_snippet: str = ""


@dataclass
class CallChainNode:
    """调用链节点"""
    function_name: str
    file_path: str
    line_number: int
    code_snippet: str
    is_source: bool = False
    is_sink: bool = False


@dataclass
class SecurityFinding:
    """安全漏洞发现记录"""
    rule_id: str
    name: str
    cwe: Optional[str]
    file_path: str
    line_number: int
    column_offset: int
    code_snippet: str
    description: str
    call_chain: Optional[List[CallChainNode]] = None


class SARIFFormatter:
    """SARIF v2.1.0 格式化器"""

    def __init__(self, tool_version: str = "1.0.0") -> None:
        """初始化SARIF格式化器
        
        参数:
            tool_version: 安全审计工具的版本号
        """
        self.tool_version = tool_version
        self.rules: Dict[str, Dict[str, Any]] = {}
        self.artifacts: Dict[str, Dict[str, Any]] = {}

    def _generate_fingerprint(self, finding: SecurityFinding) -> str:
        """生成漏洞指纹用于去重
        
        参数:
            finding: 安全漏洞发现记录
            
        返回:
            漏洞的唯一指纹哈希值
        """
        content = f"{finding.rule_id}:{finding.file_path}:{finding.line_number}:{finding.code_snippet}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_or_create_rule(self, rule_id: str) -> Dict[str, Any]:
        """获取或创建SARIF规则定义
        
        参数:
            rule_id: 规则标识符
            
        返回:
            SARIF规则定义字典
        """
        if rule_id not in self.rules:
            # 从预定义规则表中查找
            if rule_id in VULNERABILITY_RULES:
                rule_def = VULNERABILITY_RULES[rule_id].copy()
            else:
                # 创建默认规则定义
                rule_def = {
                    "id": rule_id,
                    "name": f"未知漏洞类型: {rule_id}",
                    "shortDescription": {"text": "未定义的漏洞类型"},
                    "fullDescription": {"text": "此漏洞类型暂无详细描述"},
                    "help": {"text": "请联系安全团队获取修复建议"},
                    "cwe": [],
                }
            self.rules[rule_id] = rule_def
        return self.rules[rule_id]

    def _add_artifact(self, file_path: str) -> int:
        """添加扫描的源代码文件到artifacts列表
        
        参数:
            file_path: 文件路径
            
        返回:
            artifact在数组中的索引
        """
        if file_path not in self.artifacts:
            idx = len(self.artifacts)
            self.artifacts[file_path] = {
                "index": idx,
                "location": {"uri": file_path},
            }
        return self.artifacts[file_path]["index"]

    def format_finding(self, finding: SecurityFinding) -> Dict[str, Any]:
        """将安全漏洞发现记录转换为SARIF结果格式
        
        参数:
            finding: 安全漏洞发现记录
            
        返回:
            SARIF格式的结果字典
        """
        # 获取规则定义
        rule = self._get_or_create_rule(finding.rule_id)
        
        # 添加文件到artifacts
        artifact_idx = self._add_artifact(finding.file_path)
        
        # 构建SARIF结果
        result: Dict[str, Any] = {
            "ruleId": finding.rule_id,
            "ruleIndex": list(self.rules.keys()).index(finding.rule_id),
            "level": SEVERITY_MAPPING.get("", "warning"),
            "message": {
                "text": finding.description,
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": finding.file_path,
                            "index": artifact_idx,
                        },
                        "region": {
                            "startLine": finding.line_number,
                            "startColumn": finding.column_offset,
                            "snippet": {
                                "text": finding.code_snippet,
                            },
                        },
                    },
                }
            ],
            "fingerprints": {
                "primary": self._generate_fingerprint(finding),
            },
            "properties": {
                "cwe": finding.cwe,
                "rule_id": finding.rule_id,
            },
        }
        
        # 如果存在调用链，添加到codeFlows
        if finding.call_chain and len(finding.call_chain) > 0:
            result["codeFlows"] = self._format_code_flows(finding.call_chain)
        
        # 添加CWE标签
        if finding.cwe or rule.get("cwe"):
            cwes = []
            if finding.cwe:
                cwes.append(finding.cwe)
            if rule.get("cwe"):
                cwes.extend(rule["cwe"])
            result["taxa"] = [{"id": cwe} for cwe in set(cwes)]
        
        return result

    def _format_code_flows(self, call_chain: List[CallChainNode]) -> List[Dict[str, Any]]:
        """将调用链格式化为SARIF codeFlows
        
        参数:
            call_chain: 调用链节点列表
            
        返回:
            SARIF codeFlows数组
        """
        thread_flows = []
        locations = []
        
        for i, node in enumerate(call_chain):
            # 添加文件到artifacts
            artifact_idx = self._add_artifact(node.file_path)
            
            # 构建位置信息
            location = {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": node.file_path,
                        "index": artifact_idx,
                    },
                    "region": {
                        "startLine": node.line_number,
                        "snippet": {
                            "text": node.code_snippet,
                        },
                    },
                },
                "message": {
                    "text": f"{node.function_name} "
                    f"({'污点来源' if node.is_source else '危险汇点' if node.is_sink else '中间调用'})",
                },
            }
            
            # 构建线程流位置
            thread_flow_loc = {
                "step": i + 1,
                "location": location,
                "kind": "taint",
                "properties": {
                    "isSource": node.is_source,
                    "isSink": node.is_sink,
                },
            }
            locations.append(thread_flow_loc)
        
        code_flow = {
            "threadFlows": [
                {
                    "locations": locations,
                }
            ]
        }
        
        return [code_flow]

    def add_code_flow(
        self, result: Dict[str, Any], call_chain: List[CallChainNode]
    ) -> Dict[str, Any]:
        """为SARIF结果添加调用链信息
        
        参数:
            result: 现有的SARIF结果字典
            call_chain: 调用链节点列表
            
        返回:
            添加了codeFlows的结果字典
        """
        result["codeFlows"] = self._format_code_flows(call_chain)
        return result

    def generate_sarif(
        self, findings: List[SecurityFinding], target_path: str = ""
    ) -> Dict[str, Any]:
        """生成完整的SARIF文档
        
        参数:
            findings: 安全漏洞发现记录列表
            target_path: 扫描目标路径
            
        返回:
            完整的SARIF文档字典
        """
        # 重置状态
        self.rules = {}
        self.artifacts = {}
        
        # 格式化所有发现
        results = [self.format_finding(f) for f in findings]
        
        # 构建SARIF文档
        sarif_doc: Dict[str, Any] = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "security-audit",
                            "version": self.tool_version,
                            "informationUri": "https://github.com/example/security-audit",
                            "rules": list(self.rules.values()),
                        }
                    },
                    "artifacts": [
                        {"location": {"uri": path}} for path in self.artifacts.keys()
                    ],
                    "results": results,
                    "invocations": [
                        {
                            "executionSuccessful": True,
                            "startTimeUtc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                        }
                    ],
                }
            ],
        }
        
        # 添加原始目标路径
        if target_path:
            sarif_doc["runs"][0]["originalUriBaseIds"] = {
                "PROJECTROOT": {
                    "uri": f"file://{Path(target_path).absolute()}/",
                }
            }
        
        # 添加属性
        sarif_doc["runs"][0]["properties"] = {
            "findingsCount": len(findings),
            "rulesCount": len(self.rules),
            "artifactsCount": len(self.artifacts),
        }
        
        return sarif_doc

    def save_report(
        self, sarif_doc: Dict[str, Any], output_path: str, indent: int = 2
    ) -> str:
        """将SARIF文档保存为JSON文件
        
        参数:
            sarif_doc: SARIF文档字典
            output_path: 输出文件路径
            indent: JSON缩进空格数
            
        返回:
            保存的文件路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sarif_doc, f, indent=indent, ensure_ascii=False)
        
        return str(output_file.absolute())


def _demo_findings() -> List[SecurityFinding]:
    """生成演示用的漏洞发现记录"""
    return [
        SecurityFinding(
            rule_id="sql-injection-python",
            name="SQL注入漏洞",
            cwe="CWE-89",
            file_path="app/database.py",
            line_number=42,
            column_offset=12,
            code_snippet="cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
            description="检测到SQL注入漏洞，用户输入直接拼接到SQL语句中",
            call_chain=[
                CallChainNode(
                    function_name="get_user_input",
                    file_path="app/views.py",
                    line_number=15,
                    code_snippet="user_id = request.args.get('id')",
                    is_source=True,
                ),
                CallChainNode(
                    function_name="process_user",
                    file_path="app/utils.py",
                    line_number=28,
                    code_snippet="result = query_user(uid)",
                ),
                CallChainNode(
                    function_name="query_user",
                    file_path="app/database.py",
                    line_number=42,
                    code_snippet="cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
                    is_sink=True,
                ),
            ],
        ),
        SecurityFinding(
            rule_id="command-exec-python",
            name="命令执行漏洞",
            cwe="CWE-78",
            file_path="app/utils.py",
            line_number=23,
            column_offset=8,
            code_snippet="os.system(user_cmd)",
            description="检测到命令执行漏洞，用户输入直接传递给系统命令",
        ),
        SecurityFinding(
            rule_id="xss-python",
            name="跨站脚本攻击",
            cwe="CWE-79",
            file_path="app/templates.py",
            line_number=56,
            column_offset=20,
            code_snippet="return f\"<div>{user_content}</div>\"",
            description="检测到XSS漏洞，用户内容未转义直接输出",
        ),
    ]


def main() -> int:
    """主函数 - 演示SARIF格式化器功能"""
    print("=== SARIF v2.1.0 格式化器演示 ===\n")
    
    # 创建格式化器实例
    formatter = SARIFFormatter(tool_version="1.0.0")
    
    # 获取演示数据
    findings = _demo_findings()
    
    print(f"发现 {len(findings)} 个安全漏洞\n")
    
    # 显示漏洞详情
    for i, finding in enumerate(findings, 1):
        print(f"[{i}] {finding.name}")
        print(f"    文件: {finding.file_path}:{finding.line_number}")
        print(f"    等级: {""}")
        print(f"    描述: {finding.description}")
        if finding.call_chain:
            print(f"    调用链: {len(finding.call_chain)} 个节点")
        print()
    
    # 生成SARIF文档
    print("正在生成SARIF文档...")
    sarif_doc = formatter.generate_sarif(findings, target_path="/app")
    
    # 验证SARIF结构
    print(f"✓ SARIF版本: {sarif_doc['version']}")
    print(f"✓ 工具名称: {sarif_doc['runs'][0]['tool']['driver']['name']}")
    print(f"✓ 规则数量: {len(sarif_doc['runs'][0]['tool']['driver']['rules'])}")
    print(f"✓ 结果数量: {len(sarif_doc['runs'][0]['results'])}")
    print(f"✓ Artifacts数量: {len(sarif_doc['runs'][0]['artifacts'])}")
    
    # 保存报告
    output_path = "/tmp/security-audit-report.sarif"
    saved_path = formatter.save_report(sarif_doc, output_path)
    print(f"\n✓ SARIF报告已保存: {saved_path}")
    
    # 显示报告片段
    print("\n=== SARIF报告片段 ===")
    print(json.dumps(sarif_doc["runs"][0]["results"][0], indent=2, ensure_ascii=False)[:800])
    print("...")
    
    print("\n=== 演示完成 ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
