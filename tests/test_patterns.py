from src.patterns.observer import Observable, Observer

class DummyObserver(Observer):
    def __init__(self):
        self.updated = False
    def update(self, poll):
        self.updated = True

def test_observer_pattern():
    class DummyPoll(Observable):
        pass
    p = DummyPoll()
    obs = DummyObserver()
    p.attach(obs)
    p.notify()
    assert obs.updated