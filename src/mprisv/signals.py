from dataclasses import dataclass

class Signal:
    pass

class Disconnect(Signal):
    pass

class Reconnect(Signal):
    pass

class Suspend(Signal):
    pass

@dataclass
class PlaybackStatusChanged(Signal):
    name: str
    status: str 
