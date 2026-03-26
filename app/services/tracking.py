import json
import os
import time
from typing import Dict, Any
from app.utils.logger import logger

class MetricsTracker:
    def __init__(self):
        self.metrics_file = "logs/metrics.json"
        
    def _read_metrics(self) -> Dict[str, Any]:
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "total_requests": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "requests": []
        }
        
    def _write_metrics(self, data: Dict[str, Any]):
        os.makedirs("logs", exist_ok=True)
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def track_request(self, query: str, latency: float, token_usage: Dict[str, int]) -> None:
        try:
            data = self._read_metrics()
            
            data["total_requests"] += 1
            data["total_prompt_tokens"] += token_usage.get("prompt_tokens", 0)
            data["total_completion_tokens"] += token_usage.get("completion_tokens", 0)
            data["total_tokens"] += token_usage.get("total_tokens", 0)
            
            request_record = {
                "timestamp": time.time(),
                "query": query,
                "latency_sec": latency,
                "token_usage": token_usage
            }
            
            data["requests"].append(request_record)
            
            if len(data["requests"]) > 1000:
                data["requests"] = data["requests"][-1000:]
                
            self._write_metrics(data)
            
        except Exception as e:
            logger.error(f"Failed to track metrics: {e}")
            
    def get_aggregate_metrics(self) -> Dict[str, Any]:
        data = self._read_metrics()
        
        latencies = [r["latency_sec"] for r in data["requests"]]
        if latencies:
            latencies.sort()
            p50 = latencies[int(len(latencies) * 0.50)]
            p95 = latencies[int(len(latencies) * 0.95)]
        else:
            p50 = 0.0
            p95 = 0.0
            
        return {
            "total_requests": data["total_requests"],
            "total_tokens": data["total_tokens"],
            "p50_latency": p50,
            "p95_latency": p95
        }
