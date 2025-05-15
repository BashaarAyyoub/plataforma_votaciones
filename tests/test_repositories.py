from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.encuesta_repo import EncuestaRepository
from src.models.usuario import User

def test_usuario_repo_add():
    repo = UsuarioRepository()
    u = User("newuser", "hashed")
    repo.add(u)
    assert repo.get("newuser").username == "newuser"

def test_encuesta_repo_store_and_get():
    repo = EncuestaRepository()
    pid = "poll123"
    repo.store(pid, {"pregunta": "Q?"})
    assert repo.get(pid)["pregunta"] == "Q?"