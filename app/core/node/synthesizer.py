import os 
from pydantic import BaseModel
from langchain_groq import ChatGroq
from typing import Dict,List 
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()


class Synthesizer:
    """
    Takes the query and all the findings done and approved by research and decider node and forms a
    good quality, LLM suitable context for forwarding to the generator node
    """
    def __init__(self):
        self.model_version="llama-3.1-8b-instant"

    @traceable(name="Synthesizer")  
    def __call__(self,state:dict)->dict:
        query=state.get("query")
        all_findings=state.get("research")
        try:
            llm = ChatGroq(
                model=self.model_version,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )

            cleaned_findings_text = "\n\n".join(
                [f"- **Query:** {f.get('assigned_query')}\n  **Finding:** {list(f.get('finding', {}).values())[0]}" 
                for f in all_findings]
            )

            system_prompt = f"""
                You are an expert Research Synthesizer and Technical Writer.
                Original User Query: {query}

                Here are all the raw findings collected from parallel research threads:
                {cleaned_findings_text}

                Your task is to synthesize these findings into a coherent, well-structured, and comprehensive draft that addresses the original query.
                ### YOUR RULES:
                1. SYNTHESIS: Integrate the findings into a unified narrative that answers the original query. Avoid redundancy and contradictions.
                2. STRUCTURE: Organize the draft into clear sections with headings, subhead
                ings, and bullet points where appropriate. Ensure logical flow and clarity.
                4. CLARITY: Use precise and technical language suitable for an expert audience.
                """

            messages=[
                    ("system", system_prompt),
                    ("human", "Synthesize these findings into the requested structure.")
                ]

            responses=llm.invoke(messages)

            citing_dict={}
            for finding in all_findings:
                for url in finding.get("finding",{}).keys():
                    citing_dict[url]=finding.get("assigned_query","Unknown sub-query")

            return{
                "Synthesizer": {
                    "merged_finding":all_findings,
                    "draft":responses.content,
                    "citation":citing_dict
                }
            }

        except Exception as e:
            return {
                "Synthesizer": {
                    "merged_finding": [],
                    "draft": str(e),
                    "citation": {}
                }
            }

def main():
    synthesizer_obj=Synthesizer()
    query="Compare the architectural differences and computational efficiency between LSTMs and GRUs."
    mock_finding=[
        {
            "assigned_query": "LSTM architecture and gates explained",
            "finding": {
                "https://example-ai-docs.com/lstm-architecture": "LSTMs contain three distinct gates: the input gate, forget gate, and output gate. They also maintain a separate cell state (long-term memory) alongside the hidden state (short-term memory). This separation allows them to combat the vanishing gradient problem effectively over long sequences."
            },
            "tool_logs": [{"status": "Success"}]
        },
        {
            "assigned_query": "GRU architecture vs LSTM",
            "finding": {
                "https://example-ai-docs.com/gru-architecture": "GRUs (Gated Recurrent Units) simplify the LSTM design by merging the cell state and hidden state into a single unified hidden state. They use only two gates: an update gate (which acts like a combination of LSTM's forget and input gates) and a reset gate."
            },
            "tool_logs": [{"status": "Success"}]
        },
        {
            "assigned_query": "GRU architecture vs LSTM",
            "finding": {
                "https://research-papers.org/gru-summary": "GRUs (Gated Recurrent Units) simplify the LSTM design by merging the cell state and hidden state into a single unified hidden state. They use only two gates: an update gate (which acts like a combination of LSTM's forget and input gates) and a reset gate."
            },
            "tool_logs": [{"status": "Success"}]
        },
        {
            "assigned_query": "LSTM vs GRU computational efficiency and latency",
            "finding": {
                "https://engineering-ml.com/gru-vs-lstm-speed": "Because GRUs have fewer tensor operations (two gates instead of three) and no separate cell state, they are computationally more efficient, use less memory, and train faster than LSTMs. This makes GRUs preferable for real-time inference, though LSTMs can sometimes remember longer sequences better due to their explicit cell state."
            },
            "tool_logs": [{"status": "Success"}]
        }
    ]
    response=synthesizer_obj({"query": query, "research": mock_finding})

    print(response)
    return 

if __name__=="__main__":
    main()