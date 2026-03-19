#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence


class FilterResult(Enum):
    PASS = "pass"
    FILTER = "filter"
    REVIEW = "review"


@dataclass(frozen=True)
class FilterDecision:
    result: FilterResult
    confidence: float
    reason: str
    filter_name: str


class BaseFilter:
    name = "base"

    def apply(self, finding: Dict[str, Any]) -> Optional[FilterDecision]:
        raise NotImplementedError

    @staticmethod
    def _safe_lower(value: Any) -> str:
        if value is None:
            return ""
        return str(value).lower()

    @classmethod
    def _collect_text(cls, finding: Dict[str, Any], fields: Sequence[str]) -> str:
        return "\n".join(cls._safe_lower(finding.get(field, "")) for field in fields)

    @staticmethod
    def _decision(
        result: FilterResult,
        confidence: float,
        reason: str,
        filter_name: str,
    ) -> FilterDecision:
        bounded = max(0.0, min(1.0, confidence))
        return FilterDecision(
            result=result,
            confidence=bounded,
            reason=reason,
            filter_name=filter_name,
        )


class WhitelistFilter(BaseFilter):
    name = "whitelist"

    _TEST_FILE_RE = re.compile(
        r"(^|/)(test_.*\.py|.*_test\.py|conftest\.py|tests?/.*|spec/.*)$",
        re.IGNORECASE,
    )
    _TEST_FUNCTION_RE = re.compile(
        r"\b(def|async\s+def)\s+test_[a-zA-Z0-9_]*\b|\b(pytest|unittest)\b",
        re.IGNORECASE,
    )
    _DOC_COMMENT_RE = re.compile(
        r"^\s*(#|//|/\*|\*|'''|\"\"\")|(^|\n)\s*(#|//)",
        re.MULTILINE,
    )
    _WRAPPER_RE = re.compile(
        r"\b(safe_execute|safe_query|secure_query|sanitize_input|escape_html|"
        r"validate_and_execute|parameterized_query|prepared_statement|"
        r"safe_sql_execute)\b",
        re.IGNORECASE,
    )

    def apply(self, finding: Dict[str, Any]) -> Optional[FilterDecision]:
        file_path = self._safe_lower(finding.get("file_path", "")).replace("\\", "/")
        if file_path and self._TEST_FILE_RE.search(file_path):
            return self._decision(
                FilterResult.FILTER,
                0.98,
                "命中测试文件白名单",
                self.name,
            )

        text = self._collect_text(
            finding,
            ["code_snippet", "description", "message", "function_name", "name"],
        )
        if text and self._TEST_FUNCTION_RE.search(text):
            return self._decision(
                FilterResult.FILTER,
                0.95,
                "命中测试函数白名单",
                self.name,
            )

        code_snippet = self._safe_lower(finding.get("code_snippet", ""))
        if code_snippet and self._DOC_COMMENT_RE.search(code_snippet):
            return self._decision(
                FilterResult.FILTER,
                0.82,
                "命中注释或文档字符串上下文",
                self.name,
            )

        if text and self._WRAPPER_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.7,
                "疑似安全封装函数调用",
                self.name,
            )

        return None


class DataFlowFilter(BaseFilter):
    name = "data_flow"

    _PARAM_QUERY_RE = re.compile(
        r"(execute|executemany|query)\s*\(.*(%s|\?|:\w+).*(,\s*[^\)]*)\)|"
        r"prepared\s+statement|parameterized\s+queries?",
        re.IGNORECASE | re.DOTALL,
    )
    _ORM_RE = re.compile(
        r"\b(session\.query|queryset|model\.objects\.|objects\.filter\(|"
        r"select\(|where\(|sqlalchemy|django\.db|peewee|gorm|hibernate)\b",
        re.IGNORECASE,
    )
    _SANITIZE_RE = re.compile(
        r"\b(htmlspecialchars|html\.escape|markupsafe\.escape|escape\(|"
        r"bleach\.clean|sanitize\(|xss_clean|quote_plus)\b",
        re.IGNORECASE,
    )

    def apply(self, finding: Dict[str, Any]) -> Optional[FilterDecision]:
        text = self._collect_text(
            finding,
            [
                "code_snippet",
                "description",
                "message",
                "data_flow",
                "sink",
                "source",
                "name",
            ],
        )
        if not text:
            return None

        if self._PARAM_QUERY_RE.search(text):
            return self._decision(
                FilterResult.FILTER,
                0.92,
                "检测到参数化查询模式",
                self.name,
            )

        if self._ORM_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.74,
                "检测到ORM调用，建议人工复核",
                self.name,
            )

        if self._SANITIZE_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.78,
                "检测到净化或转义处理",
                self.name,
            )

        return None


class ContextFilter(BaseFilter):
    name = "context"

    _TYPE_CHECK_RE = re.compile(
        r"\b(isinstance\s*\(|type\s*\([^\)]*\)\s*(==|is)|"
        r"typing\.cast\(|assert\s+isinstance\s*\()",
        re.IGNORECASE,
    )
    _LENGTH_CHECK_RE = re.compile(
        r"\blen\s*\([^\)]*\)\s*(<=|>=|<|>|==)\s*\d+|"
        r"\b(min|max)_length\b|\bsize\s*(<=|>=|<|>)\s*\d+",
        re.IGNORECASE,
    )
    _REGEX_CHECK_RE = re.compile(
        r"\b(re\.(match|search|fullmatch|compile)\s*\(|regex\.|"
        r"pattern\s*=\s*r['\"])",
        re.IGNORECASE,
    )

    def apply(self, finding: Dict[str, Any]) -> Optional[FilterDecision]:
        text = self._collect_text(
            finding,
            ["code_snippet", "description", "message", "context", "validation"],
        )
        if not text:
            return None

        if self._TYPE_CHECK_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.66,
                "检测到类型校验保护",
                self.name,
            )

        if self._LENGTH_CHECK_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.69,
                "检测到长度边界校验",
                self.name,
            )

        if self._REGEX_CHECK_RE.search(text):
            return self._decision(
                FilterResult.REVIEW,
                0.72,
                "检测到正则表达式校验",
                self.name,
            )

        return None


@dataclass
class FalsePositiveFilter:
    filters: List[BaseFilter] = field(
        default_factory=lambda: [
            WhitelistFilter(),
            DataFlowFilter(),
            ContextFilter(),
        ]
    )
    _stats: Dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self._stats = {
            "total": 0,
            "pass": 0,
            "filter": 0,
            "review": 0,
            "by_filter": {},
        }

    @staticmethod
    def _rank(result: FilterResult) -> int:
        order = {
            FilterResult.PASS: 0,
            FilterResult.REVIEW: 1,
            FilterResult.FILTER: 2,
        }
        return order[result]

    def filter_finding(self, finding: Dict[str, Any]) -> FilterDecision:
        decisions: List[FilterDecision] = []
        for item in self.filters:
            decision = item.apply(finding)
            if decision is not None:
                decisions.append(decision)

        if not decisions:
            final = FilterDecision(
                result=FilterResult.PASS,
                confidence=0.0,
                reason="未命中过滤规则",
                filter_name="none",
            )
        else:
            final = sorted(
                decisions,
                key=lambda value: (self._rank(value.result), value.confidence),
                reverse=True,
            )[0]

        self._stats["total"] += 1
        self._stats[final.result.value] += 1
        by_filter = self._stats["by_filter"]
        by_filter[final.filter_name] = by_filter.get(final.filter_name, 0) + 1
        return final

    def filter_findings(
        self,
        findings: Iterable[Dict[str, Any]],
        include_filtered: bool = False,
    ) -> List[Dict[str, Any]]:
        output: List[Dict[str, Any]] = []
        for finding in findings:
            decision = self.filter_finding(finding)
            enriched = dict(finding)
            enriched["filter_result"] = decision.result.value
            enriched["filter_confidence"] = decision.confidence
            enriched["filter_reason"] = decision.reason
            enriched["filter_name"] = decision.filter_name

            if include_filtered or decision.result != FilterResult.FILTER:
                output.append(enriched)

        return output

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total": self._stats["total"],
            "pass": self._stats["pass"],
            "filter": self._stats["filter"],
            "review": self._stats["review"],
            "by_filter": dict(self._stats["by_filter"]),
        }


def _demo_findings() -> List[Dict[str, Any]]:
    return [
        {
            "rule_id": "sql-injection-python",
            "file_path": "tests/test_sql.py",
            "line_number": 18,
            "code_snippet": "def test_query():\n    cursor.execute('select * from t where id=%s', (uid,))",
            "description": "动态SQL拼接风险",
        },
        {
            "rule_id": "xss-python",
            "file_path": "app/views.py",
            "line_number": 42,
            "code_snippet": "output = html.escape(user_input)",
            "description": "模板输出可能引起XSS",
        },
        {
            "rule_id": "path-traversal-python",
            "file_path": "app/files.py",
            "line_number": 73,
            "code_snippet": "if not re.fullmatch(r'[a-z0-9_\\-]+', name):\n    raise ValueError('invalid')",
            "description": "文件路径校验",
        },
        {
            "rule_id": "command-exec-python",
            "file_path": "app/runner.py",
            "line_number": 10,
            "code_snippet": "os.system(cmd)",
            "description": "命令执行风险",
        },
    ]


def _print_result(path: str, decision: FilterDecision, kept: bool) -> None:
    state = "保留" if kept else "已过滤"
    print(
        f"[{state}] {path} -> {decision.result.value} | "
        f"{decision.filter_name} | {decision.confidence:.2f} | {decision.reason}"
    )


def main() -> int:
    findings = _demo_findings()
    engine = FalsePositiveFilter()

    print("=== 误报过滤演示 ===")
    all_items = engine.filter_findings(findings, include_filtered=True)

    for item in all_items:
        decision = FilterDecision(
            result=FilterResult(item["filter_result"]),
            confidence=float(item["filter_confidence"]),
            reason=str(item["filter_reason"]),
            filter_name=str(item["filter_name"]),
        )
        _print_result(
            item.get("file_path", ""),
            decision,
            decision.result != FilterResult.FILTER,
        )

    print("\n=== 统计信息 ===")
    stats = engine.get_stats()
    print(f"总处理: {stats['total']}")
    print(f"通过: {stats['pass']}")
    print(f"过滤: {stats['filter']}")
    print(f"复核: {stats['review']}")
    print(f"按过滤器分布: {stats['by_filter']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
