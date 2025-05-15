from dataclasses import dataclass, field
from typing import List
from uuid import UUID


@dataclass
class User:
    username: str
    password_hash: str
    tokens: List[UUID] = field(default_factory=list)

    def agregar_token(self, token_id: UUID):
        self.tokens.append(token_id)

    def remover_token(self, token_id: UUID):
        if token_id in self.tokens:
            self.tokens.remove(token_id)
