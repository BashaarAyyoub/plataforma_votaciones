import uuid
from src.models.encuesta import Poll
from src.models.voto import Vote
from src.models.usuario import User
from src.models.token_nft import TokenNFT
from datetime import datetime

def test_poll_creation():
    p = Poll("Tu comida favorita?", ["Pizza", "Sushi"], 30, "simple")
    assert p.pregunta == "Tu comida favorita?"
    assert p.estado == "activa"

def test_vote_model():
    v = Vote("alice", "Pizza")
    assert v.username == "alice"

def test_user_model():
    u = User("bob", "hashedpass")
    assert u.username == "bob"

def test_token_nft_model():
    tid = uuid.uuid4()
    t = TokenNFT(tid, "alice", uuid.uuid4(), "Pizza", datetime.now())
    assert t.owner == "alice"
