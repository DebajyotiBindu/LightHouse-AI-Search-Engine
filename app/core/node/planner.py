import os
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import List
from langgraph.types import Overwrite
from langsmith import traceable

load_dotenv()

class OutputFormat(BaseModel):
    query:str
    sub_queries:List[str]
    confidence:int=0

class Planner:
    def __init__(self):
        self.model_version="openai/gpt-oss-120b"

    @traceable(name="Planner")
    def __call__(self,state:dict)->dict:
        query=state.get("query")
        try:
            '''Generates a list of subquery with confidence from the user query/question'''

            llm = ChatGroq(
                model=self.model_version,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

            system_prompt="""
                You are an expert Research Architect. Your task is to decompose the user's complex query into a precise, non-overlapping, and exhaustive list of sub-queries that can be researched independently.

                ### YOUR RULES:
                1. DECOMPOSITION: Break the user's intent into distinct research tasks. Avoid generic queries.
                2. INDEPENDENCE: Each sub-query must be self-contained. One sub-query should not depend on the results of another to be executed.
                3. SPECIFICITY: Use technical terminology relevant to the subject matter to ensure high-quality search results.
                4. MINIMALISM: Do not include redundant sub-queries. Only include tasks that are strictly necessary to answer the primary goal.
                5. CONTEXT: If the user's query is ambiguous, infer the most logical professional intent and plan accordingly.

                ### OUTPUT EXPECTATION:
                - Provide a list of sub-queries that cover the entire scope of the user's request.
                - Provide the average confidence score (Integer Format) for the entire list of subquery that you generate.
                - Focus on creating a roadmap that leads to a comprehensive, evidence-based final answer.
            """

            messages = [
                (
                    "system",
                    system_prompt
                ),
                ("human", query),
            ]

            structured_model = llm.with_structured_output(OutputFormat)

            response=structured_model.invoke(messages)
            return {
                "sub_queries":response.sub_queries,
                "confidence":response.confidence,
                "research":Overwrite([])
            }

        except Exception as e:
            return {
                "sub_queries":[],
                "confidence":0,
                "research":Overwrite([])
            }
    def plan(self, query):
        return self.__call__({"query": query})


def main():
    query=input()
    planner_obj=Planner()

    response=planner_obj.plan(query=query)
    print(response)

if __name__=="__main__":
    main()