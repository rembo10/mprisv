from enum import Enum

from mprisv import events


class Status(Enum):
    PLAYING = 1
    PAUSED  = 2
    STOPPED = 3

class Command(Enum):
    PLAY       = 1
    PAUSE      = 2
    STOP       = 3
    NEXT       = 4
    PREV       = 5
    PLAY_PAUSE = 6

class App:

    def __init__(self, player: str = None, status: Status = None):
        self.player = player
        self.status = status
        self.last_player = None
        self.play_on_reconnect = False

    def handle_event(self, event):
        if event == events.Disconnect:
            if self.status == Status.PLAYING:
                self.play_on_reconnect = True
                return (self.player, Command.PAUSE)
            else:
                self.play_on_reconnect = False
                return None
        elif event == events.Reconnect and self.play_on_reconnect:
            self.play_on_reconnect = False
            return (self.player, Command.PLAY)
        elif isinstance(event, events.PlayerPlayed):
            if self.status == Status.PLAYING and self.player != event.player:
                self.last_player = self.player
                self.player = event.player
                return (self.last_player, Command.PAUSE)
            else:
                self.player = event.player
                self.status = Status.PLAYING
                return None
        elif event == events.PlayerPaused:
            self.status = Status.PAUSED
            return None
        elif event == events.PlayerStopped:
            self.status = Status.STOPPED
            if self.last_player:
                return (self.last_player, Command.PLAY)
            else:
                return None
        elif event == events.Suspend and self.status == Status.PLAYING:
            self.play_on_reconnect = True
            return (self.player, Command.PAUSE)
        else:
            return None
