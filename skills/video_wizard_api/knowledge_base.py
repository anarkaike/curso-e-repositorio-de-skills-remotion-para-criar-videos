
import json
import time
import logging
import numpy as np
from typing import List, Optional, Any
from sqlmodel import Session, select
from sentence_transformers import SentenceTransformer
from models import KnowledgeEntry

# Global model instance (lazy loaded)
_model = None

def get_model():
    global _model
    if _model is None:
        logging.info("Loading SentenceTransformer model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        logging.info("Model loaded.")
    return _model

class KnowledgeBase:
    def __init__(self, session: Session):
        self.session = session
        self.model = get_model()

    def _get_embedding(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def find_similar(self, query_text: str, suggestion_type: str, threshold: float = 0.85) -> Optional[Any]:
        """
        Semantic search for cached suggestions.
        """
        query_embedding = self._get_embedding(query_text)
        
        # 1. Fetch all entries of same type (optimization: fetch only needed columns if possible)
        # For small scale, fetching all is fine.
        statement = select(KnowledgeEntry).where(KnowledgeEntry.suggestion_type == suggestion_type)
        results = self.session.exec(statement).all()
        
        best_match = None
        best_score = -1.0
        
        for entry in results:
            try:
                cached_embedding = json.loads(entry.embedding_json)
                score = self._cosine_similarity(query_embedding, cached_embedding)
                
                if score > best_score:
                    best_score = score
                    best_match = entry
            except Exception as e:
                logging.warning(f"Error parsing embedding for entry {entry.id}: {e}")
                continue
                
        if best_match and best_score >= threshold:
            logging.info(f"Cache hit for '{query_text}' ({suggestion_type}) - Score: {best_score:.2f}")
            return json.loads(best_match.response_json)
            
        logging.info(f"Cache miss for '{query_text}' ({suggestion_type}) - Best Score: {best_score:.2f}")
        return None

    def add_entry(self, query_text: str, suggestion_type: str, response_data: Any):
        """
        Add new entry to knowledge base.
        """
        embedding = self._get_embedding(query_text)
        
        entry = KnowledgeEntry(
            query_text=query_text,
            suggestion_type=suggestion_type,
            response_json=json.dumps(response_data),
            embedding_json=json.dumps(embedding),
            created_at=time.time()
        )
        
        self.session.add(entry)
        self.session.commit()
        logging.info(f"Saved to cache: '{query_text}' ({suggestion_type})")

