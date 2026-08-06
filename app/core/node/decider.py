from pydantic import BaseModel
from langchain_groq import ChatGroq
from typing import Dict,List
import os
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

class DeciderOutput(BaseModel):
    decider_status:float=0.0
    reasoning:str=""
    need_research:bool=False

class Decider:
    def __init__(self):
        self.model_version="llama-3.1-8b-instant"

    @traceable(name="Decider")
    def __call__(self,state:dict)->dict:
        query=state.get("query")
        finding=state.get("research")
        try:
            llm = ChatGroq(
                model=self.model_version,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

            system_prompt=f"""
                You are an expert Research Quality Controller. 
                Evaluate whether these findings comprehensively answer the original query. 
                Here are the findings collected from multiple research threads:
                {finding}
                Provide a decider_status score (0.0 to 1.0) and state whether a re-research loop is needed.
            """
            messages = [
                (
                    "system",
                    system_prompt
                ),
                ("human", query),
            ]

            structured_llm=llm.with_structured_output(DeciderOutput)
            response=structured_llm.invoke(messages)

            return {
                "decider_status":response.decider_status,
                "reasoning":response.reasoning,
                "need_research":response.need_research
            }
        
        except Exception as e:
            return {
                "decider_status":0.0,
                "reasoning":str(e),
                "need_research":True
            }

def main():
    decider_obj=Decider()
    query=input()
    mock_findings = [
        {
            "assigned_query": "Architectural differences between LSTM and GRU gates",
            "finding": {
                "https://example.com/lstm-vs-gru": "LSTMs have three gates (input, output, forget) and a separate cell state. GRUs combine the cell and hidden states and use only two gates (reset and update)."
            },
            "tool_logs": [{"status": "Success"}]
        }
    ]
    response=decider_obj({"query": query, "research": mock_findings})
    print(response)
    return 

if __name__=="__main__":
    main()