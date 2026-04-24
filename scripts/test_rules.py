#!/usr/bin/env python3
"""
安全审计规则自动化测试脚本
验证所有规则文件能正确命中对应的测试样本
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RULES_DIR = PROJECT_ROOT / "references" / "rules"
SAMPLES_DIR = PROJECT_ROOT / "test-samples"

RULE_SAMPLE_MAP = {
    "sql-injection-python.yml": "sql_injection_python.py",
    "sql-injection-java.yml": "sql_injection_java.java",
    "sql-injection-mybatis-xml.yml": "sql_injection_mybatis.xml",
    "sql-injection-go.yml": "sql_injection_go.go",
    "sql-injection-php.yml": "sql_injection_php.php",
    "sql-injection-csharp.yml": "sql_injection_csharp.cs",
    "sql-injection-javascript.yml": "sql_injection_javascript.js",
    "command-exec-python.yml": "command_exec_python.py",
    "command-exec-java.yml": "command_exec_java.java",
    "jndi-injection-java.yml": "jndi_injection_java.java",
    "command-exec-go.yml": "command_exec_go.go",
    "command-exec-php.yml": "command_exec_php.php",
    "command-exec-csharp.yml": "command_exec_csharp.cs",
    "command-exec-javascript.yml": "command_exec_javascript.js",
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
    "open-redirect-python.yml": "open_redirect_python.py",
    "open-redirect-java.yml": "open_redirect_java.java",
    "open-redirect-go.yml": "open_redirect_go.go",
    "open-redirect-php.yml": "open_redirect_php.php",
    "open-redirect-csharp.yml": "open_redirect_csharp.cs",
    "open-redirect-ruby.yml": "open_redirect_ruby.rb",
    "open-redirect-rust.yml": "open_redirect_rust.rs",
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
    "nosql-injection-java.yml": "nosql_injection_java.java",
    "nosql-injection-python.yml": "nosql_injection_python.py",
    "nosql-injection-php.yml": "nosql_injection_php.php",
    "nosql-injection-go.yml": "nosql_injection_go.go",
    "nosql-injection-csharp.yml": "nosql_injection_csharp.cs",
    "nosql-injection-ruby.yml": "nosql_injection_ruby.rb",
    "nosql-injection-rust.yml": "nosql_injection_rust.rs",
    "prototype-pollution-javascript.yml": "prototype_pollution_javascript.js",
    "sql-injection-ruby.yml": "sql_injection_ruby.rb",
    "command-exec-ruby.yml": "command_exec_ruby.rb",
    "xss-ruby.yml": "xss_ruby.rb",
    "path-traversal-ruby.yml": "path_traversal_ruby.rb",
    "ssrf-ruby.yml": "ssrf_ruby.rb",
    "xxe-ruby.yml": "xxe_ruby.rb",
    "deserialization-ruby.yml": "deserialization_ruby.rb",
    "auth-defects-ruby.yml": "auth_defects_ruby.rb",
    "hardcoded-secrets-ruby.yml": "hardcoded_secrets_ruby.rb",
    "sql-injection-rust.yml": "sql_injection_rust.rs",
    "command-exec-rust.yml": "command_exec_rust.rs",
    "xss-rust.yml": "xss_rust.rs",
    "path-traversal-rust.yml": "path_traversal_rust.rs",
    "ssrf-rust.yml": "ssrf_rust.rs",
    "xxe-rust.yml": "xxe_rust.rs",
    "deserialization-rust.yml": "deserialization_rust.rs",
    "auth-defects-rust.yml": "auth_defects_rust.rs",
    "hardcoded-secrets-rust.yml": "hardcoded_secrets_rust.rs",
    "ssti-java.yml": "ssti_java.java",
    "ssti-go.yml": "ssti_go.go",
    "ssti-php.yml": "ssti_php.php",
    "ssti-csharp.yml": "ssti_csharp.cs",
    "ssti-javascript.yml": "ssti_javascript.js",
    "ssti-ruby.yml": "ssti_ruby.rb",
    "ssti-rust.yml": "ssti_rust.rs",
    "prototype-pollution-python.yml": "prototype_pollution_python.py",
    "prototype-pollution-java.yml": "prototype_pollution_java.java",
    "prototype-pollution-go.yml": "prototype_pollution_go.go",
    "prototype-pollution-php.yml": "prototype_pollution_php.php",
    "prototype-pollution-csharp.yml": "prototype_pollution_csharp.cs",
    "prototype-pollution-ruby.yml": "prototype_pollution_ruby.rb",
    "prototype-pollution-rust.yml": "prototype_pollution_rust.rs",
    "jndi-injection-python.yml": "jndi_injection_python.py",
    "jndi-injection-go.yml": "jndi_injection_go.go",
    "jndi-injection-php.yml": "jndi_injection_php.php",
    "jndi-injection-csharp.yml": "jndi_injection_csharp.cs",
    "jndi-injection-javascript.yml": "jndi_injection_javascript.js",
    "jndi-injection-ruby.yml": "jndi_injection_ruby.rb",
    "jndi-injection-rust.yml": "jndi_injection_rust.rs",
}

SAFE_SAMPLE_MAP = {
    rule_name: f"safe_{sample_name}"
    for rule_name, sample_name in RULE_SAMPLE_MAP.items()
}


def run_ast_grep(rule_file: Path, sample_file: Path) -> list:
    # ast-grep's HTML parser skips .xml files; copy to .html temporarily
    temp_file = None
    target_file = sample_file
    if sample_file.suffix == ".xml":
        temp_file = Path(tempfile.gettempdir()) / f"{sample_file.stem}.html"
        shutil.copy(str(sample_file), str(temp_file))
        target_file = temp_file

    cmd = [
        "ast-grep", "scan",
        "--rule", str(rule_file),
        str(target_file),
        "--json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if temp_file and temp_file.exists():
        temp_file.unlink()

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
