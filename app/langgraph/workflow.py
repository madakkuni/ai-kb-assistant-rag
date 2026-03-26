from langgraph.graph import StateGraph, END
from app.langgraph.state import RequestState
from app.langgraph.nodes import (
    hybrid_retrieval_node,
    reranker_node,
    answer_generator_node,
    citation_node,
    evaluation_node
)

def create_workflow():
    workflow = StateGraph(RequestState)
    
    workflow.add_node("hybrid_retrieval", hybrid_retrieval_node)
    workflow.add_node("reranker", reranker_node)
    workflow.add_node("answer_generator", answer_generator_node)
    workflow.add_node("citation", citation_node)
    workflow.add_node("evaluation", evaluation_node)
    
    workflow.set_entry_point("hybrid_retrieval")
    
    workflow.add_edge("hybrid_retrieval", "reranker")
    workflow.add_edge("reranker", "answer_generator")
    workflow.add_edge("answer_generator", "citation")
    workflow.add_edge("citation", "evaluation")
    workflow.add_edge("evaluation", END)
    
    app = workflow.compile()
    return app

rag_workflow = create_workflow()
