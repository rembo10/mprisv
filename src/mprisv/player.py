import os
from typing import Callable

from dbus_next.aio import MessageBus

from mprisv.core import Command, Status
from mprisv.signals import PlaybackStatusChanged
from mprisv.utils import get_ifaces

PATH='/org/mpris/MediaPlayer2'
PLAYER_IFACE='org.mpris.MediaPlayer2.Player'
PROPS_IFACE='org.freedesktop.DBus.Properties'

class Player:
    def __init__(self, bus: MessageBus, on_signal: Callable, name: str):
        self.name = name
        [self._player, self._props] = get_ifaces(bus, self.name, 'mpris', PATH, [
                PLAYER_IFACE, 
                PROPS_IFACE
            ])
        self._on_signal = on_signal
    def add_listener(self):
        self._props.on_properties_changed(self._handle_property_change)
    def remove_listener(self):
        self._props.off_properties_changed(self._handle_property_change)
    @property
    async def status(self) -> Status:
        status = await self._player.get_playback_status()
        return Status[status.upper()]
    async def run(self, command):
        if command == Command.PLAY:
            await self._player.call_play()
        elif command == Command.PAUSE:
            await self._player.call_pause()
        elif command == Command.NEXT:
            await self._player.call_next()
        elif command == Command.PREV:
            await self._player.call_previous()
        elif command == Command.STOP:
            await self._player.call_stop()
        elif command == Command.PLAY_PAUSE:
            await self._player.call_play_pause()
        else:
            pass
    async def _handle_property_change(self, iface, changed, invalidated):
        if 'PlaybackStatus' in changed:
            status = changed['PlaybackStatus'].value
            await self._on_signal(PlaybackStatusChanged(self.name, Status[status.upper()]))
