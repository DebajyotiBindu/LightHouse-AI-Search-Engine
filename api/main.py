import uuid
from typing import List,Dict,Optional
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
from app.core.graph import app
from fastapi import FastAPI
from pydantic import BaseModel

fastapi_app=FastAPI()


class StartQuery(BaseModel):
    query:str
    updated_query:Optional[List[str]]
    thread_id:Optional[str]

@fastapi_app.post('/start')
def start_query(payload: StartQuery):
    if not payload.thread_id or payload.thread_id.strip() in ["", "string"]:
        uid=str(uuid.uuid4())
        is_new=True
    else:
        uid=payload.thread_id.strip()
        is_new=False

    config={"configurable": {"thread_id": uid}}
    
    try:
        current_state=app.get_state(config)
        has_state=bool(current_state and current_state.values)
    except Exception:
        has_state=False

    if is_new or not has_state:
        if not payload.query:
            return {"status": "error", "message": "Query is required for new threads."}
        
        app.invoke({"query": payload.query}, config=config)
        
        curr_state=app.get_state(config)
        sub_queries=curr_state.values.get("sub_queries", [])

        return {
            "status": "pending_review",
            "message": "Graph paused for human review.",
            "thread_id": uid,
            "sub_query": sub_queries,
            "Output": None
        }

    else:
        if payload.updated_query is not None:
            app.update_state(config, {"sub_queries": payload.updated_query}, as_node="Planner")
        
        final_output=app.invoke(None, config=config)
        
        generator_state=final_output.get("Generator", final_output.get("generator", {}))  
        if isinstance(generator_state, dict):
            final_output_state_value=generator_state.get("output") or generator_state.get("final_answer") or str(generator_state)
        else:
            final_output_state_value=str(generator_state)

        return {
            "status": "completed",
            "message": "Graph execution finished successfully.",
            "thread_id": uid,
            "sub_query": payload.updated_query or [],
            "Output": final_output_state_value
        }