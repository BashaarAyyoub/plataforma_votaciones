from src.controllers.cli_controller import CLIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

def test_cli_comando_crear(monkeypatch):
    ps = PollService()
    us = UserService()
    ns = NFTService()
    cli = CLIController(ps, us, ns)
    monkeypatch.setattr("builtins.input", lambda _: "Pizza o Sushi?")
    cli.ejecutar_comando("crear_encuesta 'Pizza o Sushi?' ['Pizza','Sushi'] 60 simple")
