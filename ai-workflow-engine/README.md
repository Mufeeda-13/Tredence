# Minimal Agent Workflow Engine (AI Engineering Assignment)

This repository contains a **minimal backend-only workflow/graph engine** implemented with **FastAPI** for the AI Engineering Internship assignment.

The goal is to demonstrate:

- Python backend fundamentals
- Clean API design with FastAPI
- Simple agent/workflow execution model
- State → transitions → loops
- Basic code hygiene

No frontend or machine learning is used here – everything is pure Python backend logic. :contentReference[oaicite:1]{index=1}


## Features

### 1. Minimal Workflow / Graph Engine

- **Nodes**: Each node is a Python function (a "tool") operating on a shared state (`dict`).
- **State**: A mutable `dict` that flows from one node to the next.
- **Edges**: Simple mapping `{"node_a": "node_b"}` describing the default execution path.
- **Branching**: A node can override the next node dynamically (e.g., based on a value in `state`).
- **Looping**: A node can return itself (or a previous node) as the next node to create a loop.
- **In-memory storage**: Graph definitions and runs are stored in memory for simplicity.

### 2. Tool Registry

- Tools (nodes) are just Python functions.
- A decorator `@register_tool("name")` registers them into a global registry.
- The `WorkflowEngine` looks up node names in this registry during execution.

### 3. FastAPI Endpoints

Exposed endpoints:

1. `POST /graph/create`  
   - **Input**: JSON describing `nodes`, `edges`, and `start_node`  
   - **Output**: `{ "graph_id": "<uuid>" }`

2. `POST /graph/run`  
   - **Input**: `graph_id` + `initial_state` (JSON)  
   - **Output**: `run_id`, `final_state`, and an execution `log`

3. `GET /graph/state/{run_id}`  
   - **Input**: `run_id` (path)  
   - **Output**: current `state`, `log`, and `finished` flag for the run

4. `GET /graph/default-id` (helper)  
   - Returns the `graph_id` of the pre-registered example workflow.

The APIs are clean, minimal, and easy to reason about.

---

## Example Workflow Implemented: Code Review Mini-Agent

This repo implements **Option A: Code Review Mini-Agent** from the assignment.

### Nodes

1. **`extract_functions`**
   - Reads the `code` string from the state.
   - Extracts very simple function names from lines starting with `def`.
   - Stores results under `state["functions"]`.

2. **`check_complexity`**
   - Computes a fake `complexity_score` using:
     - Number of lines of code
     - Number of functions
   - Stores result in `state["complexity_score"]`.

3. **`detect_basic_issues`**
   - Counts:
     - Lines containing `"TODO"`
     - Lines containing `"print("`
   - Stores `state["issue_count"]`.

4. **`suggest_improvements`**
   - Uses `complexity_score` and `issue_count` to:
     - Generate a list of text suggestions under `state["suggestions"]`
     - Compute a simple `quality_score` in `[0,1]`
   - Reads `state["quality_threshold"]` (default 0.8 if not given).
   - If `quality_score < quality_threshold`, it **loops** by overriding the next node to `"extract_functions"`.
   - Otherwise, it lets the engine follow the graph edges to `__END__`.

### Loop Condition

- The workflow **loops** until:  
  `quality_score >= quality_threshold`

This demonstrates **stateful looping** and **simple branching** inside the node.

---

## Project Structure

```text
ai-workflow-engine/
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app, endpoints
│   ├── engine.py            # Workflow engine + in-memory graph & runs
│   ├── tools.py             # Code review tools (nodes)
│   ├── workflows.py         # Registers the Code Review workflow
│   └── models.py            # Pydantic models for request/response schemas
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore
