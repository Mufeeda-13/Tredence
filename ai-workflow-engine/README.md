# Minimal Agent Workflow Engine (AI Engineering Assignment)

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

A minimal backend-only **workflow/graph engine** implemented using **FastAPI** for the AI Engineering Internship Assignment.  
This project demonstrates workflow execution, state transitions, branching, looping, and clean backend architecture.

---

## 📑 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Example Workflow](#example-workflow)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [API Usage](#api-usage)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## 📘 Overview
This project implements a **lightweight agent workflow engine** that supports:

- Node-based execution  
- Mutable state propagation  
- Looping and branching between nodes  
- Clean and well-designed FastAPI endpoints  

No frontend or machine learning models were used.  
The focus is purely backend engineering fundamentals.

---

## ⭐ Features

### 🔹 1. Workflow / Graph Engine  
- Nodes are Python functions operating on shared state (`dict`).  
- Directed edges describe transitions.  
- Supports node-level branching and looping.  
- In-memory graph + run storage.

### 🔹 2. Tool Registry  
Nodes are registered using:

```python
@register_tool("name")
🔹 3. FastAPI Endpoints
POST /graph/create – Create workflow graph

POST /graph/run – Run a workflow

GET /graph/state/{run_id} – Retrieve state/logs of a run

GET /graph/default-id – Get example workflow ID

Swagger documentation: http://127.0.0.1:8000/docs

🛠️ Tech Stack
Python 3.9+

FastAPI

Uvicorn

Pydantic

🧱 Architecture
arduino
Copy code
Client → FastAPI → Workflow Engine → Node Registry → Execution Logs
🧠 Example Workflow
This project implements Option A: Code Review Mini-Agent.

🔹 Nodes
1. extract_functions
Extracts function names from code.

2. check_complexity
Computes a simple complexity score using:

Number of lines

Number of functions

3. detect_basic_issues
Counts:

TODO comments

print() debug statements

4. suggest_improvements
Generates improvement suggestions

Computes quality_score

If score < threshold → loops back to extract_functions

Else → workflow ends

🔁 Loop Condition
lua
Copy code
while quality_score < quality_threshold:
    repeat workflow
📁 Project Structure
css
Copy code
ai-workflow-engine/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── engine.py
│   ├── tools.py
│   ├── workflows.py
│   └── models.py
├── requirements.txt
├── README.md
└── .gitignore
⚡ Setup
bash
Copy code
git clone https://github.com/<your-username>/ai-workflow-engine
cd ai-workflow-engine
pip install -r requirements.txt
uvicorn app.main:app --reload
🧪 API Usage
1️⃣ Get Default Graph ID
sql
Copy code
GET /graph/default-id
2️⃣ Run Workflow
Example request:

json
Copy code
{
  "graph_id": "<graph-id>",
  "initial_state": {
    "code": "def foo():\n    print('debug')\n    # TODO: fix",
    "quality_threshold": 0.8
  }
}
3️⃣ Get Run State
bash
Copy code
GET /graph/state/{run_id}
🚀 Future Improvements
Add database persistence

Async/background execution

WebSocket-based log streaming

AST-based real code analysis

Unit tests

Parallel node execution

Author
Mufeeda O
AI & Data Science Student
📧 Email: Mufeeda1312@gmail.com

