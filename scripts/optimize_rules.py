#!/usr/bin/env python3
"""
批量优化安全扫描规则文件
- 精简 description 为第一句话
- 精简 remediation 移除安全措施列表
- 统一字段命名
"""

import re
from pathlib import Path

def extract_first_sentence(text: str) -> str:
    """提取第一段的第一句话"""
    # 先将所有行合并，处理跨行的情况
    full_text = text.strip()
    lines = full_text.split('\n')
    
    # 收集第一段的非空行
    first_paragraph_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            break
        if stripped.startswith('-') or stripped.startswith('此规则'):
            break
        first_paragraph_lines.append(stripped)
    
    # 合并第一段的行
    first_paragraph = ' '.join(first_paragraph_lines)
    
    # 找到第一个完整的句子（以。或.结尾）
    match = re.search(r'^([^。.]+?[。.])', first_paragraph)
    if match:
        return match.group(1).strip()
    
    # 如果没有找到句子结束符，返回整个第一段
    return first_paragraph.strip() if first_paragraph else lines[0].strip() if lines else ""

def clean_remediation(text: str) -> str:
    """清理 remediation，移除安全措施列表"""
    lines = text.strip().split('\n')
    cleaned = []
    in_code_block = False
    skip_section = False
    
    for line in lines:
        stripped = line.strip()
        
        # 跟踪代码块状态
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            cleaned.append(line)
            continue
        
        # 在代码块内保留所有内容
        if in_code_block:
            cleaned.append(line)
            continue
        
        # 检测安全措施/注意事项部分开始
        if any(marker in stripped for marker in [
            '安全措施：', '注意事项：', '安全建议：',
            '其他安全措施', '最佳实践'
        ]):
            skip_section = True
            continue
        
        # 跳过安全措施列表项
        if skip_section and stripped.startswith('-'):
            continue
        
        # 如果遇到空行且不在代码块内，重置跳过状态
        if not stripped and skip_section:
            skip_section = False
            cleaned.append(line)
            continue
        
        if not skip_section:
            cleaned.append(line)
    
    # 过滤掉末尾的空行
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    
    return '\n'.join(cleaned)

def optimize_rule_file(file_path: Path) -> bool:
    """优化单个规则文件"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # 1. 提取并精简 description
    desc_match = re.search(r'^description:\s*\|\s*\n(.*?)(?=^\w+:|\Z)', content, re.MULTILINE | re.DOTALL)
    if desc_match:
        original_desc = desc_match.group(1)
        # 处理缩进
        desc_lines = original_desc.split('\n')
        # 找到基础缩进（通常是2个空格）
        base_indent = 2
        cleaned_desc_lines = []
        for line in desc_lines:
            if line.strip():
                # 去除基础缩进
                cleaned_line = line[base_indent:] if line.startswith('  ') else line
                cleaned_desc_lines.append(cleaned_line)
        
        full_desc = '\n'.join(cleaned_desc_lines)
        short_desc = extract_first_sentence(full_desc)
        
        # 替换 description
        if short_desc:
            # 保留yaml格式，使用单行或短多行
            if len(short_desc) < 60 and '\n' not in short_desc:
                new_desc = f"description: {short_desc}\n"
            else:
                new_desc = f"description: |\n  {short_desc}\n"
            
            # 替换整个 description 块
            pattern = r'^description:\s*\|\s*\n.*?(?=^\w+:|\Z)'
            content = re.sub(pattern, new_desc, content, flags=re.MULTILINE | re.DOTALL)
    
    # 2. 精简 remediation
    rem_match = re.search(r'^remediation:\s*\|\s*\n(.*?)(?=^\w+:|\Z)', content, re.MULTILINE | re.DOTALL)
    if rem_match:
        original_rem = rem_match.group(1)
        # 处理缩进
        rem_lines = original_rem.split('\n')
        base_indent = 2
        cleaned_rem_lines = []
        for line in rem_lines:
            if line.strip():
                cleaned_line = line[base_indent:] if line.startswith('  ') else line
                cleaned_rem_lines.append(cleaned_line)
        
        full_rem = '\n'.join(cleaned_rem_lines)
        cleaned_rem = clean_remediation(full_rem)
        
        if cleaned_rem:
            # 重新添加缩进
            indented_rem = '\n'.join('  ' + line if line.strip() else line for line in cleaned_rem.split('\n'))
            new_rem = f"remediation: |\n{indented_rem}\n"
            
            pattern = r'^remediation:\s*\|\s*\n.*?(?=^\w+:|\Z)'
            content = re.sub(pattern, new_rem, content, flags=re.MULTILINE | re.DOTALL)
    
    # 3. 移除 message 字段（如果没用到）
    # message 通常与 description 重复
    content = re.sub(r'^message:.*\n', '', content, flags=re.MULTILINE)
    
    # 4. 移除 risk_severity（保留 severity）
    content = re.sub(r'^risk_severity:.*\n', '', content, flags=re.MULTILINE)
    
    # 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 如果内容有变化，写回文件
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    
    return False

def main():
    rules_dir = Path('references/rules')
    rule_files = list(rules_dir.glob('*.yml'))
    
    print(f"发现 {len(rule_files)} 个规则文件")
    print("开始批量优化...\n")
    
    optimized_count = 0
    for rule_file in sorted(rule_files):
        try:
            if optimize_rule_file(rule_file):
                print(f"✓ 已优化: {rule_file.name}")
                optimized_count += 1
            else:
                print(f"- 无变化: {rule_file.name}")
        except Exception as e:
            print(f"✗ 错误: {rule_file.name} - {e}")
    
    print(f"\n完成! 优化了 {optimized_count}/{len(rule_files)} 个文件")

if __name__ == '__main__':
    main()
