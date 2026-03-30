#!/usr/bin/env python3
"""
安全审计扫描器主程序
用于检测代码中的安全漏洞
"""

import argparse
import json
import sys
import yaml
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache

from ast_grep_wrapper import AstGrepWrapper
from report_generator import MarkdownFormatter, ReportData, ReportMetadata, Finding, SeverityLevel
from sarif_formatter import SARIFFormatter, SecurityFinding as SarifSecurityFinding, CallChainNode
from call_chain_tracer import CallChainTracer, CallChain
from taint_tracker import TaintTracker
from call_graph import CallGraphBuilder
from fp_filter import FalsePositiveFilter, FilterResult


@dataclass
class AuditConfig:
    """扫描配置类"""
    target_path: str
    mode: str = "quick"  # quick, comprehensive
    output_format: str = "markdown"  # markdown, json, sarif
    fail_on: Optional[str] = None
    workers: int = 4  # 并行工作进程数
    timeout: int = 30  # 单个文件扫描超时时间（秒）


@dataclass
class SecurityFinding:
    """安全漏洞发现记录"""
    rule_id: str
    name: str
    severity: str  # 严重, 高危, 中危, 低危
    cwe: Optional[str]
    file_path: str
    line_number: int
    column_offset: int
    code_snippet: str
    description: str
    remediation: str
    confidence: float  # 0.0 - 1.0
    call_chain: Optional[str] = None
    false_positive_reason: Optional[str] = None


# 文件扩展名到语言的映射
EXTENSION_TO_LANGUAGE = {
    '.py': 'python',
    '.java': 'java',
    '.go': 'go',
    '.php': 'php',
    '.cs': 'csharp',
    '.js': 'javascript',
    '.ts': 'javascript',
}

# 风险等级映射
SEVERITY_MAPPING = {
    'error': '严重',
    'warning': '高危',
    'info': '中危',
    'hint': '低危',
    '严重': '严重',
    '高危': '高危',
    '中危': '中危',
    '低危': '低危',
}


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='安全审计扫描器 - 检测代码中的安全漏洞'
    )
    parser.add_argument('target', help='要扫描的代码目录路径')
    parser.add_argument('--mode', choices=['quick', 'comprehensive'],
                       default='quick', help='扫描模式')
    parser.add_argument('--format', choices=['markdown', 'json', 'sarif'],
                       default='markdown', help='输出格式')
    parser.add_argument('--fail-on', choices=['严重', '高危', '中危', '低危'],
                       help='发现指定等级及以上漏洞时返回错误码')
    parser.add_argument('-j', '--workers', type=int, default=None,
                       help='并行扫描进程数（默认：CPU核心数）')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                       help='单个文件扫描超时时间（秒，默认：30）')
    parser.add_argument('--no-parallel', action='store_true',
                       help='禁用并行扫描（使用串行模式）')
    return parser.parse_args()


def discover_files(target_path: str) -> List[Path]:
    """发现要扫描的文件"""
    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"目标路径不存在: {target_path}")

    # 支持的语言扩展名
    extensions = set(EXTENSION_TO_LANGUAGE.keys())

    files = []
    if target.is_file():
        if target.suffix in extensions:
            files.append(target)
    else:
        for ext in extensions:
            files.extend(target.rglob(f'*{ext}'))

    # 过滤掉测试文件和第三方库
    files = [f for f in files if 'test' not in f.name.lower()
             and 'node_modules' not in str(f)
             and '.git' not in str(f)]

    return files


def get_rule_files(rules_dir: Path) -> List[Path]:
    """获取所有YAML规则文件"""
    return list(rules_dir.glob('*.yml'))


@lru_cache(maxsize=128)
def load_rule_metadata(rule_file: str) -> Dict[str, Any]:
    """加载YAML规则文件的元数据（带缓存）"""
    try:
        with open(rule_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"警告: 无法加载规则文件 {rule_file}: {e}")
        return {}


def _load_rule_metadata_uncached(rule_file: Path) -> Dict[str, Any]:
    """加载YAML规则文件的元数据（不带缓存，用于pickle序列化）"""
    try:
        with open(rule_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"警告: 无法加载规则文件 {rule_file}: {e}")
        return {}
    """加载YAML规则文件的元数据"""
    try:
        with open(rule_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"警告: 无法加载规则文件 {rule_file}: {e}")
        return {}


def get_rules_for_language(rules_dir: Path, language: str) -> List[Path]:
    """获取指定语言的规则文件"""
    all_rules = get_rule_files(rules_dir)
    matching_rules = []

    for rule_file in all_rules:
        metadata = load_rule_metadata(str(rule_file))
        if metadata.get('language') == language:
            matching_rules.append(rule_file)

    return matching_rules


def ast_match_to_security_finding(match: Dict[str, Any], rule_metadata: Dict[str, Any]) -> SecurityFinding:
    """将ast-grep匹配结果转换为SecurityFinding对象"""
    # 从规则元数据获取信息
    rule_id = rule_metadata.get('id', 'unknown')
    name = rule_metadata.get('name', '未知漏洞')
    severity = rule_metadata.get('risk_severity') or SEVERITY_MAPPING.get(
        rule_metadata.get('severity', 'warning'), '中危'
    )
    cwe = rule_metadata.get('cwe')
    description = rule_metadata.get('description', rule_metadata.get('message', ''))
    remediation = rule_metadata.get('remediation', '请参考相关安全文档进行修复')

    # 从匹配结果获取位置信息
    file_path = match.get('file_path', '')
    line_number = match.get('line_number', 0)
    column = match.get('column', 0)
    code_snippet = match.get('text', '')

    return SecurityFinding(
        rule_id=rule_id,
        name=name,
        severity=severity,
        cwe=cwe,
        file_path=file_path,
        line_number=line_number,
        column_offset=column,
        code_snippet=code_snippet,
        description=description,
        remediation=remediation,
        confidence=0.9  # 默认置信度
    )


def _scan_file_worker(args: tuple) -> List[Dict[str, Any]]:
    """
    工作进程函数：扫描单个文件（必须是顶层函数才能被pickle序列化）

    参数:
        args: (file_path_str, rules_dir_str, timeout)

    返回:
        发现结果的字典列表
    """
    file_path_str, rules_dir_str, timeout = args
    file_path = Path(file_path_str)
    rules_dir = Path(rules_dir_str)

    findings = []

    # 获取文件语言
    language = EXTENSION_TO_LANGUAGE.get(file_path.suffix)
    if not language:
        return findings

    # 获取该语言的规则
    all_rules = get_rule_files(rules_dir)
    rules = []
    for rule_file in all_rules:
        metadata = _load_rule_metadata_uncached(rule_file)
        if metadata.get('language') == language:
            rules.append((rule_file, metadata))

    if not rules:
        return findings

    # 创建新的wrapper实例（每个进程一个）
    try:
        ast_wrapper = AstGrepWrapper()
    except RuntimeError:
        return findings

    # 使用每个规则扫描文件
    for rule_file, rule_metadata in rules:
        try:
            matches = ast_wrapper.scan(str(rule_file), str(file_path), timeout=timeout)

            for match in matches:
                finding = {
                    "rule_id": rule_metadata.get('id', 'unknown'),
                    "name": rule_metadata.get('name', '未知漏洞'),
                    "severity": rule_metadata.get('risk_severity') or SEVERITY_MAPPING.get(
                        rule_metadata.get('severity', 'warning'), '中危'
                    ),
                    "cwe": rule_metadata.get('cwe'),
                    "file_path": match.file_path,
                    "line_number": match.line_number,
                    "column_offset": match.column_start,
                    "code_snippet": match.text,
                    "description": rule_metadata.get('description', rule_metadata.get('message', '')),
                    "remediation": rule_metadata.get('remediation', '请参考相关安全文档进行修复'),
                    "confidence": 0.9
                }
                findings.append(finding)

        except Exception:
            continue

    return findings


def scan_file(file_path: Path, rules_dir: Path, ast_wrapper: AstGrepWrapper, timeout: int = 30) -> List[SecurityFinding]:
    """扫描单个文件（串行版本，用于兼容性）"""
    findings = []

    # 获取文件语言
    language = EXTENSION_TO_LANGUAGE.get(file_path.suffix)
    if not language:
        return findings

    # 获取该语言的规则
    rules = get_rules_for_language(rules_dir, language)

    # 使用每个规则扫描文件
    for rule_file in rules:
        try:
            rule_metadata = load_rule_metadata(str(rule_file))
            matches = ast_wrapper.scan(str(rule_file), str(file_path), timeout=timeout)

            for match in matches:
                finding = SecurityFinding(
                    rule_id=rule_metadata.get('id', 'unknown'),
                    name=rule_metadata.get('name', '未知漏洞'),
                    severity=rule_metadata.get('risk_severity') or SEVERITY_MAPPING.get(
                        rule_metadata.get('severity', 'warning'), '中危'
                    ),
                    cwe=rule_metadata.get('cwe'),
                    file_path=match.file_path,
                    line_number=match.line_number,
                    column_offset=match.column_start,
                    code_snippet=match.text,
                    description=rule_metadata.get('description', rule_metadata.get('message', '')),
                    remediation=rule_metadata.get('remediation', '请参考相关安全文档进行修复'),
                    confidence=0.9
                )
                findings.append(finding)

        except Exception as e:
            print(f"警告: 使用规则 {rule_file.name} 扫描 {file_path} 时出错: {e}")
            continue

    return findings


def enhance_findings_with_call_chains_and_filter(findings: List[SecurityFinding]) -> List[SecurityFinding]:
    """使用CallChainTracer增强发现结果并应用FalsePositiveFilter过滤"""
    if not findings:
        return findings

    taint_tracker = TaintTracker()
    call_graph = CallGraphBuilder()

    for finding in findings:
        code = finding.code_snippet
        file_path = finding.file_path
        line_num = finding.line_number

        func_name = f"func_{finding.rule_id}_{line_num}"
        call_graph.add_function(func_name, file_path, line_num)

    tracer = CallChainTracer(taint_tracker=taint_tracker, call_graph_builder=call_graph)
    tracer.trace_chains()

    fp_filter = FalsePositiveFilter()

    finding_dicts = []
    for f in findings:
        finding_dict = {
            "rule_id": f.rule_id,
            "file_path": f.file_path,
            "line_number": f.line_number,
            "code_snippet": f.code_snippet,
            "description": f.description,
            "name": f.name,
            "severity": f.severity,
            "cwe": f.cwe,
        }
        finding_dicts.append(finding_dict)

    filtered_dicts = fp_filter.filter_findings(finding_dicts, include_filtered=True)

    enhanced_findings = []
    for i, fd in enumerate(filtered_dicts):
        original_finding = findings[i]

        call_chain_str = None
        if tracer.chains and i < len(tracer.chains):
            call_chain_str = tracer.chains[i].format_ascii()

        false_positive_reason = None
        if fd.get("filter_result") == FilterResult.FILTER.value:
            false_positive_reason = fd.get("filter_reason", "误报过滤")
        elif fd.get("filter_result") == FilterResult.REVIEW.value:
            false_positive_reason = f"需要复核: {fd.get('filter_reason', '')}"

        enhanced_finding = SecurityFinding(
            rule_id=original_finding.rule_id,
            name=original_finding.name,
            severity=original_finding.severity,
            cwe=original_finding.cwe,
            file_path=original_finding.file_path,
            line_number=original_finding.line_number,
            column_offset=original_finding.column_offset,
            code_snippet=original_finding.code_snippet,
            description=original_finding.description,
            remediation=original_finding.remediation,
            confidence=original_finding.confidence,
            call_chain=call_chain_str,
            false_positive_reason=false_positive_reason,
        )
        enhanced_findings.append(enhanced_finding)

    return [f for f in enhanced_findings if f.false_positive_reason is None or not f.false_positive_reason.startswith("误报过滤")]


def generate_markdown_output(findings: List[SecurityFinding], config: AuditConfig, files_scanned: int) -> str:
    """生成Markdown格式输出"""
    from datetime import datetime

    # 创建ReportData
    metadata = ReportMetadata(
        target_path=config.target_path,
        scan_start_time=datetime.now(),
        total_files=files_scanned,
    )
    metadata.scan_end_time = datetime.now()

    # 转换SecurityFinding为report_generator.Finding
    report_findings = []
    for f in findings:
        finding = Finding(
            rule_id=f.rule_id,
            name=f.name,
            severity=f.severity,
            file_path=f.file_path,
            line_number=f.line_number,
            code_snippet=f.code_snippet,
            description=f.description,
            remediation=f.remediation,
            cwe=f.cwe,
            column_offset=f.column_offset,
            confidence=f.confidence,
        )
        report_findings.append(finding)

    report_data = ReportData(metadata=metadata, findings=report_findings)
    formatter = MarkdownFormatter(report_data)
    return formatter.generate_report()


def generate_sarif_output(findings: List[SecurityFinding], config: AuditConfig) -> str:
    """生成SARIF格式输出"""
    formatter = SARIFFormatter(tool_version="1.0.0")

    # 转换为sarif_formatter的SecurityFinding格式
    sarif_findings = []
    for f in findings:
        sarif_finding = SarifSecurityFinding(
            rule_id=f.rule_id,
            name=f.name,
            severity=f.severity,
            cwe=f.cwe,
            file_path=f.file_path,
            line_number=f.line_number,
            column_offset=f.column_offset,
            code_snippet=f.code_snippet,
            description=f.description,
            remediation=f.remediation,
            confidence=f.confidence,
        )
        sarif_findings.append(sarif_finding)

    sarif_doc = formatter.generate_sarif(sarif_findings, target_path=config.target_path)
    return json.dumps(sarif_doc, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    args = parse_arguments()

    # 确定并行工作进程数
    workers = args.workers if args.workers else os.cpu_count() or 4
    use_parallel = not args.no_parallel and workers > 1

    config = AuditConfig(
        target_path=args.target,
        mode=args.mode,
        output_format=args.format,
        fail_on=args.fail_on,
        workers=workers,
        timeout=args.timeout
    )

    # 发现文件
    files = discover_files(config.target_path)
    print(f"发现 {len(files)} 个待扫描文件")

    if not files:
        print("没有找到可扫描的文件")
        return 0

    # 初始化ast-grep包装器
    try:
        ast_wrapper = AstGrepWrapper()
        print(f"AST-grep版本: {ast_wrapper.get_version()}")
    except RuntimeError as e:
        print(f"错误: {e}")
        return 1

    # 获取规则目录
    script_dir = Path(__file__).parent.resolve()
    rules_dir = script_dir.parent / 'references' / 'rules'

    if not rules_dir.exists():
        print(f"错误: 规则目录不存在: {rules_dir}")
        return 1

    print(f"规则目录: {rules_dir}")
    print(f"可用规则数: {len(get_rule_files(rules_dir))}")

    # 扫描所有文件
    all_findings = []

    if use_parallel:
        print(f"使用并行扫描（{workers}个进程）...")
        # 准备参数列表
        scan_args = [(str(f), str(rules_dir), config.timeout) for f in files]

        completed = 0
        failed = 0

        print(f"扫描进度: 0/{len(files)} 文件", end='', flush=True)

        with ProcessPoolExecutor(max_workers=workers) as executor:
            # 提交所有任务
            future_to_file = {
                executor.submit(_scan_file_worker, args): files[i]
                for i, args in enumerate(scan_args)
            }

            # 处理完成的任务
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    findings_dicts = future.result()
                    completed += 1

                    # 转换字典为 SecurityFinding 对象
                    for fd in findings_dicts:
                        finding = SecurityFinding(
                            rule_id=fd["rule_id"],
                            name=fd["name"],
                            severity=fd["severity"],
                            cwe=fd.get("cwe"),
                            file_path=fd["file_path"],
                            line_number=fd["line_number"],
                            column_offset=fd["column_offset"],
                            code_snippet=fd["code_snippet"],
                            description=fd["description"],
                            remediation=fd["remediation"],
                            confidence=fd["confidence"]
                        )
                        all_findings.append(finding)

                    # 显示进度（同一行刷新）
                    print(f"\r扫描进度: {completed}/{len(files)} 文件", end='', flush=True)

                except Exception as e:
                    failed += 1
                    completed += 1
                    print(f"\r扫描进度: {completed}/{len(files)} 文件 (失败: {failed})", end='', flush=True)

            print()  # 完成后换行
    else:
        print(f"扫描进度: 0/{len(files)} 文件", end='', flush=True)
        for i, file_path in enumerate(files):
            findings = scan_file(file_path, rules_dir, ast_wrapper, timeout=config.timeout)
            all_findings.extend(findings)
            print(f"\r扫描进度: {i + 1}/{len(files)} 文件", end='', flush=True)
        print()  # 完成后换行

    print(f"应用调用链追踪和误报过滤...")
    all_findings = enhance_findings_with_call_chains_and_filter(all_findings)
    print(f"过滤后剩余 {len(all_findings)} 个发现")

    # 输出结果
    if config.output_format == 'json':
        # 构建紧凑格式：将规则元数据与实例分离，减少重复
        rules_meta = {}
        compact_findings = []

        for f in all_findings:
            # 只保留规则元数据一次
            if f.rule_id not in rules_meta:
                rules_meta[f.rule_id] = {
                    "name": f.name,
                    "severity": f.severity,
                    "cwe": f.cwe,
                    "description": f.description,
                    "remediation": f.remediation,
                }
            # 实例只保留位置信息和引用
            compact_findings.append({
                "rule_id": f.rule_id,
                "file_path": f.file_path,
                "line_number": f.line_number,
                "column_offset": f.column_offset,
                "code_snippet": f.code_snippet,
                "confidence": f.confidence,
                **({"call_chain": f.call_chain} if f.call_chain else {}),
                **({"false_positive_reason": f.false_positive_reason} if f.false_positive_reason else {}),
            })

        output = {
            "target": config.target_path,
            "files_scanned": len(files),
            "findings_count": len(all_findings),
            "rules": rules_meta,
            "findings": compact_findings,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif config.output_format == 'sarif':
        print(generate_sarif_output(all_findings, config))
    else:  # markdown
        print(generate_markdown_output(all_findings, config, len(files)))

    # 检查是否需要返回错误码
    if config.fail_on:
        severity_order = ['低危', '中危', '高危', '严重']
        fail_index = severity_order.index(config.fail_on)

        for finding in all_findings:
            if severity_order.index(finding.severity) >= fail_index:
                print(f"\n发现 {finding.severity} 级别漏洞，返回错误码 1")
                return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
