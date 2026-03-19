#!/usr/bin/env python3
"""
安全审计报告生成器
用于生成中文Markdown格式的安全审计报告
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# 风险等级枚举
class SeverityLevel:
    """风险等级常量定义"""
    CRITICAL = "严重"
    HIGH = "高危"
    MEDIUM = "中危"
    LOW = "低危"


# 风险等级对应的颜色徽章
SEVERITY_BADGES: Dict[str, str] = {
    SeverityLevel.CRITICAL: "🔴 严重",
    SeverityLevel.HIGH: "🟠 高危",
    SeverityLevel.MEDIUM: "🟡 中危",
    SeverityLevel.LOW: "🟢 低危",
}

# 风险等级排序权重
SEVERITY_WEIGHTS: Dict[str, int] = {
    SeverityLevel.CRITICAL: 4,
    SeverityLevel.HIGH: 3,
    SeverityLevel.MEDIUM: 2,
    SeverityLevel.LOW: 1,
}


@dataclass
class Finding:
    """
    安全漏洞发现记录
    
    包含漏洞的完整信息，用于生成报告
    """
    rule_id: str  # 规则ID
    name: str  # 漏洞名称
    severity: str  # 风险等级：严重/高危/中危/低危
    file_path: str  # 文件路径
    line_number: int  # 行号
    code_snippet: str  # 代码片段
    description: str  # 漏洞描述
    
    # 六个必需字段
    reproduction_steps: str = ""  # 复现步骤
    entry_point: str = ""  # 漏洞入口
    call_chain: List[Dict[str, Any]] = field(default_factory=list)  # 调用链
    remediation: str = ""  # 修复建议
    false_positive_note: str = ""  # 疑似误报说明
    
    # 可选字段
    cwe: Optional[str] = None  # CWE编号
    column_offset: int = 0  # 列偏移
    confidence: float = 1.0  # 置信度（0.0-1.0）
    language: str = "python"  # 代码语言


@dataclass
class ReportMetadata:
    """
    报告元数据
    
    包含报告生成的时间、目标路径等基本信息
    """
    target_path: str  # 扫描目标路径
    scan_start_time: datetime = field(default_factory=datetime.now)  # 扫描开始时间
    scan_end_time: Optional[datetime] = None  # 扫描结束时间
    scanner_version: str = "1.0.0"  # 扫描器版本
    total_files: int = 0  # 扫描文件总数
    
    def get_duration(self) -> float:
        """获取扫描持续时间（秒）"""
        if self.scan_end_time is None:
            return 0.0
        return (self.scan_end_time - self.scan_start_time).total_seconds()


@dataclass
class ReportData:
    """
    报告数据结构
    
    保存所有漏洞发现结果和报告元数据
    """
    metadata: ReportMetadata  # 报告元数据
    findings: List[Finding] = field(default_factory=list)  # 漏洞列表
    
    def get_findings_by_severity(self, severity: str) -> List[Finding]:
        """按风险等级获取漏洞列表"""
        return [f for f in self.findings if f.severity == severity]
    
    def get_severity_counts(self) -> Dict[str, int]:
        """获取各风险等级的漏洞数量统计"""
        counts = {
            SeverityLevel.CRITICAL: 0,
            SeverityLevel.HIGH: 0,
            SeverityLevel.MEDIUM: 0,
            SeverityLevel.LOW: 0,
        }
        for finding in self.findings:
            if finding.severity in counts:
                counts[finding.severity] += 1
        return counts
    
    def get_sorted_findings(self) -> List[Finding]:
        """按风险等级排序的漏洞列表（严重优先）"""
        return sorted(
            self.findings,
            key=lambda f: SEVERITY_WEIGHTS.get(f.severity, 0),
            reverse=True
        )


class MarkdownFormatter:
    """
    Markdown报告格式化器
    
    将漏洞数据格式化为中文Markdown报告
    """
    
    def __init__(self, report_data: ReportData):
        """
        初始化格式化器
        
        参数:
            report_data: 报告数据对象
        """
        self.report_data = report_data
    
    def generate_summary(self) -> str:
        """
        生成执行摘要
        
        包含漏洞总数、各等级分布统计、扫描概览等信息
        
        返回:
            Markdown格式的执行摘要字符串
        """
        counts = self.report_data.get_severity_counts()
        total = len(self.report_data.findings)
        meta = self.report_data.metadata
        
        lines: List[str] = []
        lines.append("## 📊 执行摘要\n")
        
        # 扫描概览
        lines.append("### 扫描概览")
        lines.append(f"- **扫描目标**: `{meta.target_path}`")
        lines.append(f"- **扫描文件数**: {meta.total_files} 个")
        lines.append(f"- **扫描时间**: {meta.scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if meta.scan_end_time:
            duration = meta.get_duration()
            lines.append(f"- **扫描耗时**: {duration:.2f} 秒")
        lines.append(f"- **扫描器版本**: v{meta.scanner_version}")
        lines.append("")
        
        # 漏洞统计
        lines.append("### 漏洞统计")
        lines.append(f"- **漏洞总数**: {total} 个")
        lines.append("")
        
        # 风险等级分布表格
        lines.append("| 风险等级 | 数量 | 占比 |")
        lines.append("|---------|------|------|")
        
        for severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, 
                        SeverityLevel.MEDIUM, SeverityLevel.LOW]:
            count = counts.get(severity, 0)
            percentage = (count / total * 100) if total > 0 else 0
            badge = SEVERITY_BADGES.get(severity, severity)
            lines.append(f"| {badge} | {count} | {percentage:.1f}% |")
        
        lines.append("")
        
        # 风险概览
        if total > 0:
            critical_count = counts.get(SeverityLevel.CRITICAL, 0)
            high_count = counts.get(SeverityLevel.HIGH, 0)
            
            if critical_count > 0:
                lines.append(
                    f"> ⚠️ **警告**: 发现 {critical_count} 个严重漏洞，建议立即修复！"
                )
            elif high_count > 0:
                lines.append(
                    f"> ⚠️ **注意**: 发现 {high_count} 个高危漏洞，建议优先处理。"
                )
            else:
                lines.append(
                    f"> ✅ **状态**: 未发现严重或高危漏洞，整体风险可控。"
                )
        else:
            lines.append("> ✅ **状态**: 未发现安全漏洞！")
        
        lines.append("")
        return "\n".join(lines)
    
    def generate_table_of_contents(self) -> str:
        """
        生成目录
        
        为报告生成中文目录，包含各风险等级的锚点链接
        
        返回:
            Markdown格式的目录字符串
        """
        lines: List[str] = []
        lines.append("## 📑 目录\n")
        
        counts = self.report_data.get_severity_counts()
        
        # 按风险等级分组
        for severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH,
                        SeverityLevel.MEDIUM, SeverityLevel.LOW]:
            count = counts.get(severity, 0)
            if count > 0:
                badge = SEVERITY_BADGES.get(severity, severity)
                anchor = self._severity_to_anchor(severity)
                lines.append(f"- [{badge} ({count})](#{anchor})")
        
        lines.append("")
        return "\n".join(lines)
    
    def format_finding(self, finding: Finding, index: int) -> str:
        """
        格式化单个漏洞详情
        
        包含6个必需字段的中文格式化输出：
        - 复现步骤
        - 漏洞入口
        - 调用链
        - 风险等级
        - 修复建议
        - 疑似误报说明
        
        参数:
            finding: 漏洞发现对象
            index: 漏洞序号
        
        返回:
            Markdown格式的漏洞详情字符串
        """
        lines: List[str] = []
        
        # 漏洞标题
        badge = SEVERITY_BADGES.get(finding.severity, finding.severity)
        lines.append(f"### {index}. {finding.name} {badge}\n")
        
        # 基本信息
        lines.append("#### 📋 基本信息")
        lines.append(f"- **规则ID**: `{finding.rule_id}`")
        if finding.cwe:
            lines.append(f"- **CWE编号**: [{finding.cwe}](https://cwe.mitre.org/data/definitions/{finding.cwe.replace('CWE-', '')}.html)")
        lines.append(f"- **文件位置**: `{finding.file_path}:{finding.line_number}`")
        lines.append(f"- **置信度**: {finding.confidence * 100:.0f}%")
        lines.append("")
        
        # 漏洞描述
        lines.append("#### 📝 漏洞描述")
        lines.append(finding.description)
        lines.append("")
        
        # 代码片段
        lines.append("#### 💻 代码片段")
        lines.append(f"```{finding.language}")
        lines.append(finding.code_snippet.strip())
        lines.append("```")
        lines.append("")
        
        # 1. 复现步骤
        lines.append("#### 🔍 复现步骤")
        if finding.reproduction_steps:
            lines.append(finding.reproduction_steps)
        else:
            lines.append("1. 定位到漏洞所在代码位置")
            lines.append(f"2. 在 `{finding.file_path}` 第 {finding.line_number} 行设置断点")
            lines.append("3. 构造恶意输入触发漏洞代码路径")
            lines.append("4. 观察程序行为确认漏洞存在")
        lines.append("")
        
        # 2. 漏洞入口
        lines.append("#### 🚪 漏洞入口")
        if finding.entry_point:
            lines.append(finding.entry_point)
        else:
            lines.append(f"- **入口函数**: `{finding.rule_id}`")
            lines.append(f"- **入口位置**: `{finding.file_path}:{finding.line_number}`")
            lines.append("- **入口参数**: 用户可控输入")
        lines.append("")
        
        # 3. 调用链
        lines.append("#### 🔗 调用链")
        if finding.call_chain:
            lines.append(self._format_call_chain_ascii(finding.call_chain))
        else:
            # 生成默认调用链可视化
            lines.append(self._generate_default_call_chain(finding))
        lines.append("")
        
        # 4. 风险等级
        lines.append("#### ⚠️ 风险等级")
        lines.append(f"**{SEVERITY_BADGES.get(finding.severity, finding.severity)}**")
        lines.append("")
        
        # 风险说明
        risk_descriptions: Dict[str, str] = {
            SeverityLevel.CRITICAL: "该漏洞可能导致系统完全沦陷，数据泄露或远程代码执行。",
            SeverityLevel.HIGH: "该漏洞可能导致敏感信息泄露或权限提升，需要尽快修复。",
            SeverityLevel.MEDIUM: "该漏洞在特定条件下可能被利用，建议计划修复。",
            SeverityLevel.LOW: "该漏洞风险较低，可在常规维护中处理。",
        }
        lines.append(risk_descriptions.get(finding.severity, "风险等级待评估。"))
        lines.append("")
        
        # 5. 修复建议
        lines.append("#### 🔧 修复建议")
        if finding.remediation:
            lines.append(finding.remediation)
        else:
            lines.append("建议采取以下修复措施：")
            lines.append("1. 对用户输入进行严格的验证和过滤")
            lines.append("2. 使用参数化查询或预编译语句")
            lines.append("3. 对输出进行适当的编码和转义")
            lines.append("4. 遵循最小权限原则")
        lines.append("")
        
        # 6. 疑似误报说明
        lines.append("#### 🤔 疑似误报说明")
        if finding.false_positive_note:
            lines.append(finding.false_positive_note)
        else:
            lines.append("- **误报可能性**: 低")
            lines.append("- **判断依据**: 代码模式匹配，未检测到明显的安全防护措施")
            lines.append("- **建议**: 人工复核确认是否为真实漏洞")
        lines.append("")
        
        # 分隔线
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)
    
    def _format_call_chain_ascii(self, call_chain: List[Dict[str, Any]]) -> str:
        """
        格式化调用链ASCII可视化
        
        将调用链数据转换为ASCII艺术图
        
        参数:
            call_chain: 调用链节点列表
        
        返回:
            ASCII格式的调用链可视化字符串
        """
        lines: List[str] = []
        lines.append("```")
        
        if not call_chain:
            lines.append("(调用链为空)")
            lines.append("```")
            return "\n".join(lines)
        
        # 漏洞入口
        first_node = call_chain[0]
        lines.append("+-- 漏洞入口")
        lines.append(f"|   {first_node.get('function_name', 'unknown')} ")
        lines.append(f"|   ({first_node.get('file_path', 'unknown')}:{first_node.get('line_number', 0)})")
        if 'code_snippet' in first_node:
            snippet = first_node['code_snippet'][:50] + "..." if len(first_node['code_snippet']) > 50 else first_node['code_snippet']
            lines.append(f"|   代码: {snippet}")
        lines.append("|")
        
        # 中间调用
        if len(call_chain) > 2:
            lines.append("+-- 中间调用")
            for i, node in enumerate(call_chain[1:-1], 1):
                lines.append(f"|   [{i}] {node.get('function_name', 'unknown')}")
                lines.append(f"|       ({node.get('file_path', 'unknown')}:{node.get('line_number', 0)})")
                if 'code_snippet' in node:
                    snippet = node['code_snippet'][:40] + "..." if len(node['code_snippet']) > 40 else node['code_snippet']
                    lines.append(f"|       代码: {snippet}")
            lines.append("|")
        
        # 危险操作
        if len(call_chain) > 1:
            last_node = call_chain[-1]
            lines.append("+-- 危险操作")
            lines.append(f"    {last_node.get('function_name', 'unknown')}")
            lines.append(f"    ({last_node.get('file_path', 'unknown')}:{last_node.get('line_number', 0)})")
            if 'code_snippet' in last_node:
                snippet = last_node['code_snippet'][:50] + "..." if len(last_node['code_snippet']) > 50 else last_node['code_snippet']
                lines.append(f"    代码: {snippet}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def _generate_default_call_chain(self, finding: Finding) -> str:
        """
        生成默认调用链可视化
        
        当没有详细调用链数据时使用
        
        参数:
            finding: 漏洞发现对象
        
        返回:
            ASCII格式的默认调用链可视化字符串
        """
        lines: List[str] = []
        lines.append("```")
        lines.append("+-- 漏洞入口")
        lines.append(f"|   用户输入接收点")
        lines.append(f"|   ({finding.file_path}:{finding.line_number})")
        lines.append("|")
        lines.append("+-- 数据流传播")
        lines.append("|   污点数据传播路径")
        lines.append("|")
        lines.append("+-- 危险操作")
        lines.append(f"    {finding.rule_id}")
        lines.append(f"    ({finding.file_path}:{finding.line_number})")
        lines.append("```")
        return "\n".join(lines)
    
    def _severity_to_anchor(self, severity: str) -> str:
        """
        将风险等级转换为锚点ID
        
        参数:
            severity: 风险等级字符串
        
        返回:
            用于Markdown锚点的字符串
        """
        anchor_map = {
            SeverityLevel.CRITICAL: "严重",
            SeverityLevel.HIGH: "高危",
            SeverityLevel.MEDIUM: "中危",
            SeverityLevel.LOW: "低危",
        }
        return anchor_map.get(severity, severity)
    
    def generate_findings_by_severity(self, severity: str) -> str:
        """
        生成特定风险等级的漏洞列表
        
        参数:
            severity: 风险等级（严重/高危/中危/低危）
        
        返回:
            Markdown格式的漏洞列表字符串
        """
        findings = self.report_data.get_findings_by_severity(severity)
        if not findings:
            return ""
        
        lines: List[str] = []
        badge = SEVERITY_BADGES.get(severity, severity)
        anchor = self._severity_to_anchor(severity)
        
        lines.append(f"## {badge} <a id='{anchor}'></a>\n")
        
        # 按置信度排序
        sorted_findings = sorted(findings, key=lambda f: f.confidence, reverse=True)
        
        for i, finding in enumerate(sorted_findings, 1):
            lines.append(self.format_finding(finding, i))
        
        return "\n".join(lines)
    
    def generate_report(self) -> str:
        """
        生成完整报告
        
        组装所有部分生成完整的Markdown报告
        
        返回:
            完整的Markdown报告字符串
        """
        lines: List[str] = []
        
        # 报告标题
        lines.append("# 🔒 安全审计报告\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 执行摘要
        lines.append(self.generate_summary())
        
        # 目录
        if self.report_data.findings:
            lines.append(self.generate_table_of_contents())
        
        # 按风险等级分组展示漏洞
        for severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH,
                        SeverityLevel.MEDIUM, SeverityLevel.LOW]:
            section = self.generate_findings_by_severity(severity)
            if section:
                lines.append(section)
        
        # 报告结尾
        lines.append("## 📌 附录\n")
        lines.append("### 风险等级说明")
        lines.append("- 🔴 **严重**: 可能导致系统完全沦陷，需要立即修复")
        lines.append("- 🟠 **高危**: 可能导致敏感数据泄露或权限提升，需要优先修复")
        lines.append("- 🟡 **中危**: 在特定条件下可能被利用，建议计划修复")
        lines.append("- 🟢 **低危**: 风险较低，可在常规维护中处理")
        lines.append("")
        
        lines.append("---")
        lines.append("*报告由安全审计扫描器自动生成*")
        
        return "\n".join(lines)


def create_sample_findings() -> List[Finding]:
    """
    创建示例漏洞数据
    
    用于测试报告生成功能
    
    返回:
        示例漏洞发现列表
    """
    return [
        Finding(
            rule_id="sql-injection-python",
            name="SQL注入漏洞",
            severity=SeverityLevel.CRITICAL,
            file_path="app/database.py",
            line_number=42,
            code_snippet="cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
            description="用户输入直接拼接到SQL查询中，存在SQL注入风险。攻击者可通过构造恶意输入执行任意SQL语句，窃取或篡改数据库数据。",
            reproduction_steps="""1. 访问用户详情页面
2. 在URL参数中输入 `?id=1 OR 1=1`
3. 观察是否返回所有用户数据
4. 尝试输入 `?id=1; DROP TABLE users--` 测试数据破坏性""",
            entry_point="用户输入通过HTTP GET参数传入，未经任何过滤直接传入数据库查询函数",
            call_chain=[
                {"function_name": "get_user", "file_path": "app/views.py", "line_number": 25, 
                 "code_snippet": "user_id = request.args.get('id')"},
                {"function_name": "fetch_user_data", "file_path": "app/service.py", "line_number": 38,
                 "code_snippet": "return db.query_user(user_id)"},
                {"function_name": "query_user", "file_path": "app/database.py", "line_number": 42,
                 "code_snippet": "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")"},
            ],
            remediation="""1. 使用参数化查询：
   ```python
   cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
   ```
2. 对所有用户输入进行类型校验和长度限制
3. 使用ORM框架提供的查询构造器
4. 对数据库账户使用最小权限原则""",
            false_positive_note="- **误报可能性**: 低\n- **判断依据**: 明确使用f-string拼接SQL语句，无参数化查询迹象\n- **建议**: 确认为真实漏洞，需立即修复",
            cwe="CWE-89",
            confidence=0.95,
            language="python",
        ),
        Finding(
            rule_id="command-injection-python",
            name="命令注入漏洞",
            severity=SeverityLevel.HIGH,
            file_path="app/utils.py",
            line_number=78,
            code_snippet="os.system(f\"ping -c 1 {hostname}\")",
            description="用户可控的主机名参数直接拼接到系统命令中，攻击者可通过注入恶意命令执行任意系统指令。",
            reproduction_steps="""1. 找到网络诊断功能入口
2. 在主机名输入框中填入 `; cat /etc/passwd`
3. 提交表单
4. 观察响应中是否包含系统文件内容""",
            entry_point="用户通过表单提交主机名，服务端直接将其拼接到ping命令",
            call_chain=[
                {"function_name": "network_diag", "file_path": "app/views.py", "line_number": 56,
                 "code_snippet": "hostname = request.form.get('host')"},
                {"function_name": "ping_host", "file_path": "app/utils.py", "line_number": 78,
                 "code_snippet": "os.system(f\"ping -c 1 {hostname}\")"},
            ],
            remediation="""1. 使用subprocess模块并传递参数列表：
   ```python
   subprocess.run(['ping', '-c', '1', hostname], check=True)
   ```
2. 对主机名进行严格的正则验证，只允许合法的主机名字符
3. 避免使用shell=True参数
4. 考虑使用专门的网络库替代系统命令""",
            false_positive_note="- **误报可能性**: 极低\n- **判断依据**: 直接使用os.system执行拼接命令，无任何过滤\n- **建议**: 确认为高危漏洞，需紧急修复",
            cwe="CWE-78",
            confidence=0.98,
            language="python",
        ),
        Finding(
            rule_id="hardcoded-secret",
            name="硬编码密钥",
            severity=SeverityLevel.MEDIUM,
            file_path="config/settings.py",
            line_number=15,
            code_snippet='SECRET_KEY = "sk_live_abcdefghijklmnopqrstuvwxyz123456"',
            description="代码中硬编码了生产环境密钥，如果代码泄露，攻击者可直接获取敏感凭证。",
            reproduction_steps="""1. 查看配置文件config/settings.py
2. 第15行直接暴露密钥常量
3. 密钥格式符合支付平台API密钥特征""",
            entry_point="配置文件中的硬编码密钥常量",
            call_chain=[
                {"function_name": "settings.py", "file_path": "config/settings.py", "line_number": 15,
                 "code_snippet": 'SECRET_KEY = "sk_live_abcdefghijklmnopqrstuvwxyz123456"'},
            ],
            remediation="""1. 将密钥移至环境变量：
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```
2. 使用密钥管理系统（如AWS KMS、HashiCorp Vault）
3. 将密钥文件加入.gitignore
4. 轮换已泄露的密钥""",
            false_positive_note="- **误报可能性**: 中\n- **判断依据**: 虽然看起来像密钥，但可能是测试用的假密钥\n- **建议**: 确认是否为真实密钥，如是则需立即轮换",
            cwe="CWE-798",
            confidence=0.75,
            language="python",
        ),
        Finding(
            rule_id="debug-mode-enabled",
            name="调试模式开启",
            severity=SeverityLevel.LOW,
            file_path="app.py",
            line_number=8,
            code_snippet="app.run(debug=True)",
            description="应用程序以调试模式运行，可能暴露敏感信息和调试接口。",
            reproduction_steps="""1. 查看app.py启动文件
2. 确认debug参数设置为True
3. 访问任意不存在的URL触发调试页面""",
            entry_point="应用启动时的调试模式配置",
            remediation="""1. 在生产环境禁用调试模式：
   ```python
   debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
   app.run(debug=debug)
   ```
2. 使用环境变量控制调试开关
3. 配置专门的日志系统替代调试输出""",
            false_positive_note="- **误报可能性**: 低\n- **判断依据**: 明确设置debug=True\n- **建议**: 确认是否在生产环境部署，如是则需关闭",
            cwe="CWE-489",
            confidence=0.90,
            language="python",
        ),
    ]


def main() -> int:
    """
    主函数 - 演示报告生成功能
    
    返回:
        程序退出码
    """
    print("=== 安全审计报告生成器演示 ===\n")
    
    # 创建示例数据
    sample_findings = create_sample_findings()
    
    # 创建报告元数据
    metadata = ReportMetadata(
        target_path="/path/to/source/code",
        total_files=156,
        scanner_version="1.0.0",
    )
    metadata.scan_end_time = datetime.now()
    
    # 创建报告数据
    report_data = ReportData(
        metadata=metadata,
        findings=sample_findings,
    )
    
    # 创建格式化器并生成报告
    formatter = MarkdownFormatter(report_data)
    report = formatter.generate_report()
    
    # 输出报告
    print(report)
    
    # 保存到文件
    output_path = Path("security_audit_report.md")
    output_path.write_text(report, encoding="utf-8")
    print(f"\n✅ 报告已保存到: {output_path.absolute()}")
    
    # 打印统计信息
    counts = report_data.get_severity_counts()
    print("\n=== 漏洞统计 ===")
    for severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH,
                    SeverityLevel.MEDIUM, SeverityLevel.LOW]:
        count = counts.get(severity, 0)
        print(f"{SEVERITY_BADGES.get(severity, severity)}: {count} 个")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
