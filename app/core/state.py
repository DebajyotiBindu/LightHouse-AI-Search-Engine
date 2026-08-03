import os
from typing_extensions import TypedDict,List,Dict
from typing import Annotated
from pydantic import BaseModel
import operator

class PlannerState(BaseModel):
    query:str
    sub_queries:List[str]=[]
    confidence:int=0

class ResearchState(BaseModel):
    assigned_query:str
    finding:Dict[str,str]={}
    tool_logs:List[Dict]=[]

class EvaluationState(BaseModel):
    decider_status:float=0.0
    reasoning:str=""
    need_research:bool=False

class SynthesisState(BaseModel):
    merged_finding:List[Dict]=[]
    draft:str=""
    citation:dict[str,str]={}

class GeneratorState(BaseModel):
    output:str=""

class State(TypedDict):
    query:str
    sub_queries:List[str]
    research: Annotated[List[dict], operator.add]
    evaluation:EvaluationState
    Synthesizer: SynthesisState
    generator: GeneratorState
