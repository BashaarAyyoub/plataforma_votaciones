from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class TokenNFT:
    token_id: UUID
    owner: str
    poll_id: UUID
    option: str
    issued_at: datetime
