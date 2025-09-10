from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Document:
    title: str
    content: str
    id: str
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }