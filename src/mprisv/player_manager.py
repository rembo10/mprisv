import os
from typing import Callable

from dbus_next.aio import MessageBus

from mprisv.signals import Signal, Disconnect, Reconnect, Suspend, PlaybackStatusChanged
from mprisv.core import Status, Command
from mprisv.logger import get_log
from mprisv.utils import get_ifaces, is_mpris
from mprisv.player import Player

log=get_log(__name__)

NAME='org.freedesktop.DBus'
PATH='/org/freedesktop/DBus'
IFACE='org.freedesktop.DBus'

class PlayerManager:

    def __init__(self, bus: MessageBus):
        self._bus = bus
        [self._dbus] = get_ifaces(bus, NAME, 'dbus', PATH, [IFACE])
        self.players_by_name = {}
        self.player: str = None 
        self.status: Status = None
        self.last_player: str = None
        self.play_on_reconnect: bool = False
    async def _add_player(self, name):
        log.info(f'Adding player: {name}')
        player = Player(self._bus, self.signal_handler, name)
        player.add_listener()
        self.players_by_name[name] = player
        status = await player.status
        if not self.player:
            self.player = name 
            self.status = status
        elif status == Status.PLAYING:
            await self.signal_handler(PlaybackStatusChanged(name, Status.PLAYING))
    async def _remove_player(self, name):
        log.info(f'Removing player: {name}')
        self.players_by_name[name].remove_listener()
        self.players_by_name.pop(name)
        # catch players that don't send a stopped signal on exit
        if name == self.player and self.status != Status.STOPPED:
            await self.signal_handler(PlaybackStatusChanged(name, Status.STOPPED))
        if name == self.player:
            self.player = None
            self.status = None
        if name == self.last_player:
            self.last_player = None
    async def initialize(self, default_player=None):
        await self._get_initial_players()
    async def _get_initial_players(self):
        all_names = await self._dbus.call_list_names()
        for name in filter(is_mpris, all_names):
            await self._add_player(name)
    async def _handle_owner_change(self, name, new, old):
        if not is_mpris(name):
            return
        if old:
            await self._add_player(name)
        else:
            await self._remove_player(name)
    async def signal_handler(self, signal: Signal):
        log.info(f'Got signal: {signal}')
        if (signal == Disconnect or signal == Suspend) and self.status == Status.PLAYING:
            await self.run(Command.PAUSE)
            self.play_on_reconnect = True
        elif signal == Reconnect and self.play_on_reconnect and self.status == Status.PAUSED:
            await self.run(Command.PLAY)
        elif isinstance(signal, PlaybackStatusChanged):
            if signal.name == self.player:
                if signal.status == Status.STOPPED and self.last_player:
                    self.status = Status.STOPPED
                    await self.run(Command.PLAY, self.last_player)
                    self.last_player = None
                else:
                    self.status = signal.status
            elif signal.status == Status.PLAYING:
                if self.status == Status.PLAYING:
                    await self.run(Command.PAUSE, self.player)
                    self.last_player = self.player
                self.player = signal.name
                self.status = Status.PLAYING
            elif signal.status == Status.STOPPED and signal.name == self.last_player:
                self.last_player = None
            else:
                pass
    def add_listener(self):
        self._dbus.on_name_owner_changed(self._handle_owner_change)
    def remove_listener(self):
        self._dbus.off_name_owner_changed(self._handle_owner_change)
    async def run(self, command: Command, player: str=None):
        if not player:
            player = self.player
        log.info(f'Sending {command} to: {player}')
        await self.players_by_name[player].run(command)
