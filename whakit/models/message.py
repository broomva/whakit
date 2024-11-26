# whakit/models/message_models.py

from typing import Any, Dict, Optional

from pydantic import BaseModel


class Message(BaseModel):
    from_number: str
    message_type: str
    content: Dict[str, Any]
    message_id: str
