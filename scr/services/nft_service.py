import uuid
from datetime import datetime
from typing import List

from src.models.token_nft import TokenNFT
from src.repositories.nft_repo import NFTRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.models.usuario import User

class NFTService:
    def __init__(self, nft_repo: NFTRepository, user_repo: UsuarioRepository):
        self.nft_repo = nft_repo
        self.user_repo = user_repo

    def mint_token(self, username: str, poll_id: str, opcion: str) -> TokenNFT:
        token = TokenNFT(
            token_id=str(uuid.uuid4()),
            owner=username,
            poll_id=poll_id,
            option=opcion,
            issued_at=datetime.utcnow()
        )
        self.nft_repo.guardar_token(token)

        user = self.user_repo.obtener_usuario(username)
        if user:
            user.tokens.append(token.token_id)
            self.user_repo.guardar_usuario(user)

        return token

    def listar_tokens_usuario(self, username: str) -> List[TokenNFT]:
        return self.nft_repo.obtener_tokens_por_usuario(username)

    def transferir_token(self, token_id: str, nuevo_owner: str, actual_owner: str) -> bool:
        token = self.nft_repo.obtener_token(token_id)
        if not token or token.owner != actual_owner:
            return False

        token.owner = nuevo_owner
        self.nft_repo.guardar_token(token)

        # Actualizar ambos usuarios
        viejo_usuario = self.user_repo.obtener_usuario(actual_owner)
        nuevo_usuario = self.user_repo.obtener_usuario(nuevo_owner)

        if not nuevo_usuario:
            return False

        if viejo_usuario:
            viejo_usuario.tokens.remove(token_id)
            self.user_repo.guardar_usuario(viejo_usuario)

        nuevo_usuario.tokens.append(token_id)
        self.user_repo.guardar_usuario(nuevo_usuario)

        return True
