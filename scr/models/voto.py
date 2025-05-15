from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Vote:
    poll_id: UUID
    username: str
    opcion: str  # o List[str] si es múltiple
    timestamp: datetime
