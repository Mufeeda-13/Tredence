# app/tools.py
from typing import Any, Dict, Optional, Tuple, List

from .engine import State, NodeFunc, register_tool


def _get_threshold(state: State) -> float:
    # Default threshold if not provided in state
    return float(state.get("quality_threshold", 0.8))


@register_tool("extract_functions")
def extract_functions(state: State) -> Tuple[State, Optional[str]]:
    """
    Very simple, rule-based "function extractor".
    Looks for lines starting with 'def ' and collects function names.
    """
    code: str = state.get("code", "")
    functions: List[str] = []

    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def ") and "(" in line:
            name_part = line[4:line.index("(")].strip()
            if name_part:
                functions.append(name_part)

    state["functions"] = functions
    state.setdefault("log", []).append(f"Extracted {len(functions)} function(s).")
    # No override; engine will follow edges
    return state, None


@register_tool("check_complexity")
def check_complexity(state: State) -> Tuple[State, Optional[str]]:
    """
    Fake "complexity" check:
    - Uses number of lines and functions to create a simple complexity score.
    """
    code: str = state.get("code", "")
    functions = state.get("functions", [])
    num_lines = len(code.splitlines())
    num_functions = len(functions)

    # Very naive fake score
    complexity_score = min(1.0, (num_lines / 200.0) + (num_functions / 20.0))
    state["complexity_score"] = complexity_score
    state.setdefault("log", []).append(
        f"Complexity score computed: {complexity_score:.2f}"
    )
    return state, None


@register_tool("detect_basic_issues")
def detect_basic_issues(state: State) -> Tuple[State, Optional[str]]:
    """
    Detect simple issues:
    - 'TODO' comments
    - 'print(' usage as a proxy for debug code
    """
    code: str = state.get("code", "")
    issues = 0

    for line in code.splitlines():
        if "TODO" in line:
            issues += 1
        if "print(" in line:
            issues += 1

    state["issue_count"] = issues
    state.setdefault("log", []).append(f"Detected {issues} basic issue(s).")

    return state, None


@register_tool("suggest_improvements")
def suggest_improvements(state: State) -> Tuple[State, Optional[str]]:
    """
    Suggests basic improvements and updates a quality_score.
    Loops until 'quality_score >= quality_threshold'.
    Loop is implemented by overriding the next node.
    """
    complexity = float(state.get("complexity_score", 0.0))
    issues = int(state.get("issue_count", 0))
    threshold = _get_threshold(state)

    suggestions: List[str] = []

    if complexity > 0.8:
        suggestions.append("Consider splitting large functions into smaller ones.")
    if issues > 0:
        suggestions.append("Remove debug prints and address TODO comments.")
    if not suggestions:
        suggestions.append("Code looks clean based on current simple checks.")

    # Very simple quality scoring: lower complexity and fewer issues -> higher quality
    quality_score = max(0.0, 1.0 - complexity - (issues * 0.05))
    quality_score = max(0.0, min(1.0, quality_score))

    state["quality_score"] = quality_score
    state["suggestions"] = suggestions
    state.setdefault("log", []).append(
        f"Quality score: {quality_score:.2f} (threshold: {threshold:.2f})"
    )

    # Looping: if below threshold, re-run from extract_functions
    if quality_score < threshold:
        state.setdefault("log", []).append(
            "Quality below threshold, looping once more through the pipeline."
        )
        # In a real system you might mutate state etc. Here we just demonstrate the loop.
        return state, "extract_functions"

    state.setdefault("log", []).append(
        "Quality threshold reached. Stopping the workflow."
    )
    # None = follow edges to "__END__" in the graph
    return state, None
