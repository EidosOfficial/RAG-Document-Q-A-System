from typing import TypedDict, List


class AgentState(TypedDict):
    question: str
    retrieved_chunks: List
    context: str
    generation: str
    is_sufficient: str
    retry_count: int
