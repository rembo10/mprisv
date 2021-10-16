#!/usr/bin/env python
import sys

import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType

from mprisv.bluez import Bluez
from mprisv.login import Login
from mprisv.player_manager import PlayerManager
from mprisv.interface import Interface
from mprisv.utils import get_ifaces

NAME='com.mprisv'
PATH='/com/mprisv'
IFACE='com.mprisv.Remote'

loop = asyncio.get_event_loop()

async def main():

    system_bus = await MessageBus(None, BusType.SYSTEM).connect()
    session_bus = await MessageBus().connect()

    pm = PlayerManager(session_bus)
    pm.add_listener()
    await pm.initialize()

    interface = Interface(IFACE, pm.run)
    session_bus.export(PATH, interface)
    await session_bus.request_name(NAME)

    bluez = Bluez(system_bus, pm.signal_handler)
    bluez.add_listener()

    login = Login(system_bus, pm.signal_handler)
    login.add_listener()

    await loop.create_future()

async def send(cmd: str):
    bus = await MessageBus().connect()
    [remote] = get_ifaces(bus, NAME, 'mprisv', PATH, [IFACE])
    if cmd == 'play':
        await remote.call_play()
    elif cmd == 'pause':
        await remote.call_pause()
    elif cmd == 'stop':
        await remote.call_stop()
    elif cmd == 'next':
        await remote.call_next()
    elif cmd == 'prev':
        await remote.call_prev()
    elif cmd == 'playpause':
        await remote.call_play_pause()
    else:
        print('Unknown command')

def start():
    if len(sys.argv) >= 2:
        loop.run_until_complete(send(sys.argv[1]))
    else:
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            print('Exiting')

if __name__ == '__main__':
    start()

