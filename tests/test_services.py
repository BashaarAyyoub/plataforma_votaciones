import pytest
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

def test_create_and_vote_poll():
    ps = PollService()
    us = UserService()
    ns = NFTService()
    us.register("john", "pwd")
    pid = ps.create_poll("Test?", ["Yes", "No"], 30, "simple")
    ps.vote(pid, "john", ["Yes"])
    assert "john" in ps.encuestas[pid].votos

def test_double_vote_error():
    ps = PollService()
    pid = ps.create_poll("Test?", ["A", "B"], 30, "simple")
    ps.vote(pid, "eve", ["A"])
    with pytest.raises(ValueError):
        ps.vote(pid, "eve", ["B"])