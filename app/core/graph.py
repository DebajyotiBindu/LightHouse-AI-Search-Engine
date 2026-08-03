import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app.core.node.planner import OutputFormat,Planner
from app.core.node.researcher import ResearchOutput,Research
from app.core.node.decider import DeciderOutput,Decider
from app.core.node.synthesizer import Synthesizer
from app.core.node.generator import Generator
import os
from app.core.state import (
    State,
    PlannerState,
    ResearchState,
    EvaluationState,
    SynthesisState,
    GeneratorState
)
import sqlite3
from typing import Annotated,List,Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Send


os.makedirs("checkpoints",exist_ok=True)
conn=sqlite3.connect("checkpoints/state_graph.db",check_same_thread=False)
checkpointer=SqliteSaver(conn)

graph_builder=StateGraph(State)

graph_builder.add_node("Planner",Planner())
graph_builder.add_node("Researcher",Research())
graph_builder.add_node("Decider",Decider())
graph_builder.add_node("Synthesizer",Synthesizer())
graph_builder.add_node("Generator",Generator())

def distribute_research(state:State)->List[Send]:
    return [
        Send("Researcher",{"sub_query":query})
        for query in state["sub_queries"]
    ]

graph_builder.add_edge(START,"Planner")

graph_builder.add_conditional_edges(
    "Planner",
    distribute_research,
    ["Researcher"]
)

def more_research(state:State):
    evaluation=state.get("evaluation")
    if evaluation and evaluation.get("need_research"):
        return "Planner"
    return "Synthesizer"

graph_builder.add_edge("Researcher","Decider")
graph_builder.add_conditional_edges(
    "Decider",
    more_research,
    {
        "Planner":"Planner",
        "Synthesizer":"Synthesizer"
    }
)
graph_builder.add_edge("Synthesizer","Generator")
graph_builder.add_edge("Generator",END)

app=graph_builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["Researcher"]
)

# config={"configurable":{"thread_id":"5"}}
# app.invoke({"query":"Compare between LSTM and GRU"},config=config)
# current_state=app.get_state(config)
# sub_query=current_state.values.get("sub_queries",[])
# print("Current Draft for Review:", sub_query)

# print("\n[Options]")
# print("1. Press Enter to approve as-is.")
# print("2. Type your modifications, corrections, or new points to inject them into the draft.\n")

# user_input=input("Enter your input: ").strip()

# if user_input:
#     sub_query.append(user_input)
#     app.update_state(config,{"sub_queries":sub_query})
#     print("Updated Draft for Review:", current_state.values.get("sub_queries",[]))

# for message,metadata in app.stream(None,config=config,stream_mode="messages"):
#     if metadata.get("langgraph_node")=="Generator" and message.content:
#         print(message.content,end="",flush=True)