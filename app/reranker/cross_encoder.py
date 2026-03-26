from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from app.utils.config import settings
from app.utils.logger import logger

class DocumentReranker:
    def __init__(self):
        logger.info("Loading CrossEncoder model: cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)

    def rerank(self, query: str, documents: List[Document], top_k: int = None) -> List[Document]:
        if top_k is None:
            top_k = settings.RERANK_TOP_K
            
        if not documents:
            return []
            
        logger.info(f"Reranking {len(documents)} documents for query: '{query}'")
        pairs = [[query, doc.page_content] for doc in documents]
        scores = self.model.predict(pairs)
        
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        top_docs = [doc for doc, score in scored_docs[:top_k]]
        logger.info(f"Reranker selected {len(top_docs)} top documents.")
        return top_docs
