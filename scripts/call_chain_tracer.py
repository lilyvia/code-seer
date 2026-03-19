#!/usr/bin/env python3
"""调用链追踪器：整合污点追踪与调用图。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from call_graph import CallGraphBuilder, FunctionNode
    from taint_tracker import TaintStatus, TaintTracker
except ImportError:
    from .call_graph import CallGraphBuilder, FunctionNode
    from .taint_tracker import TaintStatus, TaintTracker


@dataclass
class CallChainNode:
    function_name: str
    file_path: str
    line_number: int
    code_snippet: str
    is_source: bool
    is_sink: bool
    taint_status: str


@dataclass
class CallChain:
    source: CallChainNode
    intermediate: List[CallChainNode] = field(default_factory=list)
    sink: Optional[CallChainNode] = None
    vulnerability_type: str = "unknown"
    severity: str = "低危"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vulnerability_type": self.vulnerability_type,
            "severity": self.severity,
            "source": self.source.__dict__,
            "intermediate": [node.__dict__ for node in self.intermediate],
            "sink": self.sink.__dict__ if self.sink else None,
        }

    def format_ascii(self) -> str:
        lines: List[str] = []
        lines.append(f"调用链类型: {self.vulnerability_type} | 风险等级: {self.severity}")
        lines.append("+-- 漏洞入口")
        lines.append(
            f"|   {self.source.function_name} ({self.source.file_path}:{self.source.line_number})"
        )
        lines.append(f"|   代码: {self.source.code_snippet}")
        lines.append(f"|   污点状态: {self.source.taint_status}")

        if self.intermediate:
            lines.append("+-- 中间调用")
            for node in self.intermediate:
                lines.append(
                    f"|   --> {node.function_name} ({node.file_path}:{node.line_number})"
                )
                lines.append(f"|       代码: {node.code_snippet}")
                lines.append(f"|       污点状态: {node.taint_status}")

        if self.sink:
            lines.append("+-- 危险汇点")
            lines.append(
                f"    {self.sink.function_name} ({self.sink.file_path}:{self.sink.line_number})"
            )
            lines.append(f"    代码: {self.sink.code_snippet}")
            lines.append(f"    污点状态: {self.sink.taint_status}")

        return "\n".join(lines)


class CallChainTracer:

    def __init__(self, taint_tracker: TaintTracker, call_graph_builder: CallGraphBuilder) -> None:
        self.taint_tracker = taint_tracker
        self.call_graph_builder = call_graph_builder
        self.chains: List[CallChain] = []

    def trace_chains(self) -> List[CallChain]:
        self.chains = []
        for variable_name, variable in self.taint_tracker.variables.items():
            if variable.status != TaintStatus.TAINTED:
                continue
            if not self._is_terminal_variable(variable_name):
                continue
            self.chains.extend(self._trace_variable_chain(variable_name))
        return self.chains

    def _trace_variable_chain(self, variable_name: str) -> List[CallChain]:
        sink_candidates = self._find_sink_for_variable(variable_name)
        if not sink_candidates:
            return []

        propagation_path = self.taint_tracker.get_propagation_path(variable_name)
        status = self.taint_tracker.variables[variable_name].status.value

        source_function = self._choose_source_function(propagation_path)
        source_node = self._make_node(
            function_name=source_function,
            file_path=self._get_function_file(source_function),
            line_number=self._get_function_line(source_function),
            code_snippet=f"{source_function}(...{propagation_path[0]}...)",
            is_source=True,
            is_sink=False,
            taint_status=status,
        )

        chains: List[CallChain] = []
        for sink_name, vulnerability_type in sink_candidates:
            sink_function = self._choose_sink_function(sink_name)
            sink_node = self._make_node(
                function_name=sink_function,
                file_path=self._get_function_file(sink_function),
                line_number=self._get_function_line(sink_function),
                code_snippet=f"{sink_name}({variable_name})",
                is_source=False,
                is_sink=True,
                taint_status=status,
            )

            intermediate = self._build_intermediate_nodes(source_function, sink_function, status)
            chains.append(
                CallChain(
                    source=source_node,
                    intermediate=intermediate,
                    sink=sink_node,
                    vulnerability_type=vulnerability_type,
                    severity=self._get_severity(vulnerability_type),
                )
            )

        return chains

    def _find_sink_for_variable(self, variable_name: str) -> List[tuple[str, str]]:
        sink_hits: List[tuple[str, str]] = []
        for sink in self.taint_tracker.COMMON_SINKS.values():
            result = self.taint_tracker.check_sink(variable_name, sink.name)
            if result.is_vulnerable:
                sink_hits.append((sink.name, sink.category))
        return sink_hits

    def _get_severity(self, vulnerability_type: str) -> str:
        mapping = {
            "sql_execution": "严重",
            "command_execution": "严重",
            "dom_xss": "高危",
            "deserialization": "高危",
            "path_traversal": "高危",
            "ssrf": "中危",
            "auth_defect": "中危",
            "hardcoded_secret": "中危",
            "custom": "低危",
            "unknown": "低危",
        }
        return mapping.get(vulnerability_type, "低危")

    def get_chains_by_severity(self, severity: str) -> List[CallChain]:
        return [chain for chain in self.chains if chain.severity == severity]

    def get_chains_by_type(self, vulnerability_type: str) -> List[CallChain]:
        return [chain for chain in self.chains if chain.vulnerability_type == vulnerability_type]

    def print_chains(self) -> None:
        if not self.chains:
            print("未发现可追踪调用链")
            return

        print("=== 调用链追踪结果 ===")
        for index, chain in enumerate(self.chains, 1):
            print(f"\n[{index}] {chain.vulnerability_type} ({chain.severity})")
            print(chain.format_ascii())

    def _build_intermediate_nodes(
        self,
        source_function: str,
        sink_function: str,
        taint_status: str,
    ) -> List[CallChainNode]:
        paths = self.call_graph_builder.find_paths(source_function, sink_function)
        if not paths:
            return []

        path = paths[0]
        if len(path) <= 2:
            return []

        nodes: List[CallChainNode] = []
        for function_name in path[1:-1]:
            nodes.append(
                self._make_node(
                    function_name=function_name,
                    file_path=self._get_function_file(function_name),
                    line_number=self._get_function_line(function_name),
                    code_snippet=f"{function_name}(...)",
                    is_source=False,
                    is_sink=False,
                    taint_status=taint_status,
                )
            )
        return nodes

    def _choose_source_function(self, propagation_path: List[str]) -> str:
        if not self.call_graph_builder.functions:
            return propagation_path[0] if propagation_path else "unknown_source"

        for name in propagation_path:
            if name in self.call_graph_builder.functions:
                return name

        root_candidates = [
            name
            for name, node in self.call_graph_builder.functions.items()
            if not node.called_by
        ]
        if root_candidates:
            return sorted(root_candidates)[0]
        return sorted(self.call_graph_builder.functions)[0]

    def _choose_sink_function(self, sink_name: str) -> str:
        if not self.call_graph_builder.functions:
            return sink_name

        sink_parts = [part for part in sink_name.replace(".", "_").split("_") if part]
        for function_name in self.call_graph_builder.functions:
            lower_name = function_name.lower()
            if any(part.lower() in lower_name for part in sink_parts):
                return function_name

        leaf_candidates = [
            name
            for name, node in self.call_graph_builder.functions.items()
            if not node.calls
        ]
        if leaf_candidates:
            return sorted(leaf_candidates)[0]
        return sorted(self.call_graph_builder.functions)[-1]

    def _get_function_node(self, function_name: str) -> Optional[FunctionNode]:
        return self.call_graph_builder.functions.get(function_name)

    def _get_function_file(self, function_name: str) -> str:
        node = self._get_function_node(function_name)
        if not node or not node.file_path:
            return "unknown"
        return node.file_path

    def _get_function_line(self, function_name: str) -> int:
        node = self._get_function_node(function_name)
        if not node:
            return 0
        return node.line_number

    def _make_node(
        self,
        function_name: str,
        file_path: str,
        line_number: int,
        code_snippet: str,
        is_source: bool,
        is_sink: bool,
        taint_status: str,
    ) -> CallChainNode:
        return CallChainNode(
            function_name=function_name,
            file_path=file_path,
            line_number=line_number,
            code_snippet=code_snippet,
            is_source=is_source,
            is_sink=is_sink,
            taint_status=taint_status,
        )

    def _is_terminal_variable(self, variable_name: str) -> bool:
        children = self.taint_tracker.edges.get(variable_name)
        return not children


def _build_demo_tracer() -> CallChainTracer:
    taint_tracker = TaintTracker()
    taint_tracker.track_source("user_input", "request.getParameter")
    taint_tracker.propagate_taint("user_input", "raw_query")
    taint_tracker.propagate_taint("raw_query", "sql_payload")

    graph = CallGraphBuilder()
    graph.add_function("handle_request", "app.py", 10)
    graph.add_function("prepare_query", "service.py", 22)
    graph.add_function("query_db", "db.py", 38)
    graph.add_call("handle_request", "prepare_query", 14, "app.py")
    graph.add_call("prepare_query", "query_db", 27, "service.py")

    return CallChainTracer(taint_tracker=taint_tracker, call_graph_builder=graph)


if __name__ == "__main__":
    tracer = _build_demo_tracer()
    tracer.trace_chains()
    tracer.print_chains()
