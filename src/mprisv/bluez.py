from typing import Callable

from dbus_next.aio import MessageBus

from mprisv.signals import Disconnect, Reconnect 
from mprisv.logger import get_log
from mprisv.utils import get_ifaces, is_headphones

log = get_log(__name__)

NAME='org.bluez'
PATH='/'
IFACE='org.freedesktop.DBus.ObjectManager'

class Bluez:
    def __init__(self, bus: MessageBus, on_signal: Callable):
        [self._bluez] = get_ifaces(bus, NAME, 'bluez', PATH, [IFACE])
        self._on_signal = on_signal
    def add_listener(self):
        self._bluez.on_interfaces_removed(self._on_interfaces_removed)
        self._bluez.on_interfaces_added(self._on_interfaces_added)
    def remove_listener(self):
        self._bluez.off_interfaces_removed(self._on_interfaces_removed)
        self._bluez.off_interfaces_added(self._on_interfaces_added)
    async def _on_interfaces_removed(self, path: str, ifs: list[str]):
        if is_headphones(ifs):
            await self._on_signal(Disconnect)
    async def _on_interfaces_added(self, path: str, ifs: dict):
        if is_headphones(ifs.keys()):
            await self._on_signal(Reconnect)
