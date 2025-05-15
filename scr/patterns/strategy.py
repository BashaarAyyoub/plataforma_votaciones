import random
from abc import ABC, abstractmethod

class DesempateStrategy(ABC):
    @abstractmethod
    def resolver(self, encuesta, resultados: dict) -> str:
        pass

class AlfabeticoStrategy(DesempateStrategy):
    def resolver(self, encuesta, resultados: dict) -> str:
        max_votos = max(resultados.values())
        empatados = [op for op, v in resultados.items() if v == max_votos]
        return sorted(empatados)[0]

class AleatorioStrategy(DesempateStrategy):
    def resolver(self, encuesta, resultados: dict) -> str:
        max_votos = max(resultados.values())
        empatados = [op for op, v in resultados.items() if v == max_votos]
        return random.choice(empatados)

class ProrrogaStrategy(DesempateStrategy):
    def resolver(self, encuesta, resultados: dict) -> str:
        # Reactiva la encuesta por otros 60s (simplificado)
        encuesta.duracion_segundos += 60
        encuesta.activa = True
        return "Empate detectado: encuesta reactivada por 60s"
