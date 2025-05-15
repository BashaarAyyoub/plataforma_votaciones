import json
from pathlib import Path
from typing import Optional, List
from src.models.usuario import User

USUARIOS_FILE = Path("data/usuarios.json")


class UsuarioRepository:
    def __init__(self, filepath=USUARIOS_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._guardar([])

    def _guardar(self, usuarios: List[User]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([u.__dict__ for u in usuarios], f, indent=2)

    def _cargar(self) -> List[User]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [User(**u) for u in data]

    def guardar_usuario(self, user: User):
        usuarios = self._cargar()
        usuarios = [u for u in usuarios if u.username != user.username] + [user]
        self._guardar(usuarios)

    def obtener_usuario(self, username: str) -> Optional[User]:
        for u in self._cargar():
            if u.username == username:
                return u
        return None

    def existe_usuario(self, username: str) -> bool:
        return self.obtener_usuario(username) is not None
