#!/usr/bin/env python3
"""
安全审计规则自动化测试脚本
验证所有规则文件能正确命中对应的测试样本
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
RULES_DIR = PROJECT_ROOT / "references" / "rules"
SAMPLES_DIR = PROJECT_ROOT / "test-samples"

RULE_SAMPLE_MAP = {
    "sql-injection-python.yml": "sqli_python.py",
    "sql-injection-java.yml": "SqliJava.java",
    "sql-injection-go.yml": "sqli_go.go",
    "sql-injection-php.yml": "sqli_php.php",
    "sql-injection-csharp.yml": "SqliCsharp.cs",
    "sql-injection-javascript.yml": "javascript_vulnerable.js",
    "command-exec-python.yml": "python_cmd_exec.py",
    "command-exec-java.yml": "java_cmd_exec.java",
    "command-exec-go.yml": "go_cmd_exec.go",
    "command-exec-php.yml": "php_cmd_exec.php",
    "command-exec-csharp.yml": "csharp_cmd_exec.cs",
    "command-exec-javascript.yml": "javascript_vulnerable.js",
    "xss-javascript.yml": "javascript_vulnerable.js",
    "xss-php.yml": None,
    "path-traversal-python.yml": "path_traversal_python.py",
    "path-traversal-java.yml": None,
    "path-traversal-go.yml": None,
    "path-traversal-php.yml": None,
    "path-traversal-csharp.yml": None,
    "path-traversal-javascript.yml": "javascript_vulnerable.js",
    "ssrf-python.yml": "ssrf_python.py",
    "ssrf-java.yml": "SsrfJava.java",
    "ssrf-go.yml": "ssrf_go.go",
    "ssrf-php.yml": "ssrf_php.php",
    "ssrf-csharp.yml": "SsrfCsharp.cs",
    "ssrf-javascript.yml": "javascript_vulnerable.js",
    "xxe-python.yml": None,
    "xxe-java.yml": None,
    "xxe-php.yml": None,
    "xxe-csharp.yml": None,
    "xxe-javascript.yml": "javascript_vulnerable.js",
    "deserialization-python.yml": "deserialization_python.py",
    "deserialization-java.yml": "deserialization_java.java",
    "deserialization-go.yml": "deserialization_go.go",
    "deserialization-php.yml": "deserialization_php.php",
    "deserialization-csharp.yml": "deserialization_csharp.cs",
    "deserialization-javascript.yml": "javascript_vulnerable.js",
    "auth-defects-python.yml": None,
    "auth-defects-java.yml": None,
    "auth-defects-go.yml": None,
    "auth-defects-php.yml": None,
    "auth-defects-csharp.yml": None,
    "auth-defects-javascript.yml": "javascript_vulnerable.js",
    "hardcoded-secrets-python.yml": None,
    "hardcoded-secrets-java.yml": None,
    "hardcoded-secrets-go.yml": None,
    "hardcoded-secrets-php.yml": None,
    "hardcoded-secrets-csharp.yml": None,
    "hardcoded-secrets-javascript.yml": "javascript_vulnerable.js",
}


def run_ast_grep(rule_file: Path, sample_file: Path) -> list:
    cmd = [
        "ast-grep", "scan",
        "-r", str(rule_file),
        str(sample_file),
        "--json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode not in (0, 1):
        return []
    try:
        return json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return []


def main():
    passed = 0
    failed = 0
    skipped = 0

    all_rules = sorted(RULES_DIR.glob("*.yml"))

    print(f"开始测试 {len(all_rules)} 条规则...")
    print("-" * 60)

    for rule_file in all_rules:
        rule_name = rule_file.name
        sample_name = RULE_SAMPLE_MAP.get(rule_name)

        if sample_name is None:
            print(f"[SKIP] {rule_name:45s} -> 无对应测试样本")
            skipped += 1
            continue

        sample_file = SAMPLES_DIR / sample_name
        if not sample_file.exists():
            print(f"[FAIL] {rule_name:45s} -> 样本缺失: {sample_name}")
            failed += 1
            continue

        matches = run_ast_grep(rule_file, sample_file)

        if len(matches) > 0:
            print(f"[PASS] {rule_name:45s} -> {len(matches):2d} 个匹配")
            passed += 1
        else:
            print(f"[FAIL] {rule_name:45s} -> 0 个匹配")
            failed += 1

    print("-" * 60)
    print(f"结果: {passed} 通过, {failed} 失败, {skipped} 跳过")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
