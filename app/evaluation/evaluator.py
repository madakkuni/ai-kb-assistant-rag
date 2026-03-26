from typing import Dict, Any, List
from langchain_core.documents import Document
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.utils.config import settings
from app.utils.logger import logger
import json
import os

class RAGEvaluator:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=0.0
        )
        self.eval_file = "evaluation/results.json"
        os.makedirs(os.path.dirname(self.eval_file), exist_ok=True)

    def evaluate(self, query: str, answer: str, context: List[Document]) -> Dict[str, Any]:
        logger.info(f"Running evaluation for query: {query}")
        context_str = "\n".join([doc.page_content for doc in context])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert RAG evaluation judge. You will be provided with a Question, contexts, and an Answer. Evaluate the Answer based on three metrics: Faithfulness (is the answer derived from the context?), Context Precision (are the contexts relevant to the question?), and Answer Relevance (does the answer directly address the question?). Score each from 0 to 1. Output ONLY a JSON object with keys: faithfulness, context_precision, answer_relevance."),
            ("user", f"Question: {query}\n\nContexts:\n{context_str}\n\nAnswer: {answer}")
        ])
        
        try:
            chain = prompt | self.llm
            res = chain.invoke({})
            # parse json
            text = res.content.strip()
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()
                
            metrics = json.loads(text)
            
            # Save results
            self._save_results({
                "query": query,
                "answer": answer,
                "metrics": metrics
            })
            
            return metrics
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return {"faithfulness": 0.0, "context_precision": 0.0, "answer_relevance": 0.0}
            
    def _save_results(self, data: Dict[str, Any]):
        results = []
        if os.path.exists(self.eval_file):
            with open(self.eval_file, "r", encoding="utf-8") as f:
                try:
                    results = json.load(f)
                except:
                    pass
        results.append(data)
        with open(self.eval_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
