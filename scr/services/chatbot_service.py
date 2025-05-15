from transformers import pipeline, Conversation
from typing import Dict
from src.services.poll_service import PollService

class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
        self.historial: Dict[str, Conversation] = {}

    def responder(self, username: str, mensaje: str) -> str:
        mensaje_lower = mensaje.lower()

        # Preguntas contextuales
        if "quién va ganando" in mensaje_lower:
            # Usamos la última encuesta activa
            activas = self.poll_service.encuesta_repo.listar_encuestas_activas()
            if not activas:
                return "No hay encuestas activas en este momento."
            poll = activas[-1]  # Última creada
            resultados = self.poll_service.get_partial_results(poll.id)
            if resultados:
                return f"La encuesta '{poll.pregunta}' va así: {resultados}"
            return "Aún no hay votos registrados."

        elif "cuánto falta" in mensaje_lower:
            activas = self.poll_service.encuesta_repo.listar_encuestas_activas()
            if not activas:
                return "No hay encuestas activas."
            poll = activas[-1]
            restante = (poll.fecha_inicio + poll.duracion_timedelta()) - datetime.utcnow()
            return f"Quedan aproximadamente {int(restante.total_seconds())} segundos para cerrar la encuesta."

        # Pregunta libre → IA
        if username not in self.historial:
            self.historial[username] = Conversation(mensaje)
        else:
            self.historial[username].add_user_input(mensaje)

        respuesta = self.chatbot(self.historial[username])
        return respuesta.generated_responses[-1]
