import logging
import json
import os
from datetime import datetime
from app.utils.config import settings

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
        }
        
        if hasattr(record, "query"): log_entry["query"] = record.query
        if hasattr(record, "latency"): log_entry["latency"] = record.latency
        if hasattr(record, "token_usage"): log_entry["token_usage"] = record.token_usage
        if hasattr(record, "retrieved_docs"): log_entry["retrieved_docs"] = record.retrieved_docs
        if hasattr(record, "errors"): log_entry["errors"] = record.errors
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

def setup_logger(name="kb_assistant"):
    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        os.makedirs("logs", exist_ok=True)
        
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(JsonFormatter())
        
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
