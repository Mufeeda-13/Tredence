# app/models.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class GraphCreateRequest(BaseModel):
    nodes: List[str]
    edges: Dict[str, str]
    start_node: str


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[str]


class GraphStateResponse(BaseModel):
    run_id: str
    current_node: Optional[str]
    state: Dict[str, Any]
    log: List[str]
    finished: bool
