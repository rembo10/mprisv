from dataclasses import dataclass

class Event:
    pass

class Disconnect(Event):
    pass

class Reconnect(Event):
    pass

class Suspend(Event):
    pass

@dataclass
class PlayerPlayed(Event):
    player: str

class PlayerStopped(Event):
    pass

class PlayerPaused(Event):
    pass
