from src.models.encuesta import Poll, PollMultiple, PollSimple

class PollFactory:
    @staticmethod
    def crear(tipo: str, pregunta: str, opciones: list, duracion_segundos: int) -> Poll:
        if tipo == "multiple":
            return PollMultiple(pregunta, opciones, duracion_segundos)
        else:
            return PollSimple(pregunta, opciones, duracion_segundos)
