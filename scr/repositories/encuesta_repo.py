import json
from pathlib import Path
from uuid import UUID
from typing import List, Optional
from src.models.encuesta import Poll
from datetime import datetime

ENCUESTAS_FILE = Path("data/encuestas.json")


class EncuestaRepository:
    def __init__(self, filepath=ENCUESTAS_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._guardar([])

    def _guardar(self, encuestas: List[Poll]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([self._serialize(p) for p in encuestas], f, indent=2, default=str)

    def _cargar(self) -> List[Poll]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [self._deserialize(p) for p in data]

    def _serialize(self, poll: Poll) -> dict:
        return {
            "id": str(poll.id),
            "pregunta": poll.pregunta,
            "opciones": poll.opciones,
            "votos": poll.votos,
            "votos_por_usuario": poll.votos_por_usuario,
            "estado": poll.estado,
            "timestamp_inicio": poll.timestamp_inicio.isoformat(),
            "duracion_segundos": poll.duracion_segundos,
            "tipo": poll.tipo,
        }

    def _deserialize(self, data: dict) -> Poll:
        return Poll(
            id=UUID(data["id"]),
            pregunta=data["pregunta"],
            opciones=data["opciones"],
            votos=data["votos"],
            votos_por_usuario=data.get("votos_por_usuario", {}),
            estado=data["estado"],
            timestamp_inicio=datetime.fromisoformat(data["timestamp_inicio"]),
            duracion_segundos=data["duracion_segundos"],
            tipo=data["tipo"]
        )

    def guardar_poll(self, poll: Poll):
        encuestas = self._cargar()
        encuestas = [p for p in encuestas if p.id != poll.id] + [poll]
        self._guardar(encuestas)

    def obtener_poll(self, poll_id: UUID) -> Optional[Poll]:
        encuestas = self._cargar()
        return next((p for p in encuestas if p.id == poll_id), None)

    def listar_activos(self) -> List[Poll]:
        return [p for p in self._cargar() if p.estado == "activa"]

    def listar_todos(self) -> List[Poll]:
        return self._cargar()
