# app/workflows.py
from .engine import WorkflowEngine


def register_example_workflows(engine: WorkflowEngine) -> None:
    """
    Registers one example workflow: Code Review Mini-Agent.

    Nodes:
    1. extract_functions
    2. check_complexity
    3. detect_basic_issues
    4. suggest_improvements
    Loop until quality_score >= quality_threshold.
    """

    nodes = [
        "extract_functions",
        "check_complexity",
        "detect_basic_issues",
        "suggest_improvements",
    ]

    edges = {
        "extract_functions": "check_complexity",
        "check_complexity": "detect_basic_issues",
        "detect_basic_issues": "suggest_improvements",
        "suggest_improvements": "__END__",  # engine stops here unless node overrides
    }

    graph_id = engine.create_graph(
        nodes=nodes,
        edges=edges,
        start_node="extract_functions",
    )

    # Optional: store default graph id for easy testing
    engine.default_graph_id = graph_id
