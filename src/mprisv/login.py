from functools import reduce
from typing import Callable

from dbus_next.aio import MessageBus

from mprisv.signals import Suspend
from mprisv.utils import get_ifaces

NAME='org.freedesktop.login1'
PATH='/org/freedesktop/login1'
IFACE='org.freedesktop.login1.Manager'

class Login:
    def __init__(self, bus: MessageBus, on_signal: Callable):
        [self._login] = get_ifaces(bus, NAME, 'login', PATH, [IFACE]) 
        self._on_signal = on_signal
    def add_listener(self):
        self._login.on_prepare_for_sleep(self._on_prepare_for_sleep)
    def remove_listener(self):
        self._login.off_prepare_for_sleep(self._on_prepare_for_sleep)
    async def _on_prepare_for_sleep(self, down: bool):
        if down:
            await self._on_signal(Suspend)
