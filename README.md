# LightHouse 

> Navigate through the sea of information.

LightHouse is an autonomous, graph-driven AI search and research engine engineered to cut through digital noise. Rather than relying on superficial keyword matching or static outputs, LightHouse uses an active multi-step pipeline to decompose complex queries, retrieve high-signal documents from across the web, and stream structured markdown synthesis directly to your interactive workspace.

---

## Architectural Overview

LightHouse moves beyond traditional LLM wrappers by implementing a structured agentic workflow that mimics a rigorous human research process:

1. **Intelligent Query Decomposition**
   * Sprawling or complex technical questions are automatically broken down into sharp, atomic sub-queries.
   * Targets multiple facets of a topic simultaneously to ensure broad and deep web coverage.

2. **Precision Retrieval & Human-in-the-Loop Curation**
   * Scans deep layers of the web to aggregate relevant documents and data points.
   * Features an interactive review card that allows you to inspect, modify, or curate the generated sub-queries before final synthesis begins.

3. **Real-Time Typewritten Stream Flow**
   * Compiled research reports are dynamically streamed token by token into a continuous chat stream interface.
   * Full robust markdown rendering transforms raw model outputs into beautifully formatted, structured technical documentation instantly.

---

## 🛠️ Technical Stack & Architecture

* **Backend Framework:** FastAPI (Python) for ultra-fast asynchronous routing and API management.
* **Orchestration & State Management:** LangGraph / LangChain for managing multi-step agent graphs and context threads.
* **Frontend Interface:** Pure HTML5, CSS3, and JavaScript featuring a modern dark-mode developer aesthetic (`#0b0f19` theme), custom Inter typography, and dynamic DOM manipulation.

---

## Quick Start Guide

### 1. Clone the Repository
```
git clone [https://github.com/DebajyotiBindu/LightHouse-AI-Search-Engine.git](https://github.com/DebajyotiBindu/LightHouse-AI-Search-Engine.git)
```