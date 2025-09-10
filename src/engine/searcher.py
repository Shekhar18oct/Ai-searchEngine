from typing import List, Dict, Any

from typing import List, Dict, Any, Optional
from .indexer import Indexer

class Searcher:
    def __init__(self, indexer: Optional[Indexer] = None):
        from typing import Optional
        self.indexer = indexer if indexer is not None else Indexer()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents matching the query
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries containing matched documents and their similarity scores
        """
        # Get similar documents from indexer
        if not self.indexer.documents:
            return []
            
        results = self.indexer.get_similar_documents(query, top_k)
        
        # Format results
        formatted_results = []
        for result in results:
            doc = result['document']
            formatted_results.append({
                'id': doc.id,
                'title': doc.title,
                'content': doc.content[:200] + '...' if len(doc.content) > 200 else doc.content,
                'url': doc.url,
                'similarity_score': result['similarity'],
                'created_at': doc.created_at.isoformat() if doc.created_at else None
            })
            
        return formatted_results

    def get_results(self):
        """Get all documents in the index"""
        return [doc.to_dict() for doc in self.indexer.get_index()]