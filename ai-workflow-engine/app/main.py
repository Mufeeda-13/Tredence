# app/main.py
from fastapi import FastAPI, HTTPException

from .engine import WorkflowEngine, TOOL_REGISTRY
from .models import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    GraphStateResponse,
)
from . import tools  # noqa: F401  # ensures tools are imported and registered
from .workflows import register_example_workflows

app = FastAPI(
    title="Minimal Agent Workflow Engine",
    description="A simple backend assignment implementation with FastAPI.",
    version="0.1.0",
)

engine = WorkflowEngine(tool_registry=TOOL_REGISTRY)
register_example_workflows(engine)


@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(payload: GraphCreateRequest):
    """
    Create a new workflow graph.

    Input (JSON):
    {
        "nodes": ["extract_functions", "check_complexity", ...],
        "edges": {"extract_functions": "check_complexity", ...},
        "start_node": "extract_functions"
    }
    """
    try:
        graph_id = engine.create_graph(
            nodes=payload.nodes,
            edges=payload.edges,
            start_node=payload.start_node,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run", response_model=GraphRunResponse)
def run_graph(payload: GraphRunRequest):
    """
    Run an existing graph from the beginning.

    Input (JSON):
    {
        "graph_id": "<id_from_create_or_default>",
        "initial_state": {
            "code": "...",
            "quality_threshold": 0.8
        }
    }
    """
    try:
        run = engine.run_graph(
            graph_id=payload.graph_id,
            initial_state=payload.initial_state,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return GraphRunResponse(
        run_id=run.run_id,
        final_state=run.state,
        log=run.log,
    )


@app.get("/graph/state/{run_id}", response_model=GraphStateResponse)
def get_graph_state(run_id: str):
    """
    Get the current state of a workflow run.

    This is useful if you later extend to async / background execution.
    For now, runs complete synchronously, but we still store and expose state.
    """
    run = engine.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return GraphStateResponse(
        run_id=run.run_id,
        current_node=run.current_node,
        state=run.state,
        log=run.log,
        finished=run.finished,
    )


@app.get("/graph/default-id")
def get_default_graph_id():
    """
    Convenience endpoint to fetch the auto-registered example workflow id.
    """
    if not engine.default_graph_id:
        raise HTTPException(status_code=404, detail="No default graph registered")
    return {"graph_id": engine.default_graph_id}
