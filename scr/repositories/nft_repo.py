import json
from pathlib import Path
from typing import List
from uuid import UUID
from datetime import datetime
from src.models.token_nft import TokenNFT

NFTS_FILE = Path("data/tokens.json")


class NFTRepository:
    def __init__(self, filepath=NFTS_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._guardar([])

    def _guardar(self, tokens: List[TokenNFT]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([self._serialize(t) for t in tokens], f, indent=2)

    def _cargar(self) -> List[TokenNFT]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [self._deserialize(t) for t in data]

    def _serialize(self, token: TokenNFT) -> dict:
        return {
            "token_id": str(token.token_id),
            "owner": token.owner,
            "poll_id": str(token.poll_id),
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        }

    def _deserialize(self, data: dict) -> TokenNFT:
        return TokenNFT(
            token_id=UUID(data["token_id"]),
            owner=data["owner"],
            poll_id=UUID(data["poll_id"]),
            option=data["option"],
            issued_at=datetime.fromisoformat(data["issued_at"])
        )

    def guardar_token(self, token: TokenNFT):
        tokens = self._cargar()
        tokens.append(token)
        self._guardar(tokens)

    def listar_por_usuario(self, username: str) -> List[TokenNFT]:
        return [t for t in self._cargar() if t.owner == username]

    def transferir_token(self, token_id: UUID, nuevo_owner: str) -> bool:
        tokens = self._cargar()
        actualizado = False
        for t in tokens:
            if t.token_id == token_id:
                t.owner = nuevo_owner
                actualizado = True
                break
        if actualizado:
            self._guardar(tokens)
        return actualizado
