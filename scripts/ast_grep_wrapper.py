#!/usr/bin/env python3
"""
AST-grep CLI包装器
用于执行ast-grep命令并解析结果
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AstGrepMatch:
    """AST-grep匹配结果"""
    rule_id: str
    file_path: str
    line_number: int
    column_start: int
    column_end: int
    text: str
    message: str


class AstGrepWrapper:
    """AST-grep包装器类"""
    
    def __init__(self):
        """初始化，检查ast-grep是否安装"""
        self._check_ast_grep()
    
    def _check_ast_grep(self):
        """检查ast-grep是否已安装"""
        try:
            result = subprocess.run(
                ['ast-grep', '--version'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError("ast-grep未正确安装")
        except FileNotFoundError:
            raise RuntimeError(
                "ast-grep未安装。请运行: npm install -g @ast-grep/cli"
            )
    
    def get_version(self) -> str:
        """获取ast-grep版本"""
        result = subprocess.run(
            ['ast-grep', '--version'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def scan(self, rule_file: str, target_path: str) -> List[AstGrepMatch]:
        """
        使用指定规则文件扫描目标路径
        
        参数:
            rule_file: YAML规则文件路径
            target_path: 要扫描的目录或文件路径
        
        返回:
            匹配结果列表
        """
        cmd = [
            'ast-grep', 'scan',
            '--rule', rule_file,
            '--json',
            target_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode not in [0, 1]:  # 0=无匹配, 1=有匹配
            raise RuntimeError(f"ast-grep执行失败: {result.stderr}")
        
        return self._parse_output(result.stdout)
    
    def _parse_output(self, json_output: str) -> List[AstGrepMatch]:
        """解析ast-grep JSON输出"""
        matches = []
        
        if not json_output.strip():
            return matches
        
        try:
            data = json.loads(json_output)
            
            # 处理不同版本的ast-grep输出格式
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and 'hits' in data:
                items = data['hits']
            else:
                items = []
            
            for item in items:
                match = AstGrepMatch(
                    rule_id=item.get('ruleId', 'unknown'),
                    file_path=item.get('file', ''),
                    line_number=item.get('range', {}).get('start', {}).get('line', 0),
                    column_start=item.get('range', {}).get('start', {}).get('column', 0),
                    column_end=item.get('range', {}).get('end', {}).get('column', 0),
                    text=item.get('text', ''),
                    message=item.get('message', '')
                )
                matches.append(match)
        
        except json.JSONDecodeError as e:
            print(f"解析ast-grep输出失败: {e}")
        
        return matches


def run_ast_grep(rule_file: str, target_path: str) -> List[Dict[str, Any]]:
    """
    便捷的ast-grep执行函数
    
    参数:
        rule_file: YAML规则文件路径
        target_path: 要扫描的目标路径
    
    返回:
        匹配结果字典列表
    """
    wrapper = AstGrepWrapper()
    matches = wrapper.scan(rule_file, target_path)
    
    # 转换为字典列表
    return [
        {
            "rule_id": m.rule_id,
            "file_path": m.file_path,
            "line_number": m.line_number,
            "column": m.column_start,
            "text": m.text,
            "message": m.message
        }
        for m in matches
    ]


if __name__ == '__main__':
    # 测试代码
    import sys
    
    wrapper = AstGrepWrapper()
    print(f"AST-grep版本: {wrapper.get_version()}")
    print("ast-grep集成成功！")
