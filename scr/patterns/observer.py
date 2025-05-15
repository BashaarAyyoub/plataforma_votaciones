class Observer:
    def update(self, poll_id: str):
        pass

class Observable:
    def __init__(self):
        self._observadores = []

    def registrar_observador(self, obs: Observer):
        self._observadores.append(obs)

    def notificar_observadores(self, poll_id: str):
        for obs in self._observadores:
            obs.update(poll_id)
