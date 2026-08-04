# LightHouse

> Navigate through the sea of information.

LightHouse is an autonomous, graph-driven AI search and research engine engineered to cut through digital noise. Rather than relying on superficial keyword matching or static outputs, LightHouse uses an active multi-step pipeline to decompose complex queries, retrieve high-signal documents from across the web, and stream structured markdown synthesis directly to your interactive workspace.

---
## Architectural Workflow Diagram
<img width="852" height="782" alt="Screenshot 2026-08-03 160040" src="https://github.com/user-attachments/assets/9132abf2-5bc9-45eb-b56f-d0afa5c38487" />

## Folder Structure (Folder structure too big to manually add in markdown)
<img width="885" height="723" alt="Screenshot 2026-08-03 161832" src="https://github.com/user-attachments/assets/871029b2-1d8b-4471-ad35-995cf90dbcd1" />

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

## Technical Stack & Architecture

* **Backend Framework:** FastAPI (Python) for ultra-fast asynchronous routing and API management.
* **Orchestration & State Management:** LangGraph / LangChain for managing multi-step agent graphs and context threads.
* **Frontend Interface:** Pure HTML5, CSS3, and JavaScript featuring a modern dark-mode developer aesthetic (`#0b0f19` theme), custom Inter typography, and dynamic DOM manipulation.

---

## Why LightHouse?

LightHouse combines deterministic human-in-the-loop control with resilient LangGraph state management and request caching. This ensures reliable, multi-step research workflows that avoid redundant API compute overhead while delivering high-signal, fully transparent insights.

---

## Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/DebajyotiBindu/LightHouse-AI-Search-Engine.git
```

## Some Screenshots of LightHouse:
### Home Page
<img width="785" height="600" alt="Screenshot 2026-08-03 161832" src="https://github.com/user-attachments/assets/a990bd5a-270c-4f0f-9047-7a3111af59b6" />

### Chat Page
<img width="785" height="600" alt="Screenshot 2026-08-03 154019" src="https://github.com/user-attachments/assets/7dabee06-cdb5-4806-81a0-5634fbba14ae" />
<img width="785" height="600" alt="Screenshot 2026-08-03 154104" src="https://github.com/user-attachments/assets/8634e4be-73ee-4d4a-8765-f315001a2bf9" />
<img width="785" height="600" alt="Screenshot 2026-08-03 154146" src="https://github.com/user-attachments/assets/2d849f64-9486-42bd-94eb-11d092639844" />
<img width="785" height="600" alt="Screenshot 2026-08-03 154201" src="https://github.com/user-attachments/assets/e4da6589-9189-476d-b619-3fba749104db" />

