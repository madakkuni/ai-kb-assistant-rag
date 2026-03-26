import time
from typing import Dict, Any, List
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
from app.langgraph.state import RequestState
from app.retriever.hybrid_retriever import HybridRetriever
from app.reranker.cross_encoder import DocumentReranker
from app.evaluation.evaluator import RAGEvaluator
from app.utils.config import settings
from app.utils.logger import logger

# Global singletons for performance
retriever_instance = None
reranker_instance = None
llm = None
evaluator = None

def init_components():
    global retriever_instance, reranker_instance, llm, evaluator
    if retriever_instance is None:
        try:
            retriever_instance = HybridRetriever()
        except Exception as e:
            logger.error(f"Error initializing hybrid retriever: {e}")
            
    if reranker_instance is None:
        try:
            reranker_instance = DocumentReranker()
        except Exception as e:
            logger.error(f"Error initializing reranker: {e}")

    if llm is None:
        try:
            llm = AzureChatOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                temperature=settings.TEMPERATURE
            )
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            
    if evaluator is None:
        evaluator = RAGEvaluator()

def hybrid_retrieval_node(state: RequestState) -> Dict[str, Any]:
    init_components()
    logger.info("Executing node: hybrid_retrieval")
    if retriever_instance is None:
        return {"retrieved_docs": []}
    docs = retriever_instance.retrieve(state["query"], top_k=state.get("top_k", settings.TOP_K))
    return {"retrieved_docs": docs}

def reranker_node(state: RequestState) -> Dict[str, Any]:
    init_components()
    logger.info("Executing node: reranker")
    if reranker_instance is None or not state.get("retrieved_docs"):
        return {"reranked_docs": state.get("retrieved_docs", [])}
    
    docs = reranker_instance.rerank(
        query=state["query"], 
        documents=state["retrieved_docs"], 
        top_k=state.get("rerank_top_k", settings.RERANK_TOP_K)
    )
    return {"reranked_docs": docs}

def answer_generator_node(state: RequestState) -> Dict[str, Any]:
    init_components()
    logger.info("Executing node: answer_generator")
    docs = state.get("reranked_docs", [])
    context_str = "\n\n".join([f"Source: {d.metadata.get('source', 'Unknown')} (Chunk {d.metadata.get('chunk', 'N/A')})\n{d.page_content}" for d in docs])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the KB Assistant, an enterprise RAG application. Answer the user's question using ONLY the provided contexts. If the answer is not in the context, say 'I cannot answer this based on the provided documents.' Cite your sources directly referencing the provided Source names/chunks if possible."),
        ("user", f"Contexts:\n{context_str}\n\nQuestion: {state['query']}")
    ])
    
    chain = prompt | llm
    
    with get_openai_callback() as cb:
        res = chain.invoke({})
        tokens = {
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_tokens": cb.total_tokens
        }
        
    return {
        "answer": res.content,
        "token_usage": tokens
    }

def citation_node(state: RequestState) -> Dict[str, Any]:
    logger.info("Executing node: citation")
    docs = state.get("reranked_docs", [])
    
    source_map = {}
    
    for doc in docs:
        source_name = doc.metadata.get("source", "Unknown")
        # Ensure only filename is used, extract filename from full path if necessary
        source_name = source_name.replace('\\', '/').split('/')[-1]
        
        chunk = doc.metadata.get("chunk", "N/A")
        if source_name not in source_map:
            source_map[source_name] = []
        if str(chunk) not in source_map[source_name]:
            source_map[source_name].append(str(chunk))
            
    sources = []
    for source_name, chunks in source_map.items():
        sources.append({
            "source": source_name,
            "chunks": ", ".join(chunks),
        })
            
    return {"sources": sources}

def evaluation_node(state: RequestState) -> Dict[str, Any]:
    init_components()
    if not state.get("eval_mode"):
        return {"evaluation_metrics": None}
        
    logger.info("Executing node: evaluation")
    metrics = evaluator.evaluate(
        query=state["query"],
        answer=state["answer"],
        context=state.get("reranked_docs", [])
    )
    return {"evaluation_metrics": metrics}
