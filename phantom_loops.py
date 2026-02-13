#!/usr/bin/env python3
"""
phantom_loops.py - Detect loops claiming infinity but exiting immediately

Part of Dark Matter Detection framework
Finds: while True / infinite for loops that break/return on first iteration
Why it matters: False claims of persistence shape expectations incorrectly
"""

import ast
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class PhantomType(Enum):
    """Types of phantom loop patterns"""
    WHILE_TRUE_BREAK = "while_true_break"
    WHILE_TRUE_RETURN = "while_true_return"
    WHILE_TRUE_RAISE = "while_true_raise"
    INFINITE_ITERATOR_EXIT = "infinite_iterator_exit"


@dataclass
class PhantomLoop:
    """Detected phantom loop instance"""
    line: int
    phantom_type: PhantomType
    code_snippet: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    exit_mechanism: str
    context: str


class PhantomLoopDetector(ast.NodeVisitor):
    """Detects phantom loops - syntactically infinite but actually immediate exits"""
    
    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.phantoms: List[PhantomLoop] = []
        self.current_context = "module"
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_context = self.current_context
        self.current_context = f"function:{node.name}"
        self.generic_visit(node)
        self.current_context = old_context
    
    def visit_While(self, node: ast.While):
        if self._is_infinite_condition(node.test):
            exit_info = self._check_immediate_exit(node.body)
            
            if exit_info:
                phantom_type, exit_mechanism = exit_info
                severity = self._calculate_severity(phantom_type)
                
                self.phantoms.append(PhantomLoop(
                    line=node.lineno,
                    phantom_type=phantom_type,
                    code_snippet=self._get_code_snippet(node.lineno),
                    severity=severity,
                    description=f"Loop claims infinity but {exit_mechanism} immediately",
                    exit_mechanism=exit_mechanism,
                    context=self.current_context
                ))
        
        self.generic_visit(node)
    
    def _is_infinite_condition(self, test: ast.expr) -> bool:
        if isinstance(test, ast.Constant) and test.value is True:
            return True
        return False
    
    def _check_immediate_exit(self, body: List[ast.stmt]) -> Optional[tuple]:
        if not body:
            return None
        
        first_stmt = body[0]
        
        if isinstance(first_stmt, ast.Break):
            return (PhantomType.WHILE_TRUE_BREAK, "breaks")
        if isinstance(first_stmt, ast.Return):
            return (PhantomType.WHILE_TRUE_RETURN, "returns")
        if isinstance(first_stmt, ast.Raise):
            return (PhantomType.WHILE_TRUE_RAISE, "raises")
        
        return None
    
    def _calculate_severity(self, phantom_type: PhantomType) -> str:
        if phantom_type == PhantomType.WHILE_TRUE_BREAK:
            return "HIGH"
        return "MEDIUM"
    
    def _get_code_snippet(self, line: int) -> str:
        start = max(0, line - 2)
        end = min(len(self.source_lines), line + 2)
        return "\n".join(self.source_lines[start:end])


def detect_phantom_loops(source_code: str) -> List[PhantomLoop]:
    try:
        tree = ast.parse(source_code)
        source_lines = source_code.split('\n')
        detector = PhantomLoopDetector(source_lines)
        detector.visit(tree)
        return detector.phantoms
    except SyntaxError:
        return []


def calculate_phantom_score(phantoms: List[PhantomLoop]) -> float:
    if not phantoms:
        return 0.0
    
    weights = {"HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}
    total = sum(weights.get(p.severity, 1.0) for p in phantoms)
    return min(10.0, total)
