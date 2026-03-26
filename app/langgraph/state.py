from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.documents import Document

class RequestState(TypedDict):
    query: str
    top_k: int
    rerank_top_k: int
    eval_mode: bool
    
    # intermediate
    retrieved_docs: List[Document]
    reranked_docs: List[Document]
    
    # outputs
    answer: str
    sources: List[Dict[str, Any]]
    
    # evaluation
    evaluation_metrics: Optional[Dict[str, Any]]
    
    # tracking
    token_usage: Dict[str, int]
