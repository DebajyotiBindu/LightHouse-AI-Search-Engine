from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from typing import List,Dict

load_dotenv()


class Generator:
    def __init__(self):
        self.model_version="openai/gpt-oss-120b"

    def __call__(self,state:dict) -> dict:
        """
        Receives the original query and the synthesized context, then produces the final output.
        """
        try:
            original_query = state.get("query")
            synthesized_draft = state.get("Synthesizer", {}).get("draft", "")
            citations = state.get("Synthesizer", {}).get("citation", {})
            llm = ChatGroq(
                model=self.model_version,
                temperature=0.2,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )

            system_prompt = f"""
            You are an expert technical communicator. 
            Your task is to write a clear, well-structured, and comprehensive final response to the user's original query, 
            using the synthesized research context provided below and also provide the citation as required for proof.
            Rules:
            1. Use the synthesized research context to inform your response. Do not introduce new information that is not present in the context.
            2. Ensure that the response is coherent, logically structured, and addresses all aspects of the original query.
            3. Include citations for any information derived from the synthesized context, formatted clearly and consistently.
            4. Maintain a professional and technical tone suitable for an expert audience.

            Original Query: {original_query}
            
            Synthesized Research Context:
            {synthesized_draft}

            citation:
            {citations}
            """

            messages = [
                ("system", system_prompt),
                ("human", "Generate the final response based on the provided context.")
            ]

            response=llm.invoke(messages)
            return {
                "generator": {
                    "output": response.content
                }
            }

        except Exception as e:
            return {
                "generator": {
                    "output": f"Error in generating final response: {str(e)}"
                }
            }

def main():
    generator_obj = Generator()
    
    test_query = "Compare the architectural differences and computational efficiency between LSTMs and GRUs."
    mock_draft = (
        "LSTMs utilize three gates (input, forget, output) and a separate cell state, "
        "making them robust for long-range dependencies. GRUs simplify this by merging cell and "
        "hidden states into a single vector and using only two gates (reset and update), "
        "resulting in higher computational efficiency and faster training times."
    )
    citation={'GRU architecture vs LSTM': 'https://research-papers.org/gru-summary', 'LSTM architecture': 'https://example-ai-docs.com/lstm-architecture', 'LSTM vs GRU computational efficiency and latency': 'https://engineering-ml.com/gru-vs-lstm-speed'}

    response = generator_obj({"query": test_query, "Synthesizer": {"draft": mock_draft, "citation": citation}})
    print(response)
    return

if __name__ == "__main__":
    main()