import getpass
import os 
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List,Dict

load_dotenv()

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

class ResearchOutput(BaseModel):
    assigned_query:str
    finding:Dict[str,str]={}
    tool_logs:List[Dict]=[]

class Research:
    def __init__(self):
        pass

    def __call__(self,state:dict)->dict:
        try:
            query=state.get("sub_query")
            """
            Receives query and does the web search(Research) and provide a structured formatted output.
            The next node after planner that does the research part on a single query at a time
            """

            tool = TavilySearch(
                max_results=3,
                topic="general",
                search_depth="basic",
                include_answer=True,
                include_image_descriptions=False
            )

            results = tool.invoke(query)

            assigned_query=results['query']
            findings={}
            tool_log=[
                {
                    "status":"Success",
                    "subquery":assigned_query
                }
            ]

            for res in results.get("results",[]):
                url=res.get("url","Unknown url")
                content=res.get("content","No content found")
                findings[url]=content
            
            output=ResearchOutput(
                assigned_query=assigned_query,
                finding=findings,
                tool_log=tool_log
            )

            return {
                "research": [output.model_dump()]
            }
        
        except Exception as e:
            tool_log=[
                {
                    "status":"Failed",
                    "subquery":query
                }
            ]

            print(f"Research agent has failed")
            output=ResearchOutput(
                assigned_query=query,
                finding={"error":str(e)},
                tool_log=tool_log
            )
            return {
                "research": [output.model_dump()]
            }

def main():
    research_obj=Research()
    query="Architectural differences between LSTM and GRU gates"
    result=research_obj({"sub_query": query})

    print(result)

    return
    
if __name__=="__main__":
    main()