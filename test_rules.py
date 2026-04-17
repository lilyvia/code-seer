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
    "sql-injection-java.yml": "sqli_java.java",
    "sql-injection-go.yml": "sqli_go.go",
    "sql-injection-php.yml": "sqli_php.php",
    "sql-injection-csharp.yml": "sqli_csharp.cs",
    "sql-injection-javascript.yml": "sqli_javascript.js",
    "command-exec-python.yml": "python_cmd_exec.py",
    "command-exec-java.yml": "java_cmd_exec.java",
    "jndi-injection-java.yml": "jndi_injection_java.java",
    "command-exec-go.yml": "go_cmd_exec.go",
    "command-exec-php.yml": "php_cmd_exec.php",
    "command-exec-csharp.yml": "csharp_cmd_exec.cs",
    "command-exec-javascript.yml": "cmd_exec_javascript.js",
    "xss-javascript.yml": "xss_javascript.js",
    "xss-python.yml": "xss_python.py",
    "xss-java.yml": "xss_java.java",
    "xss-go.yml": "xss_go.go",
    "xss-csharp.yml": "xss_csharp.cs",
    "xss-php.yml": "xss_php.php",
    "path-traversal-python.yml": "path_traversal_python.py",
    "path-traversal-java.yml": "path_traversal_java.java",
    "path-traversal-go.yml": "path_traversal_go.go",
    "path-traversal-php.yml": "path_traversal_php.php",
    "path-traversal-csharp.yml": "path_traversal_csharp.cs",
    "path-traversal-javascript.yml": "path_traversal_javascript.js",
    "open-redirect-javascript.yml": "open_redirect_javascript.js",
    "ssrf-python.yml": "ssrf_python.py",
    "ssrf-java.yml": "ssrf_java.java",
    "ssrf-go.yml": "ssrf_go.go",
    "ssrf-php.yml": "ssrf_php.php",
    "ssrf-csharp.yml": "ssrf_csharp.cs",
    "ssrf-javascript.yml": "ssrf_javascript.js",
    "xxe-python.yml": "xxe_python.py",
    "xxe-java.yml": "xxe_java.java",
    "xxe-go.yml": "xxe_go.go",
    "xxe-php.yml": "xxe_php.php",
    "xxe-csharp.yml": "xxe_csharp.cs",
    "xxe-javascript.yml": "xxe_javascript.js",
    "deserialization-python.yml": "deserialization_python.py",
    "ssti-python.yml": "ssti_python.py",
    "deserialization-java.yml": "deserialization_java.java",
    "deserialization-go.yml": "deserialization_go.go",
    "deserialization-php.yml": "deserialization_php.php",
    "deserialization-csharp.yml": "deserialization_csharp.cs",
    "deserialization-javascript.yml": "deserialization_javascript.js",
    "auth-defects-python.yml": "auth_defects_python.py",
    "auth-defects-java.yml": "auth_defects_java.java",
    "auth-defects-go.yml": "auth_defects_go.go",
    "auth-defects-php.yml": "auth_defects_php.php",
    "auth-defects-csharp.yml": "auth_defects_csharp.cs",
    "auth-defects-javascript.yml": "auth_defects_javascript.js",
    "hardcoded-secrets-python.yml": "hardcoded_secrets_python.py",
    "hardcoded-secrets-java.yml": "hardcoded_secrets_java.java",
    "hardcoded-secrets-go.yml": "hardcoded_secrets_go.go",
    "hardcoded-secrets-php.yml": "hardcoded_secrets_php.php",
    "hardcoded-secrets-csharp.yml": "hardcoded_secrets_csharp.cs",
    "hardcoded-secrets-javascript.yml": "hardcoded_secrets_javascript.js",
    "nosql-injection-javascript.yml": "nosql_injection_javascript.js",
    "prototype-pollution-javascript.yml": "prototype_pollution_javascript.js",
    "sql-injection-ruby.yml": "sqli_ruby.rb",
    "command-exec-ruby.yml": "cmd_exec_ruby.rb",
    "xss-ruby.yml": "xss_ruby.rb",
    "path-traversal-ruby.yml": "path_traversal_ruby.rb",
    "ssrf-ruby.yml": "ssrf_ruby.rb",
    "xxe-ruby.yml": "xxe_ruby.rb",
    "deserialization-ruby.yml": "deserialization_ruby.rb",
    "auth-defects-ruby.yml": "auth_defects_ruby.rb",
    "hardcoded-secrets-ruby.yml": "hardcoded_secrets_ruby.rb",
    "sql-injection-rust.yml": "test_rust.rs",
    "command-exec-rust.yml": "test_rust.rs",
    "xss-rust.yml": "test_rust.rs",
    "path-traversal-rust.yml": "path_traversal_rust.rs",
    "ssrf-rust.yml": "ssrf_rust.rs",
    "xxe-rust.yml": "xxe_rust.rs",
    "deserialization-rust.yml": "deserialization_rust.rs",
    "auth-defects-rust.yml": "auth_defects_rust.rs",
    "hardcoded-secrets-rust.yml": "hardcoded_secrets_rust.rs",
}

SAFE_SAMPLE_MAP = {
    rule_name: f"safe_{sample_name}"
    for rule_name, sample_name in RULE_SAMPLE_MAP.items()
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
        safe_sample_name = SAFE_SAMPLE_MAP.get(rule_name)

        if sample_name is None or safe_sample_name is None:
            print(f"[SKIP] {rule_name:45s} -> 缺少正样本或负样本映射")
            skipped += 1
            continue

        sample_file = SAMPLES_DIR / sample_name
        safe_sample_file = SAMPLES_DIR / safe_sample_name

        if not sample_file.exists() or not safe_sample_file.exists():
            missing_samples = []
            if not sample_file.exists():
                missing_samples.append(sample_name)
            if not safe_sample_file.exists():
                missing_samples.append(safe_sample_name)
            print(f"[FAIL] {rule_name:45s} -> 样本缺失: {', '.join(missing_samples)}")
            failed += 1
            continue

        positive_matches = run_ast_grep(rule_file, sample_file)
        negative_matches = run_ast_grep(rule_file, safe_sample_file)

        if len(positive_matches) > 0 and len(negative_matches) == 0:
            print(
                f"[PASS] {rule_name:45s} -> 正样本 {len(positive_matches):2d} 个匹配, "
                f"负样本 {len(negative_matches):2d} 个匹配"
            )
            passed += 1
        else:
            print(
                f"[FAIL] {rule_name:45s} -> 正样本 {len(positive_matches):2d} 个匹配, "
                f"负样本 {len(negative_matches):2d} 个匹配"
            )
            failed += 1

    print("-" * 60)
    print(f"结果: {passed} 通过, {failed} 失败, {skipped} 跳过")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
