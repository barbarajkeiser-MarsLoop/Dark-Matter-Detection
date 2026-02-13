#!/usr/bin/env python3
"""
zombie_orbits.py - Detect code that runs but produces nothing useful

Part of Dark Matter Detection framework  
Finds: High-cost execution with zero benefit
Why it matters: Computational waste disguised as productive code
"""

import ast
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class ZombieType(Enum):
    """Types of zombie orbit patterns"""
    DISCARDED_CALL = "discarded_call"
    UNUSED_COMPUTATION = "unused_computation"
    EMPTY_LOOP = "empty_loop"
    NO_RETURN_FUNCTION = "no_return_function"
    WRITE_ONLY_VARIABLE = "write_only_variable"


@dataclass
class ZombieOrbit:
    """Detected zombie code instance"""
    line: int
    zombie_type: ZombieType
    code_snippet: str
    severity: str
    description: str
    context: str


class ZombieOrbitDetector(ast.NodeVisitor):
    """Detects zombie orbits - code that executes but contributes nothing"""
    
    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.zombies: List[ZombieOrbit] = []
        self.current_context = "module"
        self.assigned_vars = set()
        self.used_vars = set()
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_context = self.current_context
        self.current_context = f"function:{node.name}"
        
        # Check if function never returns anything useful
        has_return = self._has_meaningful_return(node)
        has_side_effects = self._has_side_effects(node)
        
        if not has_return and not has_side_effects:
            self.zombies.append(ZombieOrbit(
                line=node.lineno,
                zombie_type=ZombieType.NO_RETURN_FUNCTION,
                code_snippet=self._get_code_snippet(node.lineno),
                severity="MEDIUM",
                description=f"Function '{node.name}' runs but produces no output or side effects",
                context=self.current_context
            ))
        
        self.generic_visit(node)
        self.current_context = old_context
    
    def visit_Expr(self, node: ast.Expr):
        """Detect standalone expressions (discarded values)"""
        if isinstance(node.value, ast.Call):
            func_name = self._get_call_name(node.value)
            
            # Filter out known side-effect functions
            if func_name and not self._is_side_effect_function(func_name):
                self.zombies.append(ZombieOrbit(
                    line=node.lineno,
                    zombie_type=ZombieType.DISCARDED_CALL,
                    code_snippet=self._get_code_snippet(node.lineno),
                    severity="HIGH",
                    description=f"Function call '{func_name}()' result discarded",
                    context=self.current_context
                ))
        
        # Detect expensive computations that are discarded
        if isinstance(node.value, ast.BinOp):
            self.zombies.append(ZombieOrbit(
                line=node.lineno,
                zombie_type=ZombieType.UNUSED_COMPUTATION,
                code_snippet=self._get_code_snippet(node.lineno),
                severity="MEDIUM",
                description="Computation result discarded (not assigned or returned)",
                context=self.current_context
            ))
        
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For):
        """Detect empty or no-op loops"""
        if self._is_empty_loop(node.body):
            self.zombies.append(ZombieOrbit(
                line=node.lineno,
                zombie_type=ZombieType.EMPTY_LOOP,
                code_snippet=self._get_code_snippet(node.lineno),
                severity="HIGH",
                description="Loop executes but body is empty or no-op",
                context=self.current_context
            ))
        
        self.generic_visit(node)
    
    def visit_While(self, node: ast.While):
        """Detect empty while loops"""
        if self._is_empty_loop(node.body):
            self.zombies.append(ZombieOrbit(
                line=node.lineno,
                zombie_type=ZombieType.EMPTY_LOOP,
                code_snippet=self._get_code_snippet(node.lineno),
                severity="HIGH",
                description="Loop executes but body is empty or no-op",
                context=self.current_context
            ))
        
        self.generic_visit(node)
    
    def _has_meaningful_return(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has meaningful return statements"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return):
                if node.value is not None:
                    # Has a return with value
                    return True
        return False
    
    def _has_side_effects(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has observable side effects"""
        # Simple heuristics for side effects
        for node in ast.walk(func_node):
            # Calls to print, logging, file operations, etc.
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name in ('print', 'log', 'write', 'append', 'update', 'delete'):
                    return True
            
            # Attribute assignments (modifying objects)
            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
                return True
        
        return False
    
    def _get_call_name(self, call: ast.Call) -> Optional[str]:
        """Extract function name from call node"""
        if isinstance(call.func, ast.Name):
            return call.func.id
        if isinstance(call.func, ast.Attribute):
            return call.func.attr
        return None
    
    def _is_side_effect_function(self, name: str) -> bool:
        """Check if function is known to have side effects"""
        side_effect_funcs = {
            'print', 'log', 'write', 'send', 'publish',
            'append', 'update', 'delete', 'remove', 'save',
            'close', 'flush', 'commit', 'rollback'
        }
        return name.lower() in side_effect_funcs
    
    def _is_empty_loop(self, body: List[ast.stmt]) -> bool:
        """Check if loop body is empty or contains only pass/continue"""
        if not body:
            return True
        
        # All statements are pass or continue
        for stmt in body:
            if not isinstance(stmt, (ast.Pass, ast.Continue)):
                return False
        
        return True
    
    def _get_code_snippet(self, line: int) -> str:
        start = max(0, line - 2)
        end = min(len(self.source_lines), line + 2)
        return "\n".join(self.source_lines[start:end])


def detect_zombie_orbits(source_code: str) -> List[ZombieOrbit]:
    try:
        tree = ast.parse(source_code)
        source_lines = source_code.split('\n')
        detector = ZombieOrbitDetector(source_lines)
        detector.visit(tree)
        return detector.zombies
    except SyntaxError:
        return []


def calculate_zombie_score(zombies: List[ZombieOrbit]) -> float:
    if not zombies:
        return 0.0
    
    weights = {"HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}
    total = sum(weights.get(z.severity, 1.0) for z in zombies)
    return min(10.0, total)
