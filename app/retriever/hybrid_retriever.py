import os
from typing import List, Dict
import numpy as np
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from rank_bm25 import BM25Okapi
from app.utils.config import settings
from app.utils.logger import logger

class HybridRetriever:
    def __init__(self):
        self.embeddings = AzureOpenAIEmbeddings(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            azure_deployment=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION
        )
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        self.vectorstore = Chroma(
            persist_directory=settings.VECTOR_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="kb_assistant"
        )
        self.documents: List[Document] = []
        self.bm25 = None
        self._initialize_bm25_from_vectorstore()

    def _initialize_bm25_from_vectorstore(self):
        try:
            all_docs = self.vectorstore.get()
            if all_docs and all_docs.get('documents'):
                texts = all_docs['documents']
                metadatas = all_docs['metadatas']
                
                self.documents = []
                tokenized_corpus = []
                for i, text in enumerate(texts):
                    doc = Document(page_content=text, metadata=metadatas[i] if metadatas else {})
                    self.documents.append(doc)
                    tokenized_corpus.append(text.lower().split(" "))
                
                if tokenized_corpus:
                    self.bm25 = BM25Okapi(tokenized_corpus)
                    logger.info(f"Initialized BM25 with {len(self.documents)} documents.")
        except Exception as e:
            logger.warning(f"Could not initialize BM25 from existing vectorstore: {e}")

    def add_documents(self, documents: List[Document]):
        logger.info(f"Adding {len(documents)} documents to Hybrid Retriever")
        
        self.vectorstore.add_documents(documents)
        self.documents.extend(documents)
        
        tokenized_corpus = [doc.page_content.lower().split(" ") for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.info(f"Updated BM25 index. Total documents: {len(self.documents)}")

    def retrieve(self, query: str, top_k: int = None) -> List[Document]:
        if top_k is None:
            top_k = settings.TOP_K
            
        logger.info(f"Running Hybrid Retrieval for query: '{query}'")
        if not self.documents:
            logger.warning("No documents in index.")
            return []

        # Vector Search
        vector_results = self.vectorstore.similarity_search(query, k=top_k)
        
        # BM25 Search
        tokenized_query = query.lower().split(" ")
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_n_indices = np.argsort(bm25_scores)[::-1][:top_k]
        bm25_results = [self.documents[i] for i in top_n_indices if bm25_scores[i] > 0]
        
        # Merge and Deduplicate
        merged_docs = {}
        for doc in vector_results + bm25_results:
            doc_hash = hash(doc.page_content)
            if doc_hash not in merged_docs:
                merged_docs[doc_hash] = doc
                
        results = list(merged_docs.values())
        logger.info(f"Hybrid retrieval yielded {len(results)} unique documents.")
        return results
