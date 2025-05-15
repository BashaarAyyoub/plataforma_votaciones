import bcrypt
import uuid
from typing import Optional
from src.repositories.usuario_repo import UsuarioRepository
from src.models.usuario import User

class UserService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
        self.sesiones = {}  # username -> session_id

    def register(self, username: str, password: str) -> bool:
        if self.repo.existe_usuario(username):
            return False
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, password_hash=password_hash, tokens=[])
        self.repo.guardar_usuario(user)
        return True

    def login(self, username: str, password: str) -> Optional[str]:
        user = self.repo.obtener_usuario(username)
        if not user:
            return None
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            session_token = str(uuid.uuid4())
            self.sesiones[username] = session_token
            return session_token
        return None

    def is_logged_in(self, username: str) -> bool:
        return username in self.sesiones

    def logout(self, username: str):
        if username in self.sesiones:
            del self.sesiones[username]

    def get_usuario(self, username: str) -> Optional[User]:
        return self.repo.obtener_usuario(username)

    def update_usuario(self, user: User):
        self.repo.guardar_usuario(user)
