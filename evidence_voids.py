#!/usr/bin/env python3
"""
evidence_voids.py - Detect gaps in observability and monitoring

Part of Dark Matter Detection framework
Finds: Missing logging, swallowed exceptions, ignored errors
Why it matters: What you can't observe, you can't debug or improve
"""

import ast
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class VoidType(Enum):
    """Types of evidence void patterns"""
    SWALLOWED_EXCEPTION = "swallowed_exception"
    BARE_EXCEPT = "bare_except"
    IGNORED_RETURN = "ignored_return"
    NO_LOGGING_IN_EXCEPT = "no_logging_in_except"
    SILENT_FAILURE = "silent_failure"


@dataclass
class EvidenceVoid:
    """Detected evidence void instance"""
    line: int
    void_type: VoidType
    code_snippet: str
    severity: str
    description: str
    context: str


class EvidenceVoidDetector(ast.NodeVisitor):
    """Detects evidence voids - missing observability in code"""
    
    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.voids: List[EvidenceVoid] = []
        self.current_context = "module"
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_context = self.current_context
        self.current_context = f"function:{node.name}"
        self.generic_visit(node)
        self.current_context = old_context
    
    def visit_Try(self, node: ast.Try):
        """Detect problematic exception handling"""
        for handler in node.handlers:
            # Bare except (catches everything)
            if handler.type is None:
                self.voids.append(EvidenceVoid(
                    line=handler.lineno,
                    void_type=VoidType.BARE_EXCEPT,
                    code_snippet=self._get_code_snippet(handler.lineno),
                    severity="HIGH",
                    description="Bare except clause catches all exceptions indiscriminately",
                    context=self.current_context
                ))
            
            # Swallowed exception (except: pass)
            if self._is_swallowed(handler.body):
                self.voids.append(EvidenceVoid(
                    line=handler.lineno,
                    void_type=VoidType.SWALLOWED_EXCEPTION,
                    code_snippet=self._get_code_snippet(handler.lineno),
                    severity="HIGH",
                    description="Exception caught but ignored (no logging, no re-raise)",
                    context=self.current_context
                ))
            
            # No logging in except block
            if not self._has_logging(handler.body):
                self.voids.append(EvidenceVoid(
                    line=handler.lineno,
                    void_type=VoidType.NO_LOGGING_IN_EXCEPT,
                    code_snippet=self._get_code_snippet(handler.lineno),
                    severity="MEDIUM",
                    description="Exception handler lacks logging (error invisible)",
                    context=self.current_context
                ))
        
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call):
        """Detect calls to fallible functions without error checking"""
        # This is approximate - would need type info for accuracy
        func_name = self._get_call_name(node)
        
        # Known fallible operations
        fallible = {'open', 'urlopen', 'connect', 'request', 'load', 'parse'}
        
        if func_name in fallible:
            # Check if call is wrapped in try/except or result is checked
            if not self._is_error_checked(node):
                self.voids.append(EvidenceVoid(
                    line=node.lineno,
                    void_type=VoidType.SILENT_FAILURE,
                    code_snippet=self._get_code_snippet(node.lineno),
                    severity="MEDIUM",
                    description=f"Fallible operation '{func_name}()' lacks error handling",
                    context=self.current_context
                ))
        
        self.generic_visit(node)
    
    def _is_swallowed(self, body: List[ast.stmt]) -> bool:
        """Check if exception handler just swallows (pass or minimal handling)"""
        if not body:
            return True
        
        # Only pass statement
        if len(body) == 1 and isinstance(body[0], ast.Pass):
            return True
        
        # Only continue or break
        if len(body) == 1 and isinstance(body[0], (ast.Continue, ast.Break)):
            return True
        
        return False
    
    def _has_logging(self, body: List[ast.stmt]) -> bool:
        """Check if code block contains logging calls"""
        for node in ast.walk(ast.Module(body=body)):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name in ('log', 'debug', 'info', 'warning', 'error', 'critical', 'exception', 'print'):
                    return True
        
        return False
    
    def _is_error_checked(self, call_node: ast.Call) -> bool:
        """Check if call is in try/except context"""
        # This is a simplified check - would need parent tracking for accuracy
        # For now, assume we'll catch this at the Try level
        return False
    
    def _get_call_name(self, call: ast.Call) -> Optional[str]:
        """Extract function name from call"""
        if isinstance(call.func, ast.Name):
            return call.func.id
        if isinstance(call.func, ast.Attribute):
            return call.func.attr
        return None
    
    def _get_code_snippet(self, line: int) -> str:
        start = max(0, line - 2)
        end = min(len(self.source_lines), line + 2)
        return "\n".join(self.source_lines[start:end])


def detect_evidence_voids(source_code: str) -> List[EvidenceVoid]:
    try:
        tree = ast.parse(source_code)
        source_lines = source_code.split('\n')
        detector = EvidenceVoidDetector(source_lines)
        detector.visit(tree)
        return detector.voids
    except SyntaxError:
        return []


def calculate_void_score(voids: List[EvidenceVoid]) -> float:
    if not voids:
        return 0.0
    
    weights = {"HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}
    total = sum(weights.get(v.severity, 1.0) for v in voids)
    return min(10.0, total)
