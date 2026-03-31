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


@dataclass
class Finding:
    """
    安全漏洞发现记录
    
    包含漏洞的完整信息，用于生成报告
    """
    rule_id: str  # 规则ID
    name: str  # 漏洞名称
    file_path: str  # 文件路径
    line_number: int  # 行号
    code_snippet: str  # 代码片段
    description: str  # 漏洞描述
    
    # 可选字段
    cwe: Optional[str] = None  # CWE编号
    column_offset: int = 0  # 列偏移
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
        
        返回:
            Markdown格式的执行摘要字符串
        """
        total = len(self.report_data.findings)
        meta = self.report_data.metadata
        
        lines: List[str] = []
        lines.append("## 执行摘要\n")
        
        # 精简的扫描概览
        lines.append(f"- **目标**: `{meta.target_path}` | **文件数**: {meta.total_files} | **时间**: {meta.scan_start_time.strftime('%Y-%m-%d %H:%M')}")
        
        if total == 0:
            lines.append("- **状态**: 未发现安全漏洞")
        else:
            lines.append(f"- **发现漏洞**: {total} 个")
        
        lines.append("")
        return "\n".join(lines)
    
    def format_finding(self, finding: Finding, index: int) -> str:
        """
        格式化单个漏洞详情
        
        参数:
            finding: 漏洞发现对象
            index: 漏洞序号
        
        返回:
            Markdown格式的漏洞详情字符串
        """
        lines: List[str] = []
        
        # 漏洞标题
        cwe_info = f" [{finding.cwe}]" if finding.cwe else ""
        lines.append(f"### {index}. {finding.name}{cwe_info}")
        lines.append(f"`{finding.file_path}:{finding.line_number}`\n")
        
        # 漏洞描述（精简）
        cleaned_desc = self._clean_description(finding.description)
        if cleaned_desc:
            lines.append(cleaned_desc)
            lines.append("")
        
        # 代码片段（无语言标注）
        lines.append("```")
        lines.append(finding.code_snippet.strip())
        lines.append("```")
        lines.append("")
        
        return "\n".join(lines)
    
    def _clean_description(self, description: str) -> str:
        """清理描述文本，去除冗余内容"""
        if not description:
            return ""
        
        lines = description.strip().split('\n')
        core_desc = []
        
        for line in lines:
            line = line.strip()
            if not line:
                break
            if any(marker in line for marker in [
                '此规则检测', '此规则', '检测以下', '风险：', '典型目标',
                '本规则关注', '安全风险', '可能导致'
            ]):
                break
            core_desc.append(line)
        
        return ' '.join(core_desc) if core_desc else lines[0] if lines else ""
    
    def generate_report(self) -> str:
        """
        生成完整报告
        
        返回:
            完整的Markdown报告字符串
        """
        lines: List[str] = []
        
        # 报告标题
        lines.append(f"# 安全审计报告 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
        
        # 执行摘要
        lines.append(self.generate_summary())
        
        # 漏洞列表
        if self.report_data.findings:
            lines.append("## 漏洞列表\n")
            for i, finding in enumerate(self.report_data.findings, 1):
                lines.append(self.format_finding(finding, i))
        
        return "\n".join(lines)


def create_sample_findings() -> List[Finding]:
    """创建示例漏洞数据"""
    return [
        Finding(
            rule_id="sql-injection-python",
            name="SQL注入漏洞",
            file_path="app/database.py",
            line_number=42,
            code_snippet='cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
            description="用户输入直接拼接到SQL查询中，存在SQL注入风险。",
            cwe="CWE-89",
            language="python",
        ),
        Finding(
            rule_id="command-injection-python",
            name="命令注入漏洞",
            file_path="app/utils.py",
            line_number=78,
            code_snippet='os.system(f"ping -c 1 {hostname}")',
            description="用户可控的主机名参数直接拼接到系统命令中。",
            cwe="CWE-78",
            language="python",
        ),
    ]


def main() -> int:
    """主函数 - 演示报告生成功能"""
    print("=== 安全审计报告生成器演示 ===\n")
    
    sample_findings = create_sample_findings()
    
    metadata = ReportMetadata(
        target_path="/path/to/source/code",
        total_files=156,
        scanner_version="1.0.0",
    )
    metadata.scan_end_time = datetime.now()
    
    report_data = ReportData(
        metadata=metadata,
        findings=sample_findings,
    )
    
    formatter = MarkdownFormatter(report_data)
    report = formatter.generate_report()
    
    print(report)
    
    output_path = Path("security_audit_report.md")
    output_path.write_text(report, encoding="utf-8")
    print(f"\n✅ 报告已保存到: {output_path.absolute()}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
