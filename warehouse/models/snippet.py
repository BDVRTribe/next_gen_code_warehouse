from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class CodeSnippet:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    language: str
    tags: List[str] = field(default_factory=list)
    content: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

