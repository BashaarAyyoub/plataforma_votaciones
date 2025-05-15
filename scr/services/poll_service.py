from datetime import datetime, timedelta
import uuid
from typing import List, Optional

from src.models.encuesta import Poll
from src.models.voto import Vote
from src.services.nft_service import NFTService
from src.patterns.observer import Observable
from src.patterns.strategy import DesempateStrategy
from src.patterns.factory import PollFactory
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.usuario_repo import UsuarioRepository

class PollService(Observable):
    def __init__(self, encuesta_repo: EncuestaRepository, user_repo: UsuarioRepository, nft_service: NFTService):
        super().__init__()
        self.encuesta_repo = encuesta_repo
        self.user_repo = user_repo
        self.nft_service = nft_service

    def create_poll(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple") -> Poll:
        poll = PollFactory.crear(tipo, pregunta, opciones, duracion_segundos)
        self.encuesta_repo.guardar_encuesta(poll)
        return poll

    def vote(self, poll_id: str, username: str, opciones: List[str]) -> bool:
        self.check_timeouts()

        poll = self.encuesta_repo.obtener_encuesta(poll_id)
        if not poll or not poll.activa:
            return False
        if poll.ya_voto(username):
            return False
        if not poll.votar(username, opciones):
            return False

        self.encuesta_repo.guardar_encuesta(poll)
        for opcion in opciones:
            self.nft_service.mint_token(username, poll_id, opcion)
        return True

    def close_poll(self, poll_id: str):
        poll = self.encuesta_repo.obtener_encuesta(poll_id)
        if not poll or not poll.activa:
            return

        poll.activa = False
        poll.fecha_cierre = datetime.utcnow()
        self.encuesta_repo.guardar_encuesta(poll)

        self.notificar_observadores(poll_id)

    def check_timeouts(self):
        for poll in self.encuesta_repo.listar_encuestas_activas():
            if datetime.utcnow() > poll.fecha_inicio + timedelta(seconds=poll.duracion_segundos):
                self.close_poll(poll.id)

    def get_partial_results(self, poll_id: str) -> Optional[dict]:
        poll = self.encuesta_repo.obtener_encuesta(poll_id)
        if not poll:
            return None
        return poll.resultados()

    def get_final_results(self, poll_id: str, estrategia: DesempateStrategy) -> Optional[dict]:
        poll = self.encuesta_repo.obtener_encuesta(poll_id)
        if not poll or poll.activa:
            return None

        resultados = poll.resultados()
        if poll.hay_empate(resultados):
            ganador = estrategia.resolver(poll, resultados)
            resultados["ganador_resuelto"] = ganador
        return resultados
