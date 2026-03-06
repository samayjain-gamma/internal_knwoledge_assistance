from typing import Dict, List, Optional, TypedDict


class GraphState(TypedDict, total=False):

    user_input: str
    query: str
    rewritten_query: str
    retrieved_docs: List[Dict]

    history: Optional[List[Dict[str, str]]]

    generated_answer: str
    citations: List[str]

    injection_flag: bool
    input_validation_flag: bool
    exit: bool
