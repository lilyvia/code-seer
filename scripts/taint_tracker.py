#!/usr/bin/env python3
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class TaintStatus(Enum):
    CLEAN = "clean"
    TAINTED = "tainted"
    SANITIZED = "sanitized"


@dataclass(frozen=True)
class TaintSource:
    name: str
    category: str
    description: str


@dataclass(frozen=True)
class TaintSink:
    name: str
    category: str
    description: str


@dataclass(frozen=True)
class Sanitizer:
    name: str
    category: str
    description: str


@dataclass
class TaintVariable:
    name: str
    status: TaintStatus = TaintStatus.CLEAN
    source: Optional[TaintSource] = None
    sanitized_by: Optional[Sanitizer] = None
    parents: Set[str] = field(default_factory=set)


@dataclass
class SinkCheckResult:
    sink: TaintSink
    variable: str
    status: TaintStatus
    is_vulnerable: bool
    propagation_path: List[str]


class TaintTracker:
    COMMON_SOURCES: Dict[str, TaintSource] = {
        "request.getParameter": TaintSource(
            name="request.getParameter",
            category="user_input",
            description="HTTP请求参数",
        ),
        "file.read": TaintSource(
            name="file.read",
            category="file_input",
            description="文件读取内容",
        ),
    }

    COMMON_SINKS: Dict[str, TaintSink] = {
        "cursor.execute": TaintSink(
            name="cursor.execute",
            category="sql_execution",
            description="SQL执行接口",
        ),
        "os.system": TaintSink(
            name="os.system",
            category="command_execution",
            description="系统命令执行",
        ),
        "innerHTML": TaintSink(
            name="innerHTML",
            category="dom_xss",
            description="DOM HTML注入点",
        ),
    }

    COMMON_SANITIZERS: Dict[str, Sanitizer] = {
        "htmlspecialchars": Sanitizer(
            name="htmlspecialchars",
            category="xss_sanitization",
            description="HTML特殊字符转义",
        ),
        "parameterized_query": Sanitizer(
            name="parameterized_query",
            category="sql_sanitization",
            description="参数化查询",
        ),
        "parameterized queries": Sanitizer(
            name="parameterized queries",
            category="sql_sanitization",
            description="参数化查询",
        ),
    }

    def __init__(self) -> None:
        self.variables: Dict[str, TaintVariable] = {}
        self.edges: Dict[str, Set[str]] = {}

    def _ensure_variable(self, variable_name: str) -> TaintVariable:
        if variable_name not in self.variables:
            self.variables[variable_name] = TaintVariable(name=variable_name)
        return self.variables[variable_name]

    def track_source(self, variable_name: str, source_name: str) -> TaintVariable:
        source = self.COMMON_SOURCES.get(
            source_name,
            TaintSource(
                name=source_name,
                category="custom",
                description="自定义污点源",
            ),
        )
        variable = self._ensure_variable(variable_name)
        variable.status = TaintStatus.TAINTED
        variable.source = source
        variable.sanitized_by = None
        return variable

    def propagate_taint(self, from_var: str, to_var: str) -> TaintVariable:
        source_var = self._ensure_variable(from_var)
        target_var = self._ensure_variable(to_var)

        if from_var not in self.edges:
            self.edges[from_var] = set()
        self.edges[from_var].add(to_var)
        target_var.parents.add(from_var)

        if source_var.status == TaintStatus.TAINTED:
            target_var.status = TaintStatus.TAINTED
            target_var.source = source_var.source
            target_var.sanitized_by = None

        return target_var

    def sanitize_variable(self, variable_name: str, sanitizer_name: str) -> TaintVariable:
        sanitizer = self.COMMON_SANITIZERS.get(
            sanitizer_name,
            Sanitizer(
                name=sanitizer_name,
                category="custom",
                description="自定义净化器",
            ),
        )
        variable = self._ensure_variable(variable_name)
        variable.status = TaintStatus.SANITIZED
        variable.sanitized_by = sanitizer
        return variable

    def is_tainted(self, variable_name: str) -> bool:
        variable = self.variables.get(variable_name)
        return bool(variable and variable.status == TaintStatus.TAINTED)

    def check_sink(self, variable_name: str, sink_name: str) -> SinkCheckResult:
        sink = self.COMMON_SINKS.get(
            sink_name,
            TaintSink(
                name=sink_name,
                category="custom",
                description="自定义危险汇点",
            ),
        )

        variable = self._ensure_variable(variable_name)
        is_vulnerable = variable.status == TaintStatus.TAINTED

        return SinkCheckResult(
            sink=sink,
            variable=variable_name,
            status=variable.status,
            is_vulnerable=is_vulnerable,
            propagation_path=self.get_propagation_path(variable_name),
        )

    def get_propagation_path(self, variable_name: str) -> List[str]:
        self._ensure_variable(variable_name)

        path: List[str] = []
        visited: Set[str] = set()

        def dfs(current: str) -> None:
            if current in visited:
                return
            visited.add(current)

            parents = sorted(self.variables[current].parents)
            if not parents:
                path.append(current)
                return

            for parent in parents:
                dfs(parent)
            path.append(current)

        dfs(variable_name)

        ordered_path: List[str] = []
        seen: Set[str] = set()
        for name in path:
            if name not in seen:
                seen.add(name)
                ordered_path.append(name)
        return ordered_path


def _demo() -> None:
    tracker = TaintTracker()

    tracker.track_source("user_input", "request.getParameter")
    tracker.propagate_taint("user_input", "raw_query")
    tracker.propagate_taint("raw_query", "sql")

    sql_result = tracker.check_sink("sql", "cursor.execute")

    tracker.propagate_taint("user_input", "html_fragment")
    tracker.sanitize_variable("html_fragment", "htmlspecialchars")
    xss_result = tracker.check_sink("html_fragment", "innerHTML")

    tracker.track_source("file_payload", "file.read")
    tracker.propagate_taint("file_payload", "shell_cmd")
    cmd_result = tracker.check_sink("shell_cmd", "os.system")

    print("=== 污点追踪演示 ===")
    print(f"SQL汇点是否存在风险: {sql_result.is_vulnerable}")
    print(f"SQL传播链: {' -> '.join(sql_result.propagation_path)}")
    print(f"XSS汇点是否存在风险: {xss_result.is_vulnerable}")
    print(f"XSS传播链: {' -> '.join(xss_result.propagation_path)}")
    print(f"命令执行汇点是否存在风险: {cmd_result.is_vulnerable}")
    print(f"命令执行传播链: {' -> '.join(cmd_result.propagation_path)}")


if __name__ == "__main__":
    _demo()
