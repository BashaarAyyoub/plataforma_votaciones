from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from uuid import uuid4, UUID


@dataclass
class Poll:
    id: UUID
    pregunta: str
    opciones: List[str]
    votos: Dict[str, int] = field(default_factory=dict)
    votos_por_usuario: Dict[str, List[str]] = field(default_factory=dict)  # username: opciones
    estado: str = "activa"  # o 'cerrada'
    timestamp_inicio: datetime = field(default_factory=datetime.utcnow)
    duracion_segundos: int = 60
    tipo: str = "simple"  # o 'multiple'

    def esta_activa(self) -> bool:
        if self.estado != "activa":
            return False
        tiempo_limite = self.timestamp_inicio + timedelta(seconds=self.duracion_segundos)
        return datetime.utcnow() < tiempo_limite

    def cerrar(self):
        self.estado = "cerrada"

    def agregar_voto(self, username: str, opciones_elegidas: List[str]) -> bool:
        if username in self.votos_por_usuario:
            return False  # ya votó

        for opcion in opciones_elegidas:
            if opcion not in self.opciones:
                continue
            self.votos[opcion] = self.votos.get(opcion, 0) + 1

        self.votos_por_usuario[username] = opciones_elegidas
        return True
