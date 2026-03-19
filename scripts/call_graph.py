#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class FunctionCall:
    caller: str
    callee: str
    line_number: int
    file_path: str
    args: List[str] = field(default_factory=list)


@dataclass
class FunctionNode:
    name: str
    file_path: str = ""
    line_number: int = 0
    calls: List[FunctionCall] = field(default_factory=list)
    called_by: List[FunctionCall] = field(default_factory=list)


class CallGraphBuilder:
    def __init__(self) -> None:
        self.functions: Dict[str, FunctionNode] = {}

    def add_function(
        self,
        function_name: str,
        file_path: str = "",
        line_number: int = 0,
    ) -> FunctionNode:
        node = self.functions.get(function_name)
        if node is None:
            node = FunctionNode(
                name=function_name,
                file_path=file_path,
                line_number=line_number,
            )
            self.functions[function_name] = node
            return node

        if file_path and not node.file_path:
            node.file_path = file_path
        if line_number and not node.line_number:
            node.line_number = line_number
        return node

    def add_call(
        self,
        caller: str,
        callee: str,
        line_number: int,
        file_path: str,
        args: List[str] | None = None,
    ) -> FunctionCall:
        caller_node = self.add_function(caller)
        callee_node = self.add_function(callee)
        call = FunctionCall(
            caller=caller,
            callee=callee,
            line_number=line_number,
            file_path=file_path,
            args=args or [],
        )
        caller_node.calls.append(call)
        callee_node.called_by.append(call)
        return call

    def find_paths(
        self,
        source: str,
        target: str,
        max_depth: int = 20,
    ) -> List[List[str]]:
        if source not in self.functions or target not in self.functions:
            return []

        paths: List[List[str]] = []

        def dfs(current: str, path: List[str], visited: Set[str]) -> None:
            if len(path) > max_depth:
                return
            if current == target:
                paths.append(path.copy())
                return

            node = self.functions[current]
            for call in node.calls:
                next_name = call.callee
                if next_name in visited:
                    continue
                visited.add(next_name)
                path.append(next_name)
                dfs(next_name, path, visited)
                path.pop()
                visited.remove(next_name)

        dfs(source, [source], {source})
        return paths

    def get_callers(self, function_name: str) -> List[str]:
        if function_name not in self.functions:
            return []

        result: Set[str] = set()
        stack = [function_name]
        seen: Set[str] = set()

        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)

            for call in self.functions[current].called_by:
                if call.caller not in result:
                    result.add(call.caller)
                    stack.append(call.caller)

        return sorted(result)

    def get_callees(self, function_name: str) -> List[str]:
        if function_name not in self.functions:
            return []

        result: Set[str] = set()
        stack = [function_name]
        seen: Set[str] = set()

        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)

            for call in self.functions[current].calls:
                if call.callee not in result:
                    result.add(call.callee)
                    stack.append(call.callee)

        return sorted(result)

    def get_statistics(self) -> Dict[str, int]:
        total_functions = len(self.functions)
        total_calls = sum(len(node.calls) for node in self.functions.values())
        isolated = 0
        roots = 0
        leafs = 0

        for node in self.functions.values():
            has_in = bool(node.called_by)
            has_out = bool(node.calls)
            if not has_in and not has_out:
                isolated += 1
            if not has_in:
                roots += 1
            if not has_out:
                leafs += 1

        return {
            "total_functions": total_functions,
            "total_calls": total_calls,
            "isolated_functions": isolated,
            "root_functions": roots,
            "leaf_functions": leafs,
        }

    def print_graph(self) -> None:
        print("=== 调用图 ===")
        for name in sorted(self.functions):
            node = self.functions[name]
            location = ""
            if node.file_path:
                location = f" ({node.file_path}:{node.line_number})"
            print(f"- {name}{location}")

            outgoing = [f"{call.callee}@{call.line_number}" for call in node.calls]
            incoming = [f"{call.caller}@{call.line_number}" for call in node.called_by]

            print(f"  calls: {', '.join(outgoing) if outgoing else '-'}")
            print(f"  called_by: {', '.join(incoming) if incoming else '-'}")


def _build_demo_graph() -> CallGraphBuilder:
    graph = CallGraphBuilder()
    graph.add_function("handle_request", "app.py", 10)
    graph.add_function("validate_token", "auth.py", 5)
    graph.add_function("load_user", "user.py", 12)
    graph.add_function("query_db", "db.py", 20)
    graph.add_function("audit_log", "audit.py", 8)

    graph.add_call("handle_request", "validate_token", 12, "app.py", ["token"])
    graph.add_call("handle_request", "load_user", 13, "app.py", ["user_id"])
    graph.add_call("load_user", "query_db", 16, "user.py", ["SELECT ..."])
    graph.add_call("handle_request", "audit_log", 14, "app.py", ["event"])
    graph.add_call("validate_token", "audit_log", 9, "auth.py", ["auth_check"])
    return graph


if __name__ == "__main__":
    demo = _build_demo_graph()
    demo.print_graph()

    print("\n=== Statistics ===")
    for key, value in demo.get_statistics().items():
        print(f"{key}: {value}")

    print("\n=== Query Demo ===")
    print("callers(audit_log):", demo.get_callers("audit_log"))
    print("callees(handle_request):", demo.get_callees("handle_request"))
    print("paths(handle_request -> query_db):", demo.find_paths("handle_request", "query_db"))
